import copy, random
import Agent
import numpy as np

#variable definition
SINK = 3
HIT = 2
SHIP = 1
NONE = 0
MISS = -1
LOSE = -2

ERROR = -3

def Game(agent_name, STOP):
    agent_list = []

    for i in range(len(agent_name)):
        x = agent_name[i]
        if x == 's1':
            a = Agent.StrategicAgent1(unichr(65+i) + " (Stratgic method 1) ")
            agent_list.append(a)
        elif x == 's2':
            a = Agent.StrategicAgent2(unichr(65+i) + " (Stratgic method 2) ")
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
            pos, result = OneRound(agent1, agent2, agentA, STOP)
            if result != HIT:
                break
        if result == LOSE:
            print "Player" + agent1.Name() + " wins!"
            break
        
    #agentA.Print()
    print "Take round "+ str((round+1)/2) + " to WIN\n"
    if agent1==agentA:
        return np.array([[1, (round+1)/2], [0,0]])
    else:
        return np.array([[0,0], [1, (round+1)/2]])

def OneRound(agent1, agent2, agentA, STOP = False):
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
    return pos, result
    
