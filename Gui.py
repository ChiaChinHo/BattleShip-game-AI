# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
import Agent
import time
from GameRule import OneRound

#variable definition
SINK = 3
HIT = 2
SHIP = 1
NONE = 0
MISS = -1
LOSE = -2

ERROR = -3

a = 0.6
delay_time = 0.1

row = 10
col = 10

WIDTH = 50
HEIGHT = 50

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
    def setupUi(self, Form, app):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1850*a, 900*a)

        self.tableWidget   = self.tableWidgetDef(Form, 100*a, 250*a, WIDTH*col*a + 23, HEIGHT*row*a + 27) 
        self.tableWidget_2 = self.tableWidgetDef(Form, 750*a, 250*a, WIDTH*col*a + 23, HEIGHT*row*a + 27) 
    
        self.textEdit   = self.textEditDef(Form, 100*a, 150*a, 161*a, 71*a)
        self.textEdit_2 = self.textEditDef(Form, 750*a, 150*a, 161*a, 71*a)
        self.textEdit_5 = self.textEditDef(Form, 1400*a, 440*a, 400*a, 71*a)
        self.textEdit_6 = self.textEditDef(Form, 1400*a, 610*a, 161*a, 71*a)
        
        self.pushButton = self.pushButtonDef(Form, 1400*a, 210*a, 150*a, 46*a)
        self.pushButton_2 = self.pushButtonDef(Form, 1400*a, 270*a, 150*a, 46*a)
        self.pushButton_3 = self.pushButtonDef(Form, 1400*a, 330*a, 150*a, 46*a)

        self.label   = self.labelDef(Form, 100*a, 100*a, 121*a, 21*a)
        self.label_2 = self.labelDef(Form, 750*a, 100*a, 121*a, 21*a)
        self.label_5 = self.labelDef(Form, 1400*a, 410*a, 121*a, 21*a)
        self.label_6 = self.labelDef(Form, 1400*a, 560*a, 121*a, 21*a)


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton.clicked.connect(self.initial)
        round1 = 0
        self.pushButton_2.clicked.connect(self.playgame)
        self.pushButton_3.clicked.connect(self.ARound)

        self.app = app
        Form.show()
    
    def tableWidgetDef(self, Form, x, y, w, h): 
        tableWidget = QtGui.QTableWidget(Form)
        tableWidget.setGeometry(QtCore.QRect(x, y, w, h))

        tableWidget.setColumnCount(col)
        tableWidget.setRowCount(row)
        for i in range(row):
            item = QtGui.QTableWidgetItem()
            tableWidget.setVerticalHeaderItem(i, item)
            tableWidget.setRowHeight(i, HEIGHT*a)
        for i in range(col):
            item = QtGui.QTableWidgetItem()
            tableWidget.setHorizontalHeaderItem(i, item)
            tableWidget.setColumnWidth(i, WIDTH*a)
        for i in range(row):
            for j in range(col):
                item = QtGui.QTableWidgetItem()
                tableWidget.setItem(i, j, item)                
        return tableWidget
    
    def textEditDef(self, Form, x, y, w, h):
        textEdit = QtGui.QTextEdit(Form)
        textEdit.setGeometry(QtCore.QRect(x, y, w, h))
        
        return textEdit

    def pushButtonDef(self, Form, x, y, w, h):
        pushButton = QtGui.QPushButton(Form)
        pushButton.setGeometry(QtCore.QRect(x, y, w, h))

        return pushButton 

    def labelDef(self, Form, x, y, w, h):
        label = QtGui.QLabel(Form)
        label.setGeometry(QtCore.QRect(x, y, w, h))
        
        return label

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

        self.setWidget(Form, self.tableWidget)
        self.setWidget(Form, self.tableWidget_2)

        self.pushButton.setText(_translate("Form", "initialize", None))
        self.pushButton_2.setText(_translate("Form", "One Game", None))
        self.pushButton_3.setText(_translate("Form", "One Round", None))

        self.label.setText(_translate("Form", "Player A", None))
        self.label_2.setText(_translate("Form", "Player B", None))
        self.label_5.setText(_translate("Form", "winner", None))
        self.label_6.setText(_translate("Form", "rounds", None))

        self.textEdit_5.setHtml(_translate("Form", '' , None))
        self.textEdit_6.setHtml(_translate("Form", "0", None))

    def setWidget(self, Form, tableWidget):
        for i in range(10):
            item = tableWidget.verticalHeaderItem(i)
            item.setText(_translate("Form", unichr(65+i), None))
        for i in range(10):
            item = tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("Form", str(i), None))
        __sortingEnabled = tableWidget.isSortingEnabled()
        tableWidget.setSortingEnabled(False)
        self.clear(Form, tableWidget)
        tableWidget.setSortingEnabled(__sortingEnabled)

    def clear(self, Form, tableWidget):
        for i in range(10):
            for j in range(10):
                item = tableWidget.item(i,j)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setText(_translate("Form", "", None))            

    def initial(self, Form):
        self.clear(Form, self.tableWidget)
        self.clear(Form, self.tableWidget_2)
        self.textEdit_5.setHtml(_translate("Form", '' , None))
        self.textEdit_6.setHtml(_translate("Form", "0", None))

        player1 = self.textEdit.toPlainText()
        player2 = self.textEdit_2.toPlainText()

        agent = []
        for i in range(2):
            if i == 0:  x = player1
            else: x = player2
            if x == 's1':
                a = Agent.StrategicAgent1(unichr(65+i) + " (Strate method 1) ")
            elif x == 's2':
                a = Agent.StrategicAgent2(unichr(65+i) + " (Strate method 2) ")
            elif x == 'mc':
                a = Agent.MonteCarloAgent(unichr(65+i) + " (Monte Carlo) ")
            elif x == 'dp':
                a = Agent.DynamicProgrammingAgent(unichr(65+i) + " (Dynamic Programming) ")
            elif x == 'rd':
                a = Agent.Agent(unichr(65+i) + " (Random) ")
            else:
                print "Illegal command!!"
            agent.append(a)

        global agentA
        global agentB

        agentA = agent[0] 
        agentB = agent[1]
        
    def playgame(self, Form):
        result = None
        while result != LOSE:
            result = self.ARound(Form)
        
    def ARound(self, Form):
        #self.work.run(Form)
        rounds = int(self.textEdit_6.toPlainText())
        rounds += 1
        self.textEdit_6.setHtml(_translate("Form", str(rounds), None))
        while True:
            (posx, posy), result = OneRound(agentA, agentB, agentA)
            item = self.tableWidget_2.item(posx, posy)
            
            if result == MISS:
                item.setText(_translate("Form", "  x  ", None))
                item.setTextColor(QtGui.QColor(0, 255, 0))
            else:
                item.setText(_translate("Form", "  *  ", None))
                item.setTextColor(QtGui.QColor(255, 0, 0))
            self.app.processEvents()

            if result == LOSE:
                self.textEdit_5.setHtml(_translate("Form", "Player" + agentA.Name(), None))
                return result
            time.sleep(delay_time)
            if result != HIT:
                break

        while True:
            (posx, posy), result = OneRound(agentB, agentA, agentA)
            item = self.tableWidget.item(posx, posy)
            
            if result == MISS:
                item.setText(_translate("Form", "  x  ", None))
                item.setTextColor(QtGui.QColor(0, 255, 0))
            else:
                item.setText(_translate("Form", "  *  ", None))
                item.setTextColor(QtGui.QColor(255, 0, 0))
            self.app.processEvents()

            if result == LOSE:
                self.textEdit_5.setHtml(_translate("Form", "Player" + agentB.Name() , None))
                return result
            time.sleep(delay_time)
            if result != HIT:
                break

        return result

def app_Form():
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    Form.setStyleSheet("QWidget#Form {border-image: url(blured.jpg);}")
    return app, Form
