import copy, random
import Agent
import sys
import numpy as np

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
    STOP = False
    argv.pop(0)
    i = 0
    c = 1
    while i < len(argv):
        x = argv[i]
        x = x.lower()
        if x in ['s1', 's2', 'mc', 'dp', 'rd']:
            agent_name.append(x)
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
    print "Average steps of playerA takes to win:", float(win[0, 1])/float(win[0, 0]) if win[0, 0] != 0 else 0, '\n'
    print "Win percentage of playerB: ", float(win[1, 0])/c
    print "Average steps of playerB takes to win:", float(win[1, 1])/float(win[1, 0]) if win[1, 0] != 0 else 0


def Game(agent_name, STOP):
    agent_list = []

    for i in range(len(agent_name)):
        x = agent_name[i]
        if x == 's1':
            a = Agent.StrategicAgent1(unichr(65+i) + " (Strate method 1) ")
            agent_list.append(a)
        elif x == 's2':
            a = Agent.StrategicAgent2(unichr(65+i) + " (Strate method 2) ")
            agent_list.append(a)
        elif x == 'mc':
            a = Agent.MonteCarloAgent(unichr(65+i) + " (Monte Carlo) ")
            agent_list.append(a)
        elif x == 'dp':
            a = Agent.DynamicProgrammingAgent(unichr(65+i) + " (Dynamic Programming) ")
            agent_list.append(a)
        elif x == 'rd':
            a = Agent.Agent(unichr(65+i) + " (Random) ")
            agent_list.append(a)
        
    agentA = agent_list[0] 
    agentB = agent_list[1]

    agent1 = agentB
    agent2 = agentA
    round = 0
    while(1):
        round += 1
        agent1, agent2 = agent2, agent1
        
        while(1):
            while(1):
                pos = agent1.position()
                result, sink_ship, sink_pos = agent2.Hit_Or_Not(pos)
                
                if result != ERROR: 
                    break
            agent1.Update(pos, result, sink_ship, sink_pos)
            if STOP:
                print "PlayerA                                           PlayerB"
                agentA.Print()
                print "Player "+ agent1.Name()+ " shoot (" + unichr(65+pos[0]) + "," + str(pos[1]) +")!"
                r = 'MISS' if result == MISS else 'HIT'
                print "It is "+ r
                raw_input()
            if result != HIT:
                break
        if result == LOSE:
            print "Player" + agent1.Name() + " wins!"
            break
    agentA.Print()
    print "Take round "+ str((round+1)/2) + " to WIN\n"
    if agent1==agentA:
        return np.array([[1, (round+1)/2], [0,0]])
    else:
        return np.array([[0,0], [1, (round+1)/2]])
        

if __name__=="__main__":
	main()
