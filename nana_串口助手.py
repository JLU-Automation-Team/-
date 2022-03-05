import re
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog
import tkinter.messagebox
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
from tkinter import END
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


global txtr2, txtr1, send_status, lx, ly, i, length
global uart, parity, bytesize, stopbits, baud
global canv, frame2, combobox1




def ui():
    # 建造一个窗口 wind
    wind = tk.Tk()
    wind.title("串口助手_nana")
    wind.geometry('800x600')
    wind.resizable(False, False)

    # 建造一个画布 canv
    canv = tk.Canvas(wind, width=800, height=600, bg="#87CEFA")
    canv.create_rectangle(14, 14, 520, 360, outline='black')
    canv.create_oval(695, 330, 715, 350, fill='black')
    canv.place(x=0, y=0)

    # 设置标签
    lab1 = tk.Label(wind, text="串口选择：", background="#87CEFA", font=("", 11))
    lab1.place(x=540, y=14)
    lab2 = tk.Label(wind, text="波特率：", background="#87CEFA", font=("", 11))
    lab2.place(x=540, y=67)
    lab3 = tk.Label(wind, text="停止位：", background="#87CEFA", font=("", 11))
    lab3.place(x=540, y=95)
    lab4 = tk.Label(wind, text="数据位：", background="#87CEFA", font=("", 11))
    lab4.place(x=540, y=123)
    lab5 = tk.Label(wind, text="校验位：", background="#87CEFA", font=("", 11))
    lab5.place(x=540, y=151)
    lab6 = tk.Label(wind, text="串口操作：", background="#87CEFA", font=("", 12))
    lab6.place(x=540, y=184)
    lab7 = tk.Label(wind, text="数据操作：", background="#87CEFA", font=("", 12))
    lab7.place(x=540, y=237)
    lab8 = tk.Label(wind, text="测试状态：", background="#87CEFA", font=("", 12))
    lab8.place(x=540, y=290)
    lab9 = tk.Label(wind, text="串口状态：", background="#87CEFA", font=("", 12))
    lab9.place(x=540, y=333)

    # 文本显示框
    txtr = tk.scrolledtext.ScrolledText(width=61, height=20)
    txtr.place(x=15, y=16)

    # 制作菜单
    mainmenu = tk.Menu(wind)  # 制作主菜单
    filemenu = tk.Menu(mainmenu, tearoff=False)   # 制作子菜单
    mainmenu.add_cascade(label='关于', menu=filemenu)  # 把子菜单放入顶端菜单
    filemenu.add_command(label='关于', command=menucommand, accelerator="Ctrl+N")  # 添加命令菜单项
    filemenu.add_separator()  # 添加分割线
    filemenu.add_command(label="退出", command=wind.quit)  # 退出
    wind.bind("<Control-n>", menucommand)  # 绑定触发事件
    wind.config(menu=mainmenu)  # 显示菜单

    # 制作按钮
    butt1 = tk.Button(wind, text="开启串口", command=uart_open)
    butt1.place(x=620, y=194)
    butt2 = tk.Button(wind, text="关闭串口", command=uart_close)
    butt2.place(x=710, y=194)
    butt3 = tk.Button(wind, text="清除接收", command=clear_reception)
    butt3.place(x=620, y=247)
    butt4 = tk.Button(wind, text="保存接收", command=receive_reception)
    butt4.place(x=710, y=247)
    butt8 = tk.Button(wind, text="实时绘图", command=draw)
    butt8.place(x=655, y=290)

    # 制作端口组合框
    combobox1 = ttk.Combobox(master=wind,
                             height=10,
                             width=25,
                             state='readonly',
                             cursor='arrow',
                             font=('', 11))
    combobox1.place(x=550, y=40)

        # 获取端口
    def uart_get():
        while True:
            uart_list = []
            uart_class = serial.tools.list_ports.comports()
            for i in uart_class:
                uart_list.append(i[0])
                # 如果发现端口，则将端口加入list中
            if uart_list:
                combobox1["values"] = uart_list

    thread3 = myThread(4, "Thread-4", uart_get)
    thread3.daemon = True
    thread3.start()

    # 获取选择的端口
    def option1(event):
        uart = combobox1.get()

    combobox1.bind('<<ComboboxSelected>>', option1)

    # 制作波特率组合框
    values2 = ['9600', '14400', '19200', '38400', '57600', '115200', '256000', '460800']
    combobox2 = ttk.Combobox(master=wind,
                             height=10,
                             width=10,
                             state='readonly',
                             cursor='arrow',
                             font=('', 11),
                             values=values2)
    combobox2.place(x=600, y=67)
    combobox2.current(0)

    def option2(event):
        baud = combobox2.get()
    combobox2.bind('<<ComboboxSelected>>', option2)

    # 制作停止位组合框
    values3 = ['1', '1.5', '2']
    combobox3 = ttk.Combobox(master=wind,
                             height=10,
                             width=10,
                             state='readonly',
                             cursor='arrow',
                             font=('', 11),
                             values=values3)
    combobox3.place(x=600, y=97)
    combobox3.current(0)

    def option3(event):
        stopbits = combobox3.get()

        if stopbits == 1 or stopbits == 2:
            stopbits = int(stopbits)
        else:
            stopbits = float(stopbits)

    combobox3.bind('<<ComboboxSelected>>', option3)

    # 制作数据位组合框
    values4 = ['8', '7']
    combobox4 = ttk.Combobox(master=wind,
                             height=10,
                             width=10,
                             state='readonly',
                             cursor='arrow',
                             font=('', 11),
                             values=values4)
    combobox4.place(x=600, y=127)
    combobox4.current(0)

    def option4(event):
        bytesize = combobox4.get()
    combobox4.bind('<<ComboboxSelected>>', option4)

    # 制作校验位组合框
    values5 = ["奇校验", "偶校验", "无校验"]
    combobox5 = ttk.Combobox(master=wind,
                             height=10,
                             width=10,
                             state='readonly',
                             cursor='arrow',
                             font=('', 11),
                             values=values5)
    combobox5.place(x=600, y=158)
    combobox5.current(0)

    def option5(event):
        parity = combobox5.get()

        if parity == "奇校验":
            parity = 'O'
        elif parity == "偶校验":
            parity = 'E'
        elif parity == "无校验":
            parity = 'N'

    combobox5.bind('<<ComboboxSelected>>', option5)

    # 制作notebook
    notebook = tkinter.ttk.Notebook(wind, width=800, height=185)
    notebook.place(x=14, y=370)
    # 制作框架
    frame1 = tkinter.Frame()
    frame2 = tkinter.Frame()
    # 第一个框架串口发送
    notebook.add(frame1, text="串口发送")
    canv1 = tk.Canvas(frame1, width=800, height=600, bg="#87CEFA")
    canv1.create_rectangle(2, 2, 600, 151, outline='black')
    canv1.place(x=0, y=0)
    txtr2 = tk.scrolledtext.ScrolledText(frame1, width=75, height=11)
    txtr2.place(x=0, y=0)
    # frame1中的label与button
    lab10 = tk.Label(frame1, text="发送操作：", background="#87CEFA", font=("", 11))
    lab10.place(x=640, y=0)
    butt5 = tk.Button(frame1, text="发送", command=send)
    butt5.place(x=670, y=40)
    butt6 = tk.Button(frame1, text="清除发送", command=clear_send)
    butt6.place(x=670, y=80)
    butt7 = tk.Button(frame1, text="读取文件", command=read_file)
    butt7.place(x=670, y=120)

    # 第二个框架图片显示
    notebook.add(frame2, text="图片显示")
    # 制作横轴长度组合框
    value6 = ['20', '50', '100', '200', '400', '800', '2000', ]
    combobox6 = ttk.Combobox(
        master=frame2,  # 父容器
        height=4,  # 高度,下拉显示的条目数量
        width=6,  # 宽度
        state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=('', 12),  # 字体
        values=value6,  # 设置下拉框的选项
    )
    combobox6.current(2)
    combobox6.place(x=700,y=0)
    # frame2中的label与button
    lab10 = tk.Label(frame2, text="横轴长度：", font=("", 11))
    lab10.place(x=600, y=0)
    butt8 = tk.Button(frame2, text="清除", command=clear_image)
    butt8.place(x=670, y=40)


    wind.mainloop()

    def optoion6(event):
        length = combobox6.get()
        combobox6.bind('<<ComboboxSelected>>', optoion6)


def update():
    status = "go"
    text = ""
    i = 0
    # 设定串口属性
    ser = serial.Serial(uart, int(baud), timeout=0.02)
    ser.parity = parity
    ser.bytesize = int(bytesize)
    ser.stopbits = stopbits
    canv.create_oval(695, 330, 715, 350, fill='red')
    canv.place(x=0, y=0)
    # 不停进行读写操作
    while True:
        try:
            # 向串口发送
            if send_status == "go":
                result = txtr2.get("1.0","end")+"\r\n"
                ser.write(result.encode())
                send_status = "stop"
            # 从串口接收
            size = ser.inWaiting()
            if size != 0:
            # 死循环重复接收
                while True:
                    reception = ser.read(size)
                    txtr1.insert("insert", reception)
                    txtr1.yview_moveto(1.0)
                    # 读取的文件
                    if text.endswith("\r\n"):
                        try:
                            # 俺也不知道为啥要有个1
                            print("1")
                            # 这个正则到底是嘛意思
                            findlink = re.compile(r'ng=(.*)')
                            data = float(re.findall(findlink, text)[0])
                            #读完清空
                            text=''
                            ly.append(data)
                            lx.append(i)
                            i += 1
                            break
                        except Exception as e:
                            print("读取文件失败%s" % e)
                    else:
                        try:
                            text = text + reception.decode()
                        except Exception as e:
                            print("我怎么知道这是啥问题%s" % e)
                    # 看看是不是关闭串口
                    if status == "stop":
                        print("stopstop")
                        canv.create_oval(695, 330, 715, 350, fill='black')
                        canv.place(x=0, y=0)
                        canv.update()
                        break
                if status == "stop":
                    print("stopstop")
                    canv.create_oval(695, 330, 715, 350, fill='black')
                    canv.place(x=0, y=0)
                    canv.update()
                    break
        except Exception as e:
            print("我怎么知道这是啥问题%s" % e)


def draw():
    thread4 = myThread(4, "Thread-4", image)
    thread4.daemon = True
    thread4.start()

# 画图
def image():
    # 死循环狂画
    while True:
        try:
            # 擦干净
            plt.cla()
            start = len(lx)-int(length)
            if start < 0:
                start = 0
            # 设置xy轴范围
            plt.xlim(start, len(lx))
            plt.ylim(1.2*min(ly), 1.2*max(ly))
            plt.plot(lx,ly)
            fig, ax = plt.subplots()
            canv2 = FigureCanvasTkAgg(fig, frame2)
            canv2.draw()
            canv2.get_tk_widget().pack(side=tk.BOTTOM,
                                       fill=tk.BOTH,
                                       expand=tk.YES)
            frame2.update()
        except Exception as e:
            print("画图出问题了%s" % e)
            continue

def clear_image():
    lx = []
    ly = []
    i = 0


def read_file():
    # 读取文件
    filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),))
    if filename != "":
        try:
            with open(filename, "r", newline='') as f:
                text = f.read()
                txtr1.insert("insert", text)
        except Exception as e:
            print("读取文件出现问题%s" % e)


def clear_send():
    txtr2.delete(1.0, END)


def send():
    send_status = "go"



def uart_open():
    """"开启串口"""
    thread2 = myThread(2, "Thread-2", update)
    thread2.daemon = True
    thread2.start()


def uart_close():
    """关闭串口"""
    status = "stop"
    print("stop")


def clear_reception():
    """清除接收"""
    txtr1.delete(1.0, END)
    print("clear reception")


def receive_reception():
    """保留接收"""
    status = "stop"
    result = txtr1.get("1.0", "end")
    filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),))
    if filename != "":
        try:
            with open(filename + ".txt", "w+") as f:
                f.write(result)
                f.close()
        except Exception as e:
            print("保留失败%s" % e)


def menucommand():
    """子菜单command函数"""
    tk.messagebox.showinfo("balabala")

# 区分线程来使得ui和刷新异步
class myThread(threading.Thread):
    def __init__(self, threadID, name, function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function

    def run(self):
        self.function()


if __name__ == '__main__':
    baud = 115200
    parity = 'N'
    bytesize = 8
    stopbits = 1
    send_status = "stop"
    ly = [0]
    lx = [0]
    data = 0
    i = 0
    length = 100
    thread1 = myThread(1, "Thread-1", ui)
    thread1.start()




