from socket import timeout
from timeit import Timer
import PyQt6

from sqlalchemy import false, true
import LCOMX_gui
import sys
import serial
import serial.tools.list_ports
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox,QStatusBar
from PyQt6.QtCore import QTimer ,QDateTime,Qt


class lcomx(QMainWindow):
    def __init__(self):
        self.now=QDateTime().currentDateTime()
        self.pull=None
        super().__init__()
        self.ser=None
        self.message = QMessageBox()
        self.ui = LCOMX_gui.Ui_LCOMX()
        self.ui.setupUi(self)
        self.paritylist = ["N", "O", "E"]
        self.get_portlist()
        # self.ui.textEdit.setPlainText("示例")

        self.statusBar().showMessage(self.now.toString(Qt.DateFormat.TextDate))#显示当前时间
        self.timer_bar=QTimer(self)
        self.timer_bar.timeout.connect(self.change_time_bar)
        self.timer_bar.start(1000)

        


        # 接收数据定时器
        self.timer_get = QTimer(self)
        self.timer_get.timeout.connect(self.timer_get_data)
        self.timer_get.start(1)

        #检测串口是否存在
        self.timer_test = QTimer(self)
        self.timer_test.timeout.connect(self.test_port)
        self.timer_test.start(100)

        # #发送数据定时器
        # self.timer_send=QTimer(self)
        # self.timer_send.timeout.connect(self.timer_send_data)
        # self.timer_send.start()      当前版本未加入定时功能

        self.ui.pushButton_3.clicked.connect(self.send_data)  # 实现发送数据按钮
        self.ui.pushButton_4.clicked.connect(self.clear_data)  # 实现清除数据按钮
        self.ui.pushButton.clicked.connect(self.clear_send)  # 实现清除发送数据

        self.ui.radioButton.clicked.connect(self.port_operate)  # 实现串口操作

        self.ui.radioButton_huiche.clicked.connect(self.add_huiche)  # 实现回车自动添加
        self.ui.radioButton_huiche.setChecked(True)  # 默认发送回车
        self.addhuiche = True

        self.ui.pushButton_2.clicked.connect(self.get_portlist)#实现了拉取串口列表
        #改变串口属性时发生相应变化
        self.ui.comboBox.activated.connect(self.port_change)
        self.ui.comboBox_2.activated.connect(self.port_change)
        self.ui.comboBox_3.activated.connect(self.port_change)
        self.ui.comboBox_4.activated.connect(self.port_change)
        self.ui.comboBox_5.activated.connect(self.port_change)

    def change_time_bar(self):
        self.now=QDateTime().currentDateTime()
        self.statusBar().showMessage(self.now.toString(Qt.DateFormat.TextDate))#显示当前时间

    def test_port(self):

                # 拉取窗口列表，加入到comboBox中
        port_list = list(serial.tools.list_ports.comports())

        if port_list == []:
            self.ui.radioButton.setChecked(False)
            if self.ser is not None:
                self.ser.close
            self.ui.comboBox.clear()
            if self.pull==False:
                self.pull=True
                self.ser=None
                self.message.information(self,"通知","串口已拔出")
            
        else:
            pass

    def add_huiche(self):
        if self.ui.radioButton_huiche.isChecked():
            self.addhuiche = True
        else:
            self.addhuiche = False

    def port_operate(self):
        if self.ui.radioButton.isChecked():
            if self.ser:
                if not self.ser.isOpen():
                    self.ser.open()
        else:
            if self.ser:
                if self.ser.isOpen():
                    self.ser.close()
        pass

    def clear_send(self):
        self.ui.textEdit_3.clear()

    def port_change(self):
        try:
            if self.ser:
                if self.ser.isOpen():
                    self.ser.close()
            portx = self.ui.comboBox.currentText()  # 端口
            if portx != None:
                bps = int(self.ui.comboBox_2.currentText())  # 波特率
                bytesize = int(self.ui.comboBox_4.currentText())
                stopbits = int(self.ui.comboBox_3.currentText())
                parity = self.paritylist[int(self.ui.comboBox_5.currentIndex())]
                self.ser = serial.Serial(
                    portx, bps, bytesize=bytesize, stopbits=stopbits, timeout=5, parity=parity)
                self.ui.radioButton.setChecked(True)
                self.pull=False
            else:
                self.message.information(self, "消息", "无串口")

        except serial.serialutil.SerialException:
            self.message.information(self, "消息", "串口无法打开")

    def clear_data(self):
        self.ui.textEdit.clear()

    def send_data(self):
        # print(1)
        data=self.ui.textEdit_3.toPlainText()
        
        data=data.encode('gbk')
        if self.addhuiche:
            data=data+"\r\n".encode("gbk")
        self.ser.write(data)
        pass

    def timer_get_data(self):
        # 接收数据处理函数
        if self.ser is not None:
            if self.ser.isOpen():
                try:
                    num = self.ser.inWaiting()#获取输入缓冲区的剩余字节数
                except:
                    self.port_close()
                    return None
                if num > 0:
                    data = self.ser.read(num)
                    try:
                        data=data.decode("gbk")
                    except UnicodeDecodeError:
                        data="解码失败\r\n"
                    self.ui.textEdit.insertPlainText(data)
            


    def port_close(self):
        if self.ser:
            if self.ser.isOpen():
                self.ser.close()
                self.ui.radioButton.setChecked(False)

    def port_open(self):
        if self.ser:
            if not self.ser.isOpen():
                self.ser.open()
                self.ui.radioButton.setChecked(True)


    def timer_send_data(self):
        # 发送数据处理函数
        pass

    def get_portlist(self):
        # 拉取窗口列表，加入到comboBox中
        self.ui.comboBox.clear()
        if self.ser:
            if self.ser.isOpen():
                self.ser.close()


        port_list = list(serial.tools.list_ports.comports())

        if port_list == []:
            self.ui.radioButton.setChecked(False)
        else:
            for port in port_list:
                # print(type(port.name))
                self.ui.comboBox.addItem(port.name)
            self.port_change()


def main():
    app = QApplication(sys.argv)
    gui = lcomx()
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
