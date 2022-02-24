import serial
import tkinter as tk
import threading
from tkinter import scrolledtext, ttk
import serial.tools.list_ports
import time


# tkinter要求由按钮（或者其它的插件）触发的控制器函数不能含有参数
# 若要给函数传递参数，需要在函数前添加lambda。
# 类是不能调用实例属性的
# 停止位1可对应数据位：5、6、7、8
# 停止位1.5可对应数据位：5
# 停止位2可对应数据位：6、7、8
# 由于技术问题没有攻克，这个版本直接删去停止位1.5来避免报错

class Port:
    def __init__(self, uart,baud,stopbits,databits,paritybits):
        self.ser = serial.Serial(port=uart,baudrate=baud,stopbits=stopbits,bytesize=databits,parity=paritybits, timeout=0.02)  # 串口

    # 发送数据
    def send(self, text):
        ser.write(text.encode('utf-8'))

    # 接收数据
    def receive(self, text):
        ser.readall(text.encode('utf-8'))

    # 打开串口
    def open(self):
        global state
        if self.ser.isOpen() == True:
            state = 'on'

        else:
            self.ser.open()
            state = 'on'

    # 关闭窗口
    def close(self):
        global state
        if self.ser.isOpen() == False:
            state = 'off'

        else:
            self.ser.close()
            state = 'off'

    def send_data(self,text):
        self.ser.write(text)

    def receive_data(self):
        data = self.ser.readall()
        return data


class UI:

    def __init__(self):
        global window, combobox1, state,combobox2,combobox3,combobox4,combobox5,se_text,re_text

        window = tk.Tk()  # 实例化object，建立窗口window
        window.title('串口助手')  # 标题
        window.geometry('705x525')  # 窗口尺寸
        self.state = False  # 开闭属性
        self.uart_list = []  # 可用串口
        # 串口状态圆孔
        self.statecolor = 'black'
        self.Port_chosen = Port
        self.canvas = tk.Canvas(window, width=705, height=525, bg="#F5F5F5")
        self.canvas.place(x=0, y=0)
        # 端口检测线程
        thread1 = threading.Thread(target=self.uart_dect, daemon=True)
        thread1.start()
        time.sleep(1)
        #串口选择框
        combobox1 = ttk.Combobox(window, state='readonly', height=3, width=17, font=('宋体', 10), values=self.uart_list)
        self.uart = combobox1.get()
        combobox1.place(x=555, y=35)
        # 组合框控件部署-波特率选择组合框
        baud_rate_values = [9600, 14400, 19200, 38400, 57600, 76800,115200, 128000,230400,256000, 460800]
        combobox2 = ttk.Combobox(window, height=6, width=10, state='readonly', font=('宋体', 10), value=baud_rate_values)
        combobox2.current(0)
        combobox2.place(x=605, y=65)
        self.baud = combobox2.get()
        # 组合框控件部署-停止位选择组合框
        stopbits_values = [1, 2]
        combobox3 = ttk.Combobox(window, height=3, width=10, state='readonly', font=('宋体', 10), value=stopbits_values)
        combobox3.current(0)
        combobox3.place(x=605, y=96)
        self.stopbits = combobox3.get()
        # 组合框控件部署-数据位选择组合框
        databits_values = [8, 7,6,5]
        combobox4 = ttk.Combobox(window, height=4, width=10, state='readonly', font=('宋体', 10), value=databits_values)
        combobox4.current(0)
        combobox4.place(x=605, y=127)
        self.databits = combobox4.get()

        # 组合框控件部署-校验位选择组合框
        paritybits_values = ["奇校验", "偶校验", "无校验"]
        combobox5 = ttk.Combobox(window, height=3, width=10, state='readonly', font=('宋体', 10), value=paritybits_values)
        combobox5.current(2)
        self.paritybits=combobox5.get()
        if self.paritybits == '奇校验':
            self.paritybits = 'O'
        elif self.paritybits == '偶校验':
            self.paritybits = 'E'
        else:
            self.paritybits = 'N'
        combobox5.place(x=605, y=158)

        thread4 = threading.Thread(target=self.attribute_get, daemon=True)
        thread4.start()

        # Port类更新线程
        thread2 = threading.Thread(target=self.Port_refresh, daemon=True)
        thread2.start()
        time.sleep(1)

        thread3 = threading.Thread(target=self.light, daemon=True)
        thread3.start()

        # 设定标签
        label1 = tk.Label(window, text='串口选择', font=('宋体', 10)).place(x=550, y=5)
        label2 = tk.Label(window, text='波特率', font=('宋体', 10)).place(x=550, y=65)
        label3 = tk.Label(window, text='停止位', font=('宋体', 10)).place(x=550, y=96)
        label4 = tk.Label(window, text='数据位', font=('宋体', 10)).place(x=550, y=127)
        label5 = tk.Label(window, text='校验位', font=('宋体', 10)).place(x=550, y=158)
        label6 = tk.Label(window, text='串口操作：', font=('宋体', 10)).place(x=550, y=189)
        label7 = tk.Label(window, text = '串口状态：',font =('宋体', 10)).place(x = 550,y=276)

        button3 = tk.Button(window, text='打开串口', command=lambda: self.Port_chosen(uart=self.uart,baud=self.baud,stopbits=self.stopbits,databits=self.databits,paritybits=self.paritybits).open())
        button3.place(x=625, y=183)
        button4 = tk.Button(window, text='关闭串口', command=lambda: self.Port_chosen(uart=self.uart,baud=self.baud,stopbits=self.stopbits,databits=self.databits,paritybits=self.paritybits).close())
        button4.place(x=625, y=218)

        #接收框
        re_text = tk.scrolledtext.ScrolledText(width=74, height=22)
        re_text.place(x=5, y=5)
        #接收数据线程
        thread5 = threading.Thread(target = self.receive,daemon=True)
        thread5.start()


        #发送框
        se_text = tk.scrolledtext.ScrolledText(width=70,height = 13)
        se_text.place(x=5, y=310)

        button5 = tk.Button(window,text = '发送',command = self.send)
        button5.place(x=600,y=350)
        button6 = tk.Button(window,text = '清除发送',command = self.clear_send)
        button6.place(x = 600,y=400)



        window.mainloop()

    def uart_dect(self):
        global window, combobox1
        while True:
            for i in serial.tools.list_ports.comports():  # 为所有的串口分别生成ListPortInfo object，列表封装，是个迭代器
                if i[0] in self.uart_list:
                    pass
                elif i[0] not in self.uart_list:
                    self.uart_list.append(i[0])
            time.sleep(0.01)

    def attribute_get(self):
        global combobox1, window,combobox2,combobox3,combobox4,combobox5
        while True:
            self.uart = combobox1.get()
            self.baud = combobox2.get()
            self.stopbits = combobox3.get()
            self.stopbits = int(self.stopbits)
            self.databits = combobox4.get()
            self.databits = int(self.databits)
            self.paritybits = combobox5.get()
            if self.paritybits =='奇校验':
                self.paritybits ='O'
            elif self.paritybits =='偶校验':
                self.paritybits='E'
            else:
                self.paritybits='N'


    def Port_refresh(self):
        while True:
            self.Port_chosen.uart = self.uart
            time.sleep(0.01)

    def light(self):
        global state
        while True:
            if state == 'on':
                self.canvas.create_oval(630, 275, 650, 295, fill='red')  # 串口状态显示
                self.canvas.update()
            else:
                self.canvas.create_oval(630, 275, 650, 295, fill='black')
                self.canvas.update()

    def send(self):
        global se_text
        text = se_text.get(1.0,'end')
        self.Port_chosen.send_data(
            text=text
        )

    def clear_send(self):
        global se_text
        text = se_text.get(1.0, 'end')
        self.Port_chosen.send_data(
            text=text
        )
        se_text.delete(1.0, 'end')

    def receive(self):
        global re_text
        while True:
            re_text.insert('insert',self.Port_chosen(uart=self.uart,baud=self.baud,stopbits=int(self.stopbits),databits=int(self.databits),paritybits=self.paritybits).receive_data())


if __name__ == '__main__':
    state = 'off'
    UI()
