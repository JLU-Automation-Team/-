from socket import timeout
import LCOMX_gui
import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer

class lcomx(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=LCOMX_gui.Ui_LCOMX()
        self.ui.setupUi(self)
        get_portlist(self.ui)
        self.paritylist=["N","O","E"]
        self.port_change()
        # self.ui.textEdit.setPlainText("示例")

        #接收数据定时器
        self.timer_get=QTimer(self)
        self.timer_get.timeout.connect(self.timer_get_data)
        self.timer_get.start()

        # #发送数据定时器
        # self.timer_send=QTimer(self)
        # self.timer_send.timeout.connect(self.timer_send_data)
        # self.timer_send.start()      当前版本未加入定时功能

        self.ui.pushButton_3.clicked.connect(self.send_data)#实现发送数据按钮
        self.ui.pushButton_4.clicked.connect(self.clear_data)#实现清除数据按钮
        self.ui.pushButton.clicked.connect(self.clear_send)#实现清除发送数据

        self.ui.radioButton.clicked.connect(self.port_operate)

    def port_operate(self):
        if self.ui.radioButton.isChecked:
            self.ser.open()
        else:
            self.ser.close()


    def clear_send(self):
        pass

    
    def port_change(self):
        portx=self.ui.comboBox.currentText()  #端口
        bps=int(self.ui.comboBox_2.currentText()) #波特率
        bytesize=int(self.ui.comboBox_3.currentText())
        stopbits=int(self.ui.comboBox_4.currentText())
        parity=self.paritylist[int(self.ui.comboBox_5.currentIndex())]
        self.ser = serial.Serial(portx, bps, bytesize=bytesize, stopbits=stopbits, timeout=1,parity=parity)        

    def clear_data(self):
        self.ui.textEdit.clear()

    def send_data(self):
        # print(1)
        pass





    def timer_get_data(self):
        # 接收数据处理函数
        pass
    
    def timer_send_data(self):
        # 发送数据处理函数
        pass



def get_portlist(gui):
    #拉取窗口列表，加入到comboBox中
    port_list = list(serial.tools.list_ports.comports())
    for port in port_list:
        # print(type(port.name))
        gui.comboBox.addItem(port.name)

def main():
    app = QApplication(sys.argv)
    gui = lcomx()
    gui.show()
    sys.exit(app.exec())




if __name__ == '__main__':
    main()
