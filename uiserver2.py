# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiserver2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sqlite3
import re
import pylab
from matplotlib import mlab
import sqlite3
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

SERVER_DB_NAME = "stat.db"
SERVER_DB_CLIENTS_TABLE = "clients"
UI_FORM_NO_ACTIVE_CLIENT = "NA_CLIENT"


#Init DB
conn_db = sqlite3.connect("stat.db")
cursor = conn_db.cursor() 

#Init Qt4
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Form(object):
    active_client = UI_FORM_NO_ACTIVE_CLIENT
    def __init__(self):
        pass
        # self.ax1
        # self.ax2
        # self.ax3


    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1239, 868)
        self.gridLayoutWidget = QtGui.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1201, 781))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(25, 40))
        self.label.setMaximumSize(QtCore.QSize(250, 250))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.scrollArea = QtGui.QScrollArea(self.gridLayoutWidget)
        self.scrollArea.setMaximumSize(QtCore.QSize(250, 16777215))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 248, 731))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.scrollArea)
        self.verticalLayoutScroll = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayoutScroll.setAlignment(QtCore.Qt.AlignTop)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        font_2 = QtGui.QFont()
        font_2.setPointSize(16)
        font_2.setBold(False)
        font_2.setItalic(False)
        font_2.setWeight(75)
        self.label_2.setFont(font_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(self.gridLayoutWidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayoutWidget_2 = QtGui.QWidget(self.widget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(-1, -1, 941, 731))
        self.gridLayoutWidget_2.setObjectName(_fromUtf8("gridLayoutWidget_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout.addWidget(self.widget, 1, 1, 1, 1)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.addClients()
        self.addGraph()


    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "System load monitoring", None))
        self.label.setText(_translate("Form", "Clients", None))
        self.label_2.setText(_translate("Form", "Client Details", None))


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
    

    def addClients(self):
        for i in reversed(range(self.verticalLayoutScroll.count())): 
            self.verticalLayoutScroll.itemAt(i).widget().setParent(None)

        cursor.execute("SELECT client_id FROM clients")
        clients_id = cursor.fetchall()
        buttCompileGroup = QtGui.QButtonGroup(self)
        buttCompileGroup.setExclusive(True)
        for i in clients_id:
            button_name_st = str(i)
            button_name = re.findall('(\d+)', button_name_st)
            button_name = ''.join(button_name)
            print (button_name)
            button = QtGui.QPushButton(self.scrollAreaWidgetContents_3)
            self.verticalLayoutScroll.addWidget(button)
            button.setText(button_name)
            button.setCheckable(True)
            buttCompileGroup.addButton(button)
            button.clicked.connect(self.button_clicked)
            
            if button_name == self.active_client:
                button.click()

    def button_clicked(self):
        sender = self.sender()
        self.active_client = sender.text()
        cursor.execute("SELECT * FROM clients WHERE client_id = " + self.active_client)
        a = cursor.fetchall()
        cl_id = a[0][0]
        cl_ip = a[0][1]
        cl_port = a[0][2]
        s = "Client Details: ID={}; IP={}; Port={}".format(cl_id, cl_ip, cl_port)
        self.label_2.setText(_translate("Form", s , None))

        

    def addGraph(self):
         # a figure instance to plot on
        self.figure = Figure()
        self.figure.suptitle('Client Resource Usage')
        # self.figure.tight_layout()
        # self.figure.set_grid(True)

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout_2.addWidget(self.canvas)

        self.ax1 = self.figure.add_subplot(311)
        self.ax2 = self.figure.add_subplot(312)
        self.ax3 = self.figure.add_subplot(313)
 

    def build_cpu(self, xlist, ylist_us_cpu, ylist_system_cpu, ylist_idle_cpu):
        # self.ax1.set_title("CPU Usage")
        # self.ax1.set_xlabel("Sec")
        self.ax1.set_ylabel("CPU Usage, %")
        # self.ax1.hist(xlist, ylist_us_cpu, 'g', label='user')
        # self.ax1.hist(xlist, ylist_system_cpu, 'b:', label='system')
        # self.ax1.hist(xlist, ylist_idle_cpu, 'r--', label='idle')
        self.ax1.plot(xlist, ylist_us_cpu, 'g', label='user')
        self.ax1.plot(xlist, ylist_system_cpu, 'b:', label='system')
        self.ax1.plot(xlist, ylist_idle_cpu, 'r--', label='idle')
        legend = self.ax1.legend(loc='upper left', shadow=True)

    def build_memory(self, xlist, ylist_total_memory, ylist_available_memory, ylist_used_memory):
        # self.ax2.set_title("Memory Usage")
        # self.ax2.set_xlabel("Sec")
        self.ax2.set_ylabel("Memory Usage, Mb")
        self.ax2.plot(xlist, ylist_total_memory, 'g', label='total')
        self.ax2.plot(xlist, ylist_available_memory, 'r--', label='avail')
        self.ax2.plot(xlist, ylist_used_memory, 'b:', label='used')
        legend = self.ax2.legend(loc='upper left', shadow=True)
    
    def build_du(self, xlist, ylist_total_d_u, ylist_used_d_u, ylist_free_d_u):
        # self.ax3.set_title("Disk Usage")
        self.ax3.set_xlabel("Sec")
        self.ax3.set_ylabel("Disk Usage, Mb")
        self.ax3.plot(xlist, ylist_total_d_u, 'g', label='total')
        self.ax3.plot(xlist, ylist_used_d_u, 'b:', label='used')
        self.ax3.plot(xlist, ylist_free_d_u, 'r--', label='free')
        legend = self.ax3.legend(loc='upper left', shadow=True)


    #draft version without optimization: 3600 *9 sql requests
    def fetch_data_from_db (self, x, cur_time, cl_id, field_name):
        x1 = cur_time - x
        cursor.execute("SELECT " + field_name + " FROM stat_data WHERE client_id =" + cl_id + " AND stat_time =" + str(x1))
        y = cursor.fetchone()
        if type(y) == type(None):
            print ("return_cpu {}(): sqlite returned None type".format(field_name))
            return 0
        return (y[0])

    #first optimisation version: 3600 sql requests
    def fetch_all_data_from_db (self, x, cur_time, cl_id):
        x1 = cur_time - x
        cursor.execute("SELECT * FROM stat_data WHERE client_id =" + cl_id + " AND stat_time =" + str(x1))
        y = cursor.fetchone()

        if type(y) == type(None):
            z = []
            return z
        return (y)

    #second optimization version: 1 sql request!!!
    def fetch_range_time_data_from_db (self, xmin_time_back, xmax_time_back, cl_id):
        print("fetch_range_time_data_from_db(): xmax_time_back={} xmin_time_back={}".format(xmax_time_back, xmin_time_back))
        cursor.execute("SELECT * FROM stat_data WHERE client_id =" + cl_id + " AND stat_time BETWEEN " + str(xmax_time_back) + " AND " + str(xmin_time_back))
        y = cursor.fetchall()
        print("fetch_range_time_data_from_db(): len={}".format(len(y)))
        return (y)


    def update_clients(self):
        self.addClients()

    def update_graph(self):
        if self.active_client == UI_FORM_NO_ACTIVE_CLIENT:
            return

        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()

        xmin = 0
        xmax = 3600
        dx = 1

        cur_time = int(time.time())
        xmax_time_back = cur_time - xmax
        xmin_time_back = cur_time - xmin

        next_record = []
        ylist_us_cpu = []
        ylist_system_cpu = []
        ylist_idle_cpu = []
        ylist_total_memory = []
        ylist_available_memory = []
        ylist_used_memory = []
        ylist_total_d_u = []
        ylist_used_d_u = []
        ylist_free_d_u = []

        records = self.fetch_range_time_data_from_db(xmin_time_back, xmax_time_back, self.active_client)
        #for x in xlist:
            #next_record = self.fetch_all_data_from_db(x, cur_time, self.active_client)

        counted_records=0
        curx_time = xmax_time_back
        data_aproximation = 0
        for next_record in records:
            if curx_time > xmin_time_back:
                 break
            #print("Next record={}".format(next_record))
            #print("curx_time={}",curx_time)
            #print("counted_records={}".format(counted_records))
            for i in range(curx_time, next_record[1]+1):
                #print("i in range={}",i)
                if next_record[1] == i or data_aproximation == 1:
                    #print("update_graph: rec +++++++++++++++++")
                    ylist_us_cpu.append(next_record[2])
                    ylist_system_cpu.append(next_record[3])
                    ylist_idle_cpu.append(next_record[4])
                    ylist_total_memory.append(next_record[5])
                    ylist_available_memory.append(next_record[6])
                    ylist_used_memory.append(next_record[7])
                    ylist_total_d_u.append(next_record[8])
                    ylist_used_d_u.append(next_record[9])
                    ylist_free_d_u.append(next_record[10])
                    counted_records+=1
                    #data aproximation is requied to avoid droping graph to 0 if stat data
                    #was skiped because of time border condition overlap
                    if data_aproximation == 0:
                        data_aproximation = 1
                else:
                    #print("update_graph: not rec ---------------")
                    ylist_us_cpu.append(0)
                    ylist_system_cpu.append(0)
                    ylist_idle_cpu.append(0)
                    ylist_total_memory.append(0)
                    ylist_available_memory.append(0)
                    ylist_used_memory.append(0)
                    ylist_total_d_u.append(0)
                    ylist_used_d_u.append(0)
                    ylist_free_d_u.append(0)
                    counted_records+=1

            curx_time = next_record[1] + 1


        #-1 because db doesn't yet store last second when time is fetched therefore y will have less values
        xlist = mlab.frange (xmin, counted_records-1, dx) 

        self.ax1.invert_xaxis()
        self.ax2.invert_xaxis()
        self.ax3.invert_xaxis()
        ylist_us_cpu = ylist_us_cpu[::-1]
        ylist_system_cpu = ylist_system_cpu[::-1]
        ylist_idle_cpu = ylist_idle_cpu[::-1]
        ylist_total_memory = ylist_total_memory[::-1]
        ylist_available_memory = ylist_available_memory[::-1]
        ylist_used_memory = ylist_used_memory[::-1]
        ylist_total_d_u = ylist_total_d_u[::-1]
        ylist_used_d_u = ylist_used_d_u[::-1]
        ylist_free_d_u = ylist_free_d_u[::-1]


        self.build_cpu(xlist, ylist_us_cpu, ylist_system_cpu, ylist_idle_cpu)
        self.build_memory(xlist, ylist_total_memory, ylist_available_memory, ylist_used_memory)
        self.build_du(xlist, ylist_total_d_u, ylist_used_d_u, ylist_free_d_u)

      

        self.canvas.draw()

        self.update_clients()


class UpdateThread(QtCore.QThread):

    update_graph_signal = QtCore.pyqtSignal()

    def run(self):
        while True:
            self.sleep(5) # this would be replaced by real code, producing the new text...
            self.update_graph_signal.emit()    
