import tkinter as tk
from tkinter import ttk
import serial
from tkinter import *
# 窗口基本形状
window = tk.Tk()
window.title("串口助手 by 冉钊")
window.geometry("400x500+500+200")

portx = ""
baudrate = 0
stopbits = serial.STOPBITS_ONE
Parity = serial.PARITY_NONE
bytesize = serial.EIGHTBITS


def com():
    if chuankou.current() == 0:  # com3    get()方法能得当前选项的值
        global portx
        portx = "com3"
    elif chuankou.current() == 1:  # com6
        portx = "com6"
    else:
        portx = "com4"  # com4


def botelv_function():
    global baudrate
    if botelv.current() == 0:  # 57600
        baudrate = 57600
    elif botelv.current() == 1:  # 115200
        baudrate = 115200
    elif botelv.current() == 2:  # 256000
        baudrate = 25600
    else:
        baudrate = 460800  # 460800


def tingzhiwei_function():
    global stopbits
    if tingzhiwei.current() == 0:
        stopbits = serial.STOPBITS_ONE
    elif tingzhiwei.current() == 1:
        stopbits = serial.STOPBITS_ONE_POINT_FIVE
    elif tingzhiwei.current() ==2:
        stopbits = serial.STOPBITS_TWO


def shujuwei_function():
    global bytesize
    if shujuwei.current() == 0:  # 分别是’8‘和’7‘
        bytesize = serial.EiGHTBITS
    elif shujuwei.current() == 1:
        bytesize = serial.SEVENBITS


def jiaoyanwei_function():
    global Parity
    if jiaoyanwei.current() == 0:  # 分别是奇校验 偶校验 无校验
        Parity = serial.PARITY_ODD
    elif jiaoyanwei.current() == 1:
        Parity = serial.PARITY_EVEN
    elif jiaoyanwei.current() == 2:
        Parity = serial.PARITY_NONE


def start():
    com()
    botelv_function()
    tingzhiwei_function()
    shujuwei_function()
    jiaoyanwei_function()
    global ser
    ser = serial.Serial(portx, baudrate, bytesize, Parity, stopbits,
                        timeout=None, xonxoff=0, rtscts=0, interCharTimeout=None)
    try:
        if ser.is_open:
            pass
        ser.open()
        while True:
            if ser.in_waiting:
                str1 = ser.read(ser.in_waiting).decode("gbk")
            if str == "exit":  # 退出标志
                break
            else:
                txt1.insert(END, str1)
    except Exception as e:
            print("---异常---：", e)


def close():
    ser.close()


def send():
    s = txt2.get("1.0", END)
    ser.write(s.encode("gbk"))


frame1 = Frame(master=window,  padx=5, pady=10, width=220, height=250)
frame2 = Frame(master=window,  padx=5, pady=10, width=220, height=120)
frame1.place(relx=0, rely=0.05)
frame2.place(relx=0, rely=0.75)

txt1 = Text(frame1, width=25, height=20)
txt2 = Text(frame2, width=25, height=5)
txt1.pack(side='left', fill=BOTH, expand=True)
txt2.pack(side='left', fill=BOTH, expand=True)

scr1 = Scrollbar(frame1)
scr1.pack(side=RIGHT, fill=Y)
scr2 = Scrollbar(frame2)
scr2.pack(side=RIGHT, fill=Y)

txt1.config(yscrollcommand=scr1.set)   # 文本框和滚动条结合
scr1.config(command=txt1.yview)
txt2.config(yscrollcommand=scr2.set)
scr2.config(command=txt2.yview)

button1 = tk.Button(window, text="开启串口", command=start)  # 这里应该有command 以后加上
button2 = tk.Button(window, text="关闭串口", command=close )
button3 = tk.Button(window, text="清除接受", command=lambda: txt1.delete('1.0', END))  # command=lambda”:函数名（参数列表）
button4 = tk.Button(window, text="保存接受")
button5 = tk.Button(window, text="发送", width=7, command=send)
button6 = tk.Button(window, text="清除发送", command=lambda: txt2.delete('1.0', END))
button1.place(relx=0.65, rely=0.5)
button2.place(relx=0.85, rely=0.5)
button3.place(relx=0.65, rely=0.65)
button4.place(relx=0.85, rely=0.65)
button5.place(relx=0.65, rely=0.8)
button6.place(relx=0.85, rely=0.8)

label1 = tk.Label(window,
                  text="串口选择:",
                  font=("楷体", 12),
                  width=15, height=2)
label2 = tk.Label(window,
                  text="波特率：",
                  font=("楷体", 12),
                  width=15, height=2)
label3 = tk.Label(window,
                  text="停止位:",
                  font=("楷体", 12),
                  width=15, height=2)
label4 = tk.Label(window,
                  text="数据位:",
                  font=("楷体", 12),
                  width=15, height=2)
label5 = tk.Label(window,
                  text="校验位:",
                  font=("楷体", 12),
                  width=15, height=2)
label6 = tk.Label(window,
                  text="串口操作:",
                  font=("楷体", 12),
                  width=15, height=2)
label7 = tk.Label(window,
                  text="数据操作:",
                  font=("楷体", 12),
                  width=15, height=2)
label8 = tk.Label(window,
                  text="接收数据:",
                  font=("楷体", 12),
                  width=15, height=2)
label9 = tk.Label(window,
                  text="发送数据:",
                  font=("楷体", 12),
                  width=15, height=2)
label1.place(relx=0.55, rely=0)
label2.place(relx=0.55, rely=0.1)
label3.place(relx=0.55, rely=0.15)
label4.place(relx=0.55, rely=0.2)
label5.place(relx=0.55, rely=0.25)
label6.place(relx=0.55, rely=0.42)
label7.place(relx=0.55, rely=0.58)
label8.place(relx=0, rely=0, y=-5)
label9.place(relx=0, rely=0.69)

var1 = tk.StringVar()
chuankou = ttk.Combobox(window, textvariable=var1, width=6, height=2)
chuankou['values'] = ('COM3', 'COM6', 'COM4')
chuankou['state'] = 'readonly'
chuankou.current(0)
chuankou.place(relx=0.8, rely=0.005)


var2 = tk.StringVar()
botelv = ttk.Combobox(window, textvariable=var2, width=6, height=2)
botelv['values'] = ('57600', '115200', '256000', '460800')
botelv['state'] = 'readonly'
botelv.current(0)
botelv.place(relx=0.8, rely=0.105)

var3 = tk.StringVar()
tingzhiwei = ttk.Combobox(window, textvariable=var3, width=6, height=2)
tingzhiwei['values'] = ('1', '1.5', '2')
tingzhiwei['state'] = 'readonly'
tingzhiwei.current(0)
tingzhiwei.place(relx=0.8, rely=0.155)

var4 = tk.StringVar()
shujuwei = ttk.Combobox(window, textvariable=var4, width=6, height=2)
shujuwei['values'] = ('8', '7')
shujuwei['state'] = 'readonly'
shujuwei.current(0)
shujuwei.place(relx=0.8, rely=0.205)

var5 = tk.StringVar()
jiaoyanwei = ttk.Combobox(window, textvariable=var5, width=6, height=2)
jiaoyanwei['values'] = ('奇校验', '偶校验', '无校验')
jiaoyanwei['state'] = 'readonly'
jiaoyanwei.current(2)
jiaoyanwei.place(relx=0.8, rely=0.255)

window.mainloop()

