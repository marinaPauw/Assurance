
import sys
import UI_MainWindow
import PyQt5
from PyQt5 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    global MainWindow
    MainWindow = UI_MainWindow.Ui_MainWindow()
    MainWindow.setupUi()
    MainWindow.show()
    sys.exit(app.exec_())
          