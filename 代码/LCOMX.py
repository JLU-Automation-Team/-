import LCOMX_gui
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow


class lcomx(QMainWindow):
    def __init__(self):
        super().__init__()
        ui=LCOMX_gui.Ui_LCOMX()
        ui.setupUi(self)


def main():
    app = QApplication(sys.argv)
    gui = lcomx()
    gui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
