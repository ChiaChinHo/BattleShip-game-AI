import numpy as np
from termcolor import colored
import random

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

class Agent(object):
    def __init__(self, name):
        self.ShipPosition = np.zeros(shape = (5,5), dtype=[('x', 'i4'), ('y', 'i4')]) # record ship position
        self.myGraph = self.Random() # 10*10, 5 ships random arranged 
        self.otherGraph = np.zeros((10, 10), dtype = int)
        self.ShipNum = 2+3+3+4+5
        self.name = name      
        self.ShipHit = [(5,0), (4,0), (3,0), (3,0), (2,0)] # record ship_sunk on otherGraph

    # 10*10, 5 ships random arranged 
    def Random(self):
        ships = [("Carrier",5), ("Battleship",4), ("Submarine",3), ("Cruiser",3), ("Destroyer",2)]
        graph = np.zeros((10, 10), dtype = int) # 10*10, NONE
        n = 0
        for ship in ships:
            ship_len = ship[1]
            valid = False
            while(not valid): # check can place or not
                row, col = self.randomposition()
                tmp = random.randint(0, 1)
                if tmp == 0:
                    ori = "v"
                else:
                    ori = "h"
                valid = self.check_valid(graph, row, col, ship_len, ori)

            if ori == "v": 
                for i in range(ship_len):
                    graph[row+i][col] = SHIP
                    self.ShipPosition[n][i] = (row+i, col)
            elif ori == "h":
                for i in range(ship_len):
                    graph[row][col+i] = SHIP
                    self.ShipPosition[n][i] = (row, col+i)
            n+=1

        return graph

    def check_valid(self, graph, row, col, ship_len, ori):
        if ori == "v":
            if row + ship_len > 10:
                return False
            for i in range(ship_len):
                if graph[row + i][col] != NONE:
                    return False
        
        elif ori == "h":
            if col + ship_len > 10:
                return False
            for i in range(ship_len):
                if graph[row][col + i] != NONE:
                    return False  
        return True          
 
    def Name(self):
	    return self.name	

    '''
    if there is ship on pos, return HIT
    if all ship is sunk, return LOSE
    if there is no ship on pos, return MISS
    else return ERROR
    '''
    def Hit_Or_Not(self, pos):
        row, col = pos
        sink_ship = -1  # which ship is sunk
        sink_pos = []  # sunk ship position

        if self.myGraph[row][col] == SHIP:
            result = HIT
            self.myGraph[row][col] = HIT
            self.ShipNum -= 1

            for i in range(5):
                s = True
                tmp = False
                shipLen = self.ShipHit[i][0]
                shipPos = self.ShipPosition[i]

                for j in range(shipLen):
                    if shipPos[j][0] == row and shipPos[j][1] == col:
                        tmp = True

                if(tmp == True):
                    for j in range(shipLen):
                        Row, Col = shipPos[j]
                        if(self.myGraph[Row][Col] != HIT):
                            s = False
                            break

                if(tmp == True and s == True):
                    sink_pos = self.ShipPosition[i]
                    sink_ship = i
                    break

        elif self.myGraph[row][col] == NONE:
            result = MISS
            self.myGraph[row][col] = MISS

        else : result = ERROR

        if self.ShipNum <= 0:
            result = LOSE

        return result, sink_ship, sink_pos
    
    def randomposition(self):
        row = random.randint(A, J)
        col = random.randint(0, 9)
        return (row, col)

    def position(self):
        return self.randomposition()

    '''
    Update otherGraph[pos] = state
    state = HIT or MISS
    sink = -1 mean ship not sunk
    '''
    def Update(self, pos, state, sink_ship, sink_pos):
        row, col = pos
        self.otherGraph[row][col] = state
        
        if state == HIT and sink_ship != -1:
            shipLen = self.ShipHit[sink_ship][0]
            self.ShipHit[sink_ship] = (shipLen, 1)
            for row, col in sink_pos[: shipLen]:
                self.otherGraph[row][col] = SINK
        
    def Print(self):
        print 
        print '   ',
        for i in range(10): print str(i)+' ',
        for i in range(10): print ' ',
        for i in range(10): print str(i)+' ',
        print '\n'
        for t in range(self.myGraph.shape[0]):
            print str(unichr(t+65))+"  ", 
            x = self.myGraph[t]
            for i in x:
                self.pp(i)
            for i in range(8): print ' ',
            x = self.otherGraph[t]
            print str(unichr(t+65))+"  ", 
            for i in x:
                self.pp(i)
            print '\n'
        
    def pp(self, i):
        if i == SHIP:
            print colored('o ', 'white'),
        elif i == NONE:
            print colored('o ', 'white'),
        elif i == MISS:
            print colored('x ', 'green'),
        else : print colored('* ', 'red'), # i == HIT or SINK

class StrategicAgent1(Agent):

    def position(self):
        #if boat is hit, and the adjacent position has not been hit,hit it
        pro_list = []

        for m in range(10):
            for n in range(10):
                if n < 9:
                    if (self.otherGraph[m][n] == HIT ) and (self.otherGraph[m][n+1] == NONE):
                        pro_list.append((m, n+1))
                    if (self.otherGraph[m][n+1] == HIT) and (self.otherGraph[m][n] == NONE):
                        pro_list.append((m, n))
            
                if m < J:
                    if(self.otherGraph[m][n] == HIT) and (self.otherGraph[m+1][n] == NONE):
                        pro_list.append((m+1, n))
                    if (self.otherGraph[m+1][n] == HIT) and (self.otherGraph[m][n] == NONE):
                        pro_list.append((m, n))

        if len(pro_list) == 0:
            c = 0
            while True:
                row = random.randint(A, J)
                col = random.randint(0, 9)
                #hit on the diagonal position
                if (self.otherGraph[row][col] == NONE):
                    if (row + col) % 2 == 0:
                        break
                    else:
                        c = c+1
                        #try 6 times 
                        if c == 6:
                           break                        
        else:
            row, col = random.choice(pro_list)
        return (row, col)
    
class StrategicAgent2(Agent):

    def position(self):
        pro_list = []
                
        for m in range(10):
            for n in range(10):
                if n < 9:
                    if (self.otherGraph[m][n] == HIT ) and (self.otherGraph[m][n+1] == NONE):
                        pro_list.append((m, n+1))
                    if (self.otherGraph[m][n+1] == HIT) and (self.otherGraph[m][n] == NONE):
                        pro_list.append((m, n))
            
                if m < J:
                    if(self.otherGraph[m][n] == HIT) and (self.otherGraph[m+1][n] == NONE):
                        pro_list.append((m+1, n))
                    if (self.otherGraph[m+1][n] == HIT) and (self.otherGraph[m][n] == NONE):
                        pro_list.append((m, n))

        if len(pro_list) == 0:
            bigship = self.UpdateBigShip()
            #Try to get the biggest ship, to get this one the player only have to check every fifth square (if the big one has 5 squares).
            grid = np.ones((10, 10), dtype = int)
            grid *= 4
            for m in range(10):
                for n in range(10):
                    if self.otherGraph[m][n] != NONE:
                        grid[m][n] = 0 
                        self.ModifyGrid(grid, m, n, bigship)
            c = np.max(grid)
            index = [i for i in range(10*10) if grid[i/10][i%10] == c]
            i = random.choice(index)
            row, col = (i/10, i%10)
        else:
            row, col = random.choice(pro_list)

        return (row, col)
        
    def ModifyGrid(self, grid, m, n, bigship):
        if self.otherGraph[m, n] != MISS: return

        for i in range(1, bigship):
            row, col = m-i, n
            if row < A: break
            if self.otherGraph[row][col] != NONE: break
            if i == bigship-1:
                grid[row][col] += 1
            else: grid[row][col] -= 1

        for i in range(1, bigship):
            row, col = m+i, n
            if row > J: break
            if self.otherGraph[row][col] != NONE: break
            if i == bigship-1:
                grid[row][col] += 1
            else: grid[row][col] -= 1

        for i in range(1, bigship):
            row, col = m, n-i
            if col < 0: break
            if self.otherGraph[row][col] != NONE: break
            if i == bigship-1:
                grid[row][col] += 1
            else: grid[row][col] -= 1

        for i in range(1, bigship):
            row, col = m, n+i
            if col > 9: break
            if self.otherGraph[row][col] != NONE: break
            if i == bigship-1:
                grid[row][col] += 1
            else: grid[row][col] -= 1

        for row, col in [(m-1, n-1), (m-1, n+1), (m+1, n-1), (m+1, n+1)]:
            if row < A or row > J or col < 0 or col > 9: continue
            if self.otherGraph[row][col] == NONE:
                grid[row][col] += 1

    '''
    Find the remind biggest ship 
    '''
    def UpdateBigShip(self):
        s = 0
        for x in self.ShipHit:
            if x[1] == 0 and x[0] > s:
                s = x[0]
        return s+1

class MonteCarloAgent(Agent):

    def __init__(self, name):
        self.__guessGraph = []
        self.OtherShipPos = np.zeros(shape = (5,5), dtype=[('x', 'i4'), ('y', 'i4')])
        self.step = 25 
        self.x = 2
        Agent.__init__(self,name)
        self.__numBoards =  self.step ** self.x
        self.Random_boards()

    def Random_boards(self, sink_ship = -1, sink_pos = []):
        # random certain number of boards consistent with current one
        while len(self.__guessGraph) < self.__numBoards:
            valid_board = False
            while(not valid_board):
                tmp = self.Place_ship(sink_ship, sink_pos)
                valid_board = self.check_board(tmp)
            self.__guessGraph.append(tmp)    

    def Place_ship(self,sink_ship, sink_pos):
        ships = [("Carrier",5), ("Battleship",4), ("Submarine",3), ("Cruiser",3), ("Destroyer",2)]
        graph = np.zeros((10, 10), dtype = int) # 10*10, NONE

        if(not sink_ship == -1):
            self.ShipHit[sink_ship] = (self.ShipHit[sink_ship][0], 1)
            for i in range(self.ShipHit[sink_ship][0]):
                self.OtherShipPos[sink_ship][i] = sink_pos[i]

        for i in range(4,-1,-1):
            if(self.ShipHit[i][1] == 1):
                ships.pop(i)
                for j in range(self.ShipHit[i][0]):
                    row, col = self.OtherShipPos[i][j]
                    graph[row][col] = SHIP

        while ships != []:
            ship = random.choice(ships)
            ships.remove(ship)
            ship_len = ship[1]
            valid = False

            # record hit square
            hit = [(i/10, i%10) for i in range(100) if self.otherGraph[i/10][i%10] == HIT and graph[i/10][i%10] == NONE]
            # record none square
            none = [(i/10, i%10) for i in range(100) if self.otherGraph[i/10][i%10] == NONE and graph[i/10][i%10] == NONE]

            # check can place or not
            while(not valid): 
                h = 0 # record placed in hit or none
                n = 0
                while(hit != []):
                    row, col = random.choice(hit)
                    if(graph[row][col] == NONE):
                        h = 1
                        break
                    else:
                        hit.remove((row,col))
                if(hit == [] and none != []):
                    while(True):
                        row, col = random.choice(none)
                        if(graph[row][col] == NONE):
                            n = 1
                            break
                        else:
                            none.remove((row,col))
                if(none == []):
                    break

                tmp = random.randint(0, 1)
                if tmp == 0:
                    ori = "v"
                    valid,tmp2 = self.is_valid(graph, row, col, ship_len, ori, valid)
                    if(valid == True):
                        for i in range(ship_len):
                            graph[row + i - tmp2][col] = SHIP
                    elif(valid == False):
                        ori = "h"
                        valid,tmp2 = self.is_valid(graph, row, col, ship_len, ori, valid)
                        if(valid == True):
                            for i in range(ship_len):
                                graph[row][col +i - tmp2] = SHIP
                else:
                    ori = "h"
                    valid,tmp2 = self.is_valid(graph, row, col, ship_len, ori, valid)
                    if(valid == True):
                        for i in range(ship_len):
                            graph[row][col +i - tmp2] = SHIP
                    elif(valid == False):
                        ori = "v"
                        valid,tmp2 = self.is_valid(graph, row, col, ship_len, ori, valid)
                        if(valid == True):
                            for i in range(ship_len):
                                graph[row + i - tmp2][col] = SHIP

                if(valid == False):
                    if(h == 1):
                        hit.remove((row, col))
                    elif(n == 1):
                        none.remove((row,col))

        return graph

    # check each ship can be placed in the chosen position
    def is_valid(self, graph, row, col, ship_len, ori, valid):
        ship_pos = list(range(ship_len))
        while(valid == False):
            if(ship_pos == []):
                pos = 0
                break
            valid = True
            pos = random.choice(ship_pos) 
            if ori == "v":
                if(row + ship_len - pos > 10 or row - pos < 0):
                    valid =  False
                else:
                    for i in range(ship_len):
                        if(graph[row + i - pos][col] != NONE or self.otherGraph[row + i - pos][col] == MISS):
                            valid =  False
            elif ori == "h":
                if(col + ship_len - pos > 10 or col - pos < 0):
                    valid = False
                else:
                    for i in range(ship_len):
                        if(graph[row][col + i - pos] != NONE or self.otherGraph[row][col + i - pos] == MISS):
                            valid = False
            if(valid == False):
                ship_pos.remove(pos)

        return valid, pos

    # check if randomBoard consistent with otherGraph
    def check_board(self, randomBoard):
        for i in range(10):
            for j in range(10):
                if(self.otherGraph[i][j] == HIT and randomBoard[i][j] != SHIP):
                    return False
                if(self.otherGraph[i][j] == MISS and randomBoard[i][j] == SHIP):
                    return False
        return True

    def position(self):
        sumGraph = np.sum(np.array(self.__guessGraph), axis = 0)

        # don't choose grid already hit
        for i in range(10):
            for j in range(10):
                if(self.otherGraph[i][j] != NONE):  
                    sumGraph[i][j] = 0

        c = np.max(sumGraph)
        index = [i for i in range(10*10) if sumGraph[i/10][i%10] == c]
        max_index = random.choice(index) 
        row, col = max_index/10, max_index%10

        return (row, col)

    def Update(self, pos, state, sink_ship, sink_pos):
        row, col = pos
        self.otherGraph[row][col] = state

        # delete board not consistent
        delete = []
        for i in range(len(self.__guessGraph)): 
            if(state == HIT and self.__guessGraph[i][row][col] != SHIP):
                delete.append(i)
            if(state == MISS and self.__guessGraph[i][row][col] == SHIP):
                delete.append(i)
        while(delete != []):
            j = delete.pop()
            del self.__guessGraph[j]   

        self.__numBoards = self.step ** self.x 
        if state == HIT:
            self.step -= 1 

        self.Random_boards(sink_ship, sink_pos)

class DynamicProgrammingAgent(Agent):

    def __init__(self, name):
        self.rowgrid = self.row()
        self.colgrid = self.col()
        Agent.__init__(self, name)

    def position(self):
        #grid = self.rowgrid + self.colgrid
        grid = np.multiply(self.rowgrid, self.colgrid)
        c = np.max(grid)
        index = [i for i in range(10*10) if grid[i/10, i%10] == c]
        i = random.choice(index) 
        return (i/10, i%10)

    def row(self):
        a = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                a[i, j] = self.Min(-1, 10, j, NONE, NONE)
        return a

    def col(self):
        a = np.zeros((10, 10))
        for i in range(10):
            for j in range(10):
                a[i, j] = self.Min(-1, 10, i, NONE, NONE)
        return a

    def Min(self, low, high, i, low_state, high_state):
        if low_state == HIT:
            low_state = SHIP
        else: low_state = NONE

        if high_state == HIT:
            high_state = SHIP
        else: high_state = NONE

        if low_state == NONE and high_state == NONE:
            return min(i - low , high - i)
        if low_state == SHIP and high_state == NONE:
            return high - i + 1
        if low_state == NONE and high_state == SHIP:
            return i-low + 1
        return 7 - min(i-low, high-i)

    '''
    state = HIT or MISS
    '''
    def Update(self, pos, state, sink_ship, sink_pos):
        row, col = pos
        self.otherGraph[row][col] = state
        
        if state == HIT and sink_ship != -1:
            shipLen = self.ShipHit[sink_ship][0]
            self.ShipHit[sink_ship] = (shipLen, 1)
            for r, c in sink_pos[: shipLen]:
                self.otherGraph[r][c] = SINK
        self.rowgrid[row, col] = 0
        self.colgrid[row, col] = 0

        #update self.rowgrid
        index = [i for i in range(10) if self.otherGraph[row][i] != NONE]
        low = -1
        c = 0 
        high = index[c]
        low_state = NONE
        high_state = self.otherGraph[row][index[c]]
        
        for i in range(10):
            if i == high:
                low, low_state = high, high_state
                if (c+1) < len(index): 
                    c += 1
                    high, high_state = index[c], self.otherGraph[row][index[c]]
                else:
                    high, high_state = 10, NONE
                
            else:
                self.rowgrid[row][i] = self.Min(low, high, i, low_state, high_state)

        #update self.colgrid
        index = [i for i in range(10) if self.otherGraph[i][col] != NONE]
        low = -1
        c = 0 
        high = index[c]
        low_state = NONE
        high_state = self.otherGraph[index[c]][col]
        
        for i in range(10):
            if i == high:
                low, low_state = high, high_state
                if (c+1) < len(index): 
                    c += 1
                    high, high_state = index[c], self.otherGraph[index[c]][col]
                else:
                    high, high_state = 10, NONE
                
            else:
                self.colgrid[i][col] = self.Min(low, high, i, low_state, high_state)
        

