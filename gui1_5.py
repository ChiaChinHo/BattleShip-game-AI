# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
import copy, random
import Agent
import time

#variable definition
SINK = 3
HIT = 2
SHIP = 1
NONE = 0
MISS = -1
LOSE = -2

ERROR = -3

A = 0
B = 1
C = 2
D = 3
E = 4
F = 5
G = 6
H = 7
I = 8
J = 9

a = 0.6

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
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1750*a, 1000*a)

        self.tableWidget   = self.tableWidgetDef(Form, 100*a, 250*a, WIDTH*col*a + 23, HEIGHT*row*a + 27, "") 
        self.tableWidget_2 = self.tableWidgetDef(Form, 800*a, 250*a, WIDTH*col*a + 23, HEIGHT*row*a + 27, "_2") 
    
        self.textEdit   = self.textEditDef(Form, 100*a, 150*a, 161*a, 71*a, "")
        self.textEdit_2 = self.textEditDef(Form, 800*a, 150*a, 161*a, 71*a, "_2")
        self.textEdit_5 = self.textEditDef(Form, 1490*a, 380*a, 161*a, 71*a, "_5")
        self.textEdit_6 = self.textEditDef(Form, 1490*a, 550*a, 161*a, 71*a, "_6")
        
        self.pushButton   = self.pushButtonDef(Form, 1490*a, 270*a, 150*a, 46*a, "")
        self.pushButton_2 = self.pushButtonDef(Form, 1490*a, 210*a, 150*a, 46*a, "_2")

        self.label   = self.labelDef(Form, 100*a, 100*a, 121*a, 21*a, "")
        self.label_2 = self.labelDef(Form, 800*a, 100*a, 121*a, 21*a, "_2")
        self.label_5 = self.labelDef(Form, 1490*a, 350*a, 121*a, 21*a, "_5")
        self.label_6 = self.labelDef(Form, 1490*a, 500*a, 121*a, 21*a, "_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.pushButton_2.clicked.connect(self.initial)
        round1 = 0
        self.pushButton.clicked.connect(self.playgame)

    
    def tableWidgetDef(self, Form, x, y, w, h, s = ""): 
        tableWidget = QtGui.QTableWidget(Form)
        tableWidget.setGeometry(QtCore.QRect(x, y, w, h))
        #tableWidget.setObjectName(_fromUtf8("tableWidget"+s))

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
    
    def textEditDef(self, Form, x, y, w, h, s = ""):
        textEdit = QtGui.QTextEdit(Form)
        textEdit.setGeometry(QtCore.QRect(x, y, w, h))
        #textEdit.setObjectName(_fromUtf8("textEdit" + s))
        
        return textEdit

    def pushButtonDef(self, Form, x, y, w, h, s = ""):
        pushButton = QtGui.QPushButton(Form)
        pushButton.setGeometry(QtCore.QRect(x, y, w, h))
        #pushButton.setObjectName(_fromUtf8("pushButton"))

        return pushButton 

    def labelDef(self, Form, x, y, w, h, s = ""):
        label = QtGui.QLabel(Form)
        label.setGeometry(QtCore.QRect(x, y, w, h))
        #label.setObjectName(_fromUtf8("label" + s))
        
        return label

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))

        self.setWidget(self.tableWidget)
        self.setWidget(self.tableWidget_2)

        self.pushButton.setText(_translate("Form", "play", None))
        self.pushButton_2.setText(_translate("Form", "initialize", None))

        self.label.setText(_translate("Form", "player 1", None))
        self.label_2.setText(_translate("Form", "player 2", None))
        self.label_5.setText(_translate("Form", "winner", None))
        self.label_6.setText(_translate("Form", "rounds", None))

        self.textEdit_5.setHtml(_translate("Form", '' , None))
        self.textEdit_6.setHtml(_translate("Form", "0", None))

    def setWidget(self, tableWidget):
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
                sys.exit(-1)
            agent.append(a)

        global agentA
        global agentB

        agentA = agent[0] 
        agentB = agent[1]
        
    def playgame(self, Form):
        rounds = int(self.textEdit_6.toPlainText())
        rounds += 1
        self.textEdit_6.setHtml(_translate("Form", str(rounds), None))
        a1=1

        while True:
            r1 = t(agentB, agentA)
            posx, posy = r1[0]
            item = self.tableWidget.item(posx, posy)
            
            if r1[1] == MISS:
                item.setText(_translate("Form", "x", None))
                item.setTextColor(QtGui.QColor(0, 255, 0))
            else:
                item.setText(_translate("Form", "*", None))
                item.setTextColor(QtGui.QColor(255, 0, 0))
            if r1[1] == LOSE:
                self.textEdit_5.setHtml(_translate("Form", 'player2' , None))
            if r1[1] != HIT:
                break
            time.sleep(0.5)
        while True:
            r2 = t(agentA, agentB)
            posx, posy = r2[0]
            item = self.tableWidget_2.item(posx, posy)
            
            if r2[1] == MISS:
                item.setText(_translate("Form", "  x  ", None))
                item.setTextColor(QtGui.QColor(0, 255, 0))
            else:
                item.setText(_translate("Form", "  *  ", None))
                item.setTextColor(QtGui.QColor(255, 0, 0))
            if r2[1] == LOSE:
                self.textEdit_5.setHtml(_translate("Form", 'player1', None))
            if r2[1] != HIT:
                break
            time.sleep(0.5)

def t(agent1, agent2):
    result = ERROR
    while result == ERROR:
        pos = agent1.position()
        result, sink_ship, sink_pos = agent2.Hit_Or_Not(pos)
    agent1.Update(pos, result, sink_ship, sink_pos)
    return (pos, result)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    sys.exit(app.exec_())

