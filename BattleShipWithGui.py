import copy, random
import Agent
import sys
import numpy as np
import Gui
from GameRule import Game

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

def main():
    n = 0 
    agent_name = []
    argv = sys.argv
    GUI = True
    STOP = False
    argv.pop(0)
    i = 0
    c = 1
    while i < len(argv):
        x = argv[i]
        x = x.lower()
        if x in ['s1', 's2', 'mc', 'dp', 'rd']:
            agent_name.append(x)
        elif x == '-g':
            GUI = True
        elif x == '-s':
            STOP = True
        elif x == '-n':
            i += 1
            x = argv[i]
            x = x.lower()
            if isinstance(int(x), int):
                c = int(x)
            else:
                print "Command '-n' should be followed by an intager."
                print "ERROR command ("+argv[i]+") !!!"
                sys.exit(-1)
        else:
            print "ERROR command ("+argv[i]+") !!!"
            sys.exit(-1)
        i += 1

    if GUI:
        app, Form = Gui.app_Form()
        ui = Gui.Ui_Form()
        ui.setupUi(Form, app) 
        sys.exit(app.exec_())

    else:
        win = np.zeros((2,2))
        while len(agent_name) < 2:
            agent_name.append('rd')

        #win = [[# of playerA win, step of playerA], 
        #       [# of playerB win, step of playerB]]
        win = np.zeros((2,2))
        
        for i in range(c):
            print "#", i
            win += Game(agent_name, STOP)    

        print "Win percentage of playerA: ", float(win[0, 0])/c
        print "Average steps of playerA takes to win:", float(win[0, 1])/float(win[0, 0]) if win[0, 0] != 0 else 0
        print "Win percentage of playerB: ", float(win[1, 0])/c
        print "Average steps of playerB takes to win:", float(win[1, 1])/float(win[1, 0]) if win[1, 0] != 0 else 0

if __name__=="__main__":
	main()
