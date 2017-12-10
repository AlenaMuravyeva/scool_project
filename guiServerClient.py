import sys
from PyQt4 import QtCore, QtGui, uic
import uiserver2
import signal

class MainWindow(QtGui.QMainWindow, uiserver2.Ui_Form):
   def __init__(self):
      super().__init__()
      self.setupUi(self)


def handler(signum, frame):
    print("Pressed Ctrl+c .....")
    sys.exit(0)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    
    # create the updating thread and connect
    # it's received signal to append
    # every received chunk of data/text will be appended to the text
    signal.signal(signal.SIGINT, handler)
    t = uiserver2.UpdateThread()
    t.update_graph_signal.connect(mw.update_graph)
    t.start()

    mw.show()
    app.exec_()
