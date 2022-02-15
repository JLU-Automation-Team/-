# -*- coding: utf-8 -*-
import sys
import serial
import serial.tools.list_ports
import threading
import signal
import binascii

import strings_zh as strings

if sys.version_info.major == 2:
    import Tkinter as tk
    import tkMessageBox as msgbox
elif sys.version_info.major == 3:
    import tkinter as tk
    from tkinter import messagebox as msgbox


WINDOWSIZE = '710x510+50+50'

BAUDRATES = (1200, 2400, 4800, 9600, 14400, 19200, 38400, 57600, 115200)
BYTESIZES = (5, 6, 7, 8)
PARITIES = {'None': 'N', 'Even': 'E', 'Odd': 'O', 'Mark': 'M', 'Space': 'S'}
STOPBITS = (1, 1.5, 2)
BYTETYPES = ('1 Byte', '2 Bytes', '4 Bytes')

TIMEOUT = 0.015

font = ("宋体", 10, "normal")
font_text = ("Courier", 9, "normal")


def format_data(data):
        li = data.split(' ')
        result = []
        k = 0
        for each in li:
            if len(each) <= 2:
                result.append(each)

            if len(each) > 2:
                while k < len(each):
                    result.append(each[k: k + 2])
                    k = k + 2
                k = 0

        for i in range(len(result)):
            if len(result[i]) == 1:
                result[i] = '0' + result[i]

        return result


def getAvailabelSerialPort():
    available_ports = []
    coms = serial.tools.list_ports.comports()
    if coms is not None:
        for com in coms:
            if sys.platform == 'win32':
                available_ports.append(com.device)
            elif sys.platform == 'linux2':
                if com[2] != 'n/a':
                    available_ports.append(com[0])
    return tuple(available_ports)


if sys.platform == 'win32':
    PORTS = sorted(getAvailabelSerialPort(), key=lambda n: int(n[3:]))
else:
    PORTS = getAvailabelSerialPort()


class SerialAssistantGUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('%s v%s by %s' % (strings.APP_NAME, strings.APP_VER,
                                          strings.AUTHOR))
        self.root.geometry(WINDOWSIZE)
        self.root.resizable(width=False, height=False)

        self.__recv_area()
        self.__send_area()
        self.__cmd_area()
        self.__opt_area()

        self.root.mainloop()

    def __recv_area(self):
        recv_lframe = tk.LabelFrame(self.root,
                                    text=strings.recv_buf_text,
                                    height=250)
        recv_lframe.pack(fill=tk.X, padx=5)

        recv_optframe = tk.Frame(recv_lframe)
        recv_txtframe = tk.Frame(recv_lframe)
        recv_optframe.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)
        recv_txtframe.pack(fill=tk.Y, side=tk.RIGHT, padx=5, pady=5)

        self.recv_mode = tk.IntVar()
        self.recv_mode.set(0)
        recv_radbtn1 = tk.Radiobutton(recv_optframe,
                                      text=strings.text_mode_text,
                                      font=font,
                                      variable=self.recv_mode, value=0)
        recv_radbtn2 = tk.Radiobutton(recv_optframe,
                                      text=strings.hex_mode_text,
                                      font=font,
                                      variable=self.recv_mode, value=1)
        recv_clrbtn = tk.Button(recv_optframe, width=15,
                                text=strings.clear_recv_text,
                                font=font,
                                command=self.clear_received)
        recv_radbtn1.pack(anchor=tk.W)
        recv_radbtn2.pack(anchor=tk.W)
        recv_clrbtn.pack(fill=tk.X)

        self.recv_txtarea = tk.Text(recv_txtframe, height=15, width=74,
                                    font=font_text)
        self.recv_txtarea.pack(side=tk.LEFT, fill=tk.X)
        recv_scrbar = tk.Scrollbar(recv_txtframe)
        recv_scrbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recv_txtarea['yscrollcommand'] = recv_scrbar.set
        recv_scrbar['command'] = self.recv_txtarea.yview

    def __send_area(self):
        send_lframe = tk.LabelFrame(self.root,
                                    text=strings.send_buf_text,
                                    height=100)
        send_lframe.pack(fill=tk.X, padx=5)

        send_optframe = tk.Frame(send_lframe)
        send_txtframe = tk.Frame(send_lframe)
        send_optframe.pack(fill=tk.Y, side=tk.LEFT, padx=5, pady=5)
        send_txtframe.pack(fill=tk.Y, side=tk.RIGHT, padx=5, pady=5)

        self.send_mode = tk.IntVar()
        self.send_mode.set(0)
        send_radbtn1 = tk.Radiobutton(send_optframe,
                                      text=strings.text_mode_text,
                                      font=font,
                                      variable=self.send_mode, value=0)
        send_radbtn2 = tk.Radiobutton(send_optframe,
                                      text=strings.hex_mode_text,
                                      font=font,
                                      variable=self.send_mode, value=1)
        self.linebreak = tk.IntVar()
        if sys.platform == 'win32':
            self.linebreak.set(1)
        elif sys.platform == 'linux2':
            self.linebreak.set(0)
        send_chkbtn = tk.Checkbutton(send_optframe,
                                     text=strings.line_break_text,
                                     font=font,
                                     variable=self.linebreak)
        send_clrbtn = tk.Button(send_optframe,
                                text=strings.clear_send_text,
                                font=font,
                                width=15,
                                command=self.clear_sent)
        send_radbtn1.pack(anchor=tk.W)
        send_radbtn2.pack(anchor=tk.W)
        send_chkbtn.pack(anchor=tk.W)
        send_clrbtn.pack(fill=tk.X)

        self.send_txtarea = tk.Text(send_txtframe, height=7, width=74,
                                    font=font_text)
        self.send_txtarea.pack(side=tk.LEFT, fill=tk.X)
        send_scrbar = tk.Scrollbar(send_txtframe)
        send_scrbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.send_txtarea['yscrollcommand'] = send_scrbar.set
        send_scrbar['command'] = self.send_txtarea.yview

    def __cmd_area(self):
        cmd_frame = tk.Frame(self.root)
        cmd_frame.pack(fill=tk.X, padx=5, pady=5)
        cmd_btn = tk.Button(cmd_frame,
                            text=strings.send_btn_text,
                            font=font,
                            command=self.send_data)
        cmd_btn.pack(side=tk.LEFT)

    def __opt_area(self):
        opt_frame = tk.Frame(self.root)
        opt_frame.pack(fill=tk.X, padx=5, pady=5)

        # Serial port setting
        port_label = tk.Label(opt_frame,
                              text=strings.port_lbl_text,
                              font=font)

        self.port_var = tk.StringVar()
        self.port_var.set(strings.select_port)

        if len(PORTS) == 0:
            port_opmenu = tk.OptionMenu(opt_frame, self.port_var, '')
        else:
            port_opmenu = tk.OptionMenu(opt_frame, self.port_var, *PORTS)
        port_opmenu.config(anchor=tk.W,
                           width=10,
                           font=font)
        port_label.pack(side=tk.LEFT)
        port_opmenu.pack(side=tk.LEFT)

        # Baudrate setting
        brt_label = tk.Label(opt_frame,
                             text=strings.baud_lbl_text,
                             font=font)
        self.brt_var = tk.StringVar()
        self.brt_var.set(BAUDRATES[3])
        brt_opmenu = tk.OptionMenu(opt_frame, self.brt_var, *BAUDRATES)
        brt_opmenu.config(anchor=tk.W,
                          width=3,
                          font=font)
        brt_label.pack(side=tk.LEFT)
        brt_opmenu.pack(side=tk.LEFT)

        # Bytesize setting
        size_label = tk.Label(opt_frame,
                              text=strings.size_lbl_text,
                              font=font)
        self.size_var = tk.StringVar()
        self.size_var.set(BYTESIZES[3])
        size_opmenu = tk.OptionMenu(opt_frame, self.size_var, *BYTESIZES)
        size_opmenu.config(anchor=tk.W,
                           width=3,
                           font=font)
        size_label.pack(side=tk.LEFT)
        size_opmenu.pack(side=tk.LEFT)

        # Parity setting
        parity_label = tk.Label(opt_frame,
                                text=strings.parity_lbl_text,
                                font=font)
        self.parity_var = tk.StringVar()
        self.parity_var.set('None')
        parity_opmenu = tk.OptionMenu(opt_frame, self.parity_var,
                                      *PARITIES)
        parity_opmenu.config(anchor=tk.W,
                             width=3,
                             font=font)
        parity_label.pack(side=tk.LEFT)
        parity_opmenu.pack(side=tk.LEFT)

        # Stopbit setting
        stop_label = tk.Label(opt_frame,
                              text=strings.stopbit_lbl_text,
                              font=font)
        self.stop_var = tk.StringVar()
        self.stop_var.set(STOPBITS[0])
        stop_opmenu = tk.OptionMenu(opt_frame, self.stop_var, *STOPBITS)
        stop_opmenu.config(anchor=tk.W,
                           width=3,
                           font=font)
        stop_label.pack(side=tk.LEFT)
        stop_opmenu.pack(side=tk.LEFT)

        # Set buttons
        control_frame = tk.Frame(self.root, width=300)
        status_frame = tk.Frame(self.root, width=300)
        control_frame.pack(side=tk.LEFT)
        status_frame.pack(side=tk.RIGHT)

        start_btn = tk.Button(control_frame,
                              text=strings.start_port_text,
                              width=12,
                              command=self.start_port)
        close_btn = tk.Button(control_frame,
                              text=strings.close_port_text,
                              width=12,
                              command=self.close_port)
        start_btn.pack(side=tk.LEFT, padx=5)
        close_btn.pack(side=tk.LEFT, padx=5)
        self.state_lbl = tk.Label(control_frame, text='')
        self.state_lbl.pack(side=tk.LEFT, padx=5)

        # Status frame widgets
        send_cnt_label = tk.Label(status_frame,
                                  text=strings.send_lbl_text,
                                  font=font)
        self.send_cnt = tk.StringVar()
        self.send_cnt.set(self.TX)
        send_cnt_entry = tk.Entry(status_frame,
                                  textvariable=self.send_cnt, width=10,
                                  font=font,
                                  relief=tk.SUNKEN,
                                  state=tk.DISABLED,
                                  justify=tk.RIGHT)
        send_cnt_label.pack(side=tk.LEFT)
        send_cnt_entry.pack(side=tk.LEFT)

        recv_cnt_label = tk.Label(status_frame,
                                  text=strings.recv_lbl_text,
                                  font=font)
        self.recv_cnt = tk.StringVar()
        self.recv_cnt.set(self.RX)
        recv_cnt_entry = tk.Entry(status_frame,
                                  textvariable=self.recv_cnt, width=10,
                                  font=font,
                                  relief=tk.SUNKEN,
                                  state=tk.DISABLED,
                                  justify=tk.RIGHT)
        recv_cnt_label.pack(side=tk.LEFT)
        recv_cnt_entry.pack(side=tk.LEFT)

        clr_btn = tk.Button(status_frame,
                            text=strings.clear_btn_text,
                            font=font,
                            command=self.clear_count)
        clr_btn.pack()

    def clear_received(self):
        self.recv_txtarea.delete(0.0, tk.END)

    def clear_sent(self):
        self.send_txtarea.delete(0.0, tk.END)

    def clear_count(self):
        pass

    def start_port(self):
        pass

    def send_data(self):
        pass

    def recv_data(self):
        pass


class SerialAssistant(SerialAssistantGUI):

    portisopen = 0
    TX = 0
    RX = 0

    def __init__(self):
        super(SerialAssistant, self).__init__()

    def clear_count(self):
        self.RX = 0
        self.TX = 0
        self.send_cnt.set(self.RX)
        self.recv_cnt.set(self.TX)

    def start_port(self):
        port = self.port_var.get()
        baudrate = int(self.brt_var.get())
        bytesize = int(self.size_var.get())
        parity = PARITIES[self.parity_var.get()]
        stopbits = float(self.stop_var.get())

        try:
            self.s = serial.Serial(port=port,
                                   baudrate=baudrate,
                                   bytesize=bytesize,
                                   parity=parity,
                                   stopbits=stopbits,
                                   timeout=TIMEOUT)
        except serial.SerialException as e:
            msgbox.showerror("OpenError", e)
        except serial.SerialTimeoutException as e:
            msgbox.showerror("OpenError", e)
        else:
            self.portisopen = 1
            self.state_lbl.config(background='green',
                                  text=port + strings.opening)
            self.th = threading.Thread(target=self.recv_data)
            self.th.daemon = True
            self.th.start()

    def send_data(self):
        if self.portisopen:
            data_fmt = []
            data = self.send_txtarea.get(0.0, tk.END)

            if len(data) == 1:
                return

            if self.send_mode.get():
                if data[-1] == '\x0a':
                    data = data[0:-1]
                data_fmt = format_data(data)
                for each in data_fmt:
                    try:
                        x = binascii.a2b_hex(each)
                    except TypeError:
                        x = '\x00'

                    self.s.write(x)
                    self.TX += 1
            else:
                if data[-1] == '\n':
                    data = data[0:-1]
                if self.linebreak.get():
                    data = data.replace('\n', '\r\n')

                self.s.write(data.encode('utf-8'))
                self.TX += len(data)
            self.send_cnt.set(self.TX)
        else:
            msgbox.showerror("Error", "Port NOT open!")
            return

    def recv_data(self):
        while self.portisopen:
            data = self.s.read()
            if len(data) != 0:
                if self.recv_mode.get() == 1:
                    data = binascii.b2a_hex(data)
                    if sys.version_info.major == 3:
                        data += b' '
                    elif sys.version_info.major == 2:
                        data += ' '
                    self.RX += 1
                else:
                    self.RX += len(data)
            self.recv_cnt.set(self.RX)
            if data != '\x0d':
                self.recv_txtarea.insert(tk.END, data)
                self.recv_txtarea.see(tk.END)
        return

    def close_port(self):
        if self.portisopen:
            self.portisopen = 0
            self.s.close()
            self.state_lbl.config(background='red',
                                  text=self.port_var.get() + strings.closed)
        else:
            return

    def handler(self, signum, frame):
        self.portisopen = 0
        self.th.join()

    def __del__(self):
        self.close_port()
        signal.signal(signal.SIGINT, self.handler)


def main():
    SerialAssistant()


if __name__ == '__main__':
    main()