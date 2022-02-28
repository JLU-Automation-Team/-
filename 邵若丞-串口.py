import serial.tools.list_ports
import tkinter as tk
global ser


def search():
    global var
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        var.set("没有发现端口!")
    else:
        var.set("发现%d个串口" %len(plist))
def open():
    global ser
    global var1
    var1=le2.get()
    plist = list(serial.tools.list_ports.comports())
    plist_0 = list(plist[int(var1)-1])
    serialName = plist_0[0]
    ser = serial.Serial(serialName, 9600, timeout=60)
    var.set("第%d个串口已准备好"%int(var1))
#open(1)
# search()
#print(ser.parity)
#print(ser.stopbits)
#print(ser.bytesize)
def attribute():
    global ser
    ser.parity = le5.get()
    ser.stopbits = float(le3.get())
    ser.bytesize = int(le4.get())
    ser.baudrate = int(le9.get())
    var.set("已准备就绪")


def send():
    global ser
    try:
        ser.write(te7.get().encode("gbk"))
        var.set("已成功发送！")
    except :
        var.set("未成功发送")





def accept():

    global ser
    try:
        var.set("接收完成")
        data =ser.read(ser.in_waiting).decode("utf-8")
        t8.insert('end', str(data))
    except:
        var.set("接收失败！")


        # for i in range(ser.in_waiting):
        #     t8.insert('end',str(ser.read(1)))



window=tk.Tk()
window.title('串口助手')
window.geometry('300x300')
var=tk.StringVar()
var1=tk.StringVar()
b1=tk.Button(window,text="查询串口",command=search)
b1.place(x=0,y=0)
lb1=tk.Label(window,textvariable=var,bg='red',width=30,height=2,font=('Arial',8))
lb1.place(x=80,y=0)
l2=tk.Label(window,text="输入第几个串口")
l2.place(x=0,y=40)
b=tk.Button(window,text="确定",command=open)
b.place(x=100,y=40)
le2=tk.Entry(window,bg='green')
le2.place(x=0,y=60)
l3=tk.Label(window,text="停止位1/1.5/2")
l3.place(x=0,y=80)
le3=tk.Entry(window,bg='green')
le3.place(x=0,y=100)
l4=tk.Label(window,text="数据位")
l4.place(x=0,y=120)
le4=tk.Entry(window,bg='green')
le4.place(x=0,y=140)
l5=tk.Label(window,text="校验位N/E/O")
l5.place(x=0,y=160)
le5=tk.Entry(window,bg='green')
le5.place(x=0,y=180)
l9=tk.Label(window,text="波特率（9600等）")
l9.place(x=0,y=200)
le9=tk.Entry(window,bg='green')
le9.place(x=0,y=220)
b6=tk.Button(window,text="确定并打开",command=attribute)
b6.place(x=0,y=240)
b7=tk.Button(window,text="发送数据",command=send)
b7.place(x=150,y=40)
te7=tk.Entry(window,width=20)
te7.place(x=150,y=80)
b8=tk.Button(window,text="接收数据",command=accept)
b8.place(x=150,y=140)
t8=tk.Text(window,width=20,height=4)
t8.place(x=150,y=180)

window.mainloop()








