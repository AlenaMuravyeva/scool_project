import sys
from PyQt4 import QtCore, QtGui, uic
import uiserver2

class MainWindow(QtGui.QMainWindow, uiserver2.Ui_Form):
   def __init__(self):
      super().__init__()
      self.setupUi(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    
    # create the updating thread and connect
    # it's received signal to append
    # every received chunk of data/text will be appended to the text
    t = uiserver2.UpdateThread()
    t.update_graph_signal.connect(mw.update_graph)
    t.start()

    mw.show()
    app.exec_()
