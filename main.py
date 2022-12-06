# Do not change the code framework - you could lose your grade
# Project 1 - Q2
# Name: Chenxi Dong
import argparse
import os
import heapq
import time

from visualization import vis


# You can use the heapq library in python standard libraries to implement priority queues.
# Check the Python doc of heapq.heappop and heapq.heappush at https://docs.python.org/3/library/heapq.html

class PacmanSolver:
    class state:
        # the class object for state
        def __init__(self, pacman, targets, prev, cost):
            self.pacman = pacman
            # the person's position
            self.targets = targets
            # the box's position
            self.cost = cost
            self.prev = prev

        def getPacman(self):
            return self.pacman

        def getTargets(self):
            return self.targets

        def getCost(self):
            return self.cost

        def getPrev(self):
            return self.prev

    def __loadInput(self, filename):
        f = open(filename, 'r')
        rawinput = []
        for line in f.readlines():
            rawinput.append(line.strip())
        return rawinput

    def heuristic(self, state, targets):
        theMin=0
        for target in targets:
            cur = abs(state.getPacman()[0] - target[0]) + abs(state.getPacman()[1] - target[1])
            if(cur<theMin):
                theMin=cur
        return theMin

    def solve(self, inputFilename):
        rawinput = self.__loadInput(inputFilename)
        finalMap=rawinput
        # for row in rawinput:
        #     print(row)
        numRows = len(rawinput)
        numCols = len(rawinput[0])
        map_Dict = dict()
        points=[]
        # copy the map into a hash map (dictionary)
        targets=[]
        for i in range(numRows):
            for j in range(numCols):
                if rawinput[i][j] == 'P':
                    pacman = [i, j]
                    map_Dict[str(i) +','+str(j)] = 'P'
                elif rawinput[i][j] == '.':
                    points.append([i,j])
                    map_Dict[str(i) + ','+ str(j)] = '.'
                    targets.append([i, j])
                else:
                    map_Dict[str(i) + ',' + str(j)] = rawinput[i][j]
                    continue

        # print(points)
        # dstLst=[]
        # for i in range(len(points)):
        #     for j in range(i,len(points)):
        #         dstLst.append((abs(points[i][0]-points[j][0])+abs(points[i][1]-points[j][1]), (points[i],points[j])))
        #         dstLst.sort(key=lambda x:x[0])
        # print(len(dstLst))
        shape = [numRows, numCols]
        map_Dict[str(pacman[0]) + str(pacman[1])] = ' '
        # modify the original map dictionary
        # change it later according to current state


        time = 1
        visited = dict()
        initialState = self.state(pacman,targets,pacman, 0)
        visited[str(initialState.getPacman()[0])+','+str(initialState.getPacman()[1])]=initialState
        aStarQueue = [(self.heuristic(initialState, targets), initialState.getCost(), time, initialState)]
        heapq.heapify(aStarQueue)
        # we have several standards to compare for the heap:
        #	1. heuristic
        #   2. the current state's cost
        #	3. the current time spent on going to this state
        # same comparison standard for the person's heap
        totalCost=0
        start=pacman
        path=[]
        reset=False
        while aStarQueue:
            reset=False
            cState = heapq.heappop(aStarQueue)[3]
            cost = cState.getCost()
            curTargets = cState.getTargets()
            curPacman =cState.getPacman()
            for i in range(4):
                if i == 0:
                    nextPacman = [curPacman[0], curPacman[1] + 1],
                elif i == 1:
                    nextPacman = [curPacman[0], curPacman[1] - 1],
                elif i == 2:
                    nextPacman = [curPacman[0]+1, curPacman[1]],
                else:
                    nextPacman = [curPacman[0]-1, curPacman[1]],

                nextPacman=nextPacman[0]
                if shape[0] > nextPacman[0] >= 0 and \
                        shape[1] > nextPacman[1] >= 0 and \
                        map_Dict[str(nextPacman[0]) +','+ str(nextPacman[1])] != '#' and \
                        str(nextPacman[0]) + ','+ str(nextPacman[1])  not in visited.keys():
                    if nextPacman in targets:
                        for target in targets:
                            if nextPacman==target:
                                foundStart=False
                                prevPacman=curPacman
                                tmp=[]
                                while not foundStart:
                                    if prevPacman==start:
                                        foundStart=True
                                    tmp.append(prevPacman)
                                    if map_Dict[str(prevPacman[0])+','+str(prevPacman[1])]=='.':
                                        map_Dict[str(prevPacman[0]) + ',' + str(prevPacman[1])]=' '
                                    prevState=visited[str(prevPacman[0])+','+str(prevPacman[1])]
                                    prevPacman=prevState.getPrev()
                                path=path+tmp[::-1]
                                targets.remove(target)
                                start = nextPacman
                                totalCost += cost+1
                                cost=0
                        visited=dict()
                        reset=True
                        initialState = self.state(start, targets, start, 0)
                        visited[str(start[0]) + ',' + str(start[1])] = initialState
                        if len(targets)==0:
                            # print(path)
                            ans = []
                            for i in range(numRows):
                                ans.append([])
                            count=0
                            for i in range(numRows):
                                for j in range(numCols):
                                    if[i,j] in path:
                                        if rawinput[i][j] == '.':
                                            ans[i].append('.')
                                        elif rawinput[i][j] == 'P':
                                            ans[i].append('P')
                                        else:
                                            ans[i].append('R')
                                    else:
                                        ans[i].append(rawinput[i][j])
                            # for row in ans:
                            #     print(row)
                            return totalCost, path, finalMap
                    if reset:
                        nState = self.state(nextPacman, curTargets, nextPacman, 0)
                        aStarQueue = [(self.heuristic(initialState, targets), initialState.getCost(), time, initialState)]
                        heapq.heapify(aStarQueue)
                    else:
                        nState = self.state(nextPacman, curTargets, curPacman, cost + 1)
                        heapq.heappush(aStarQueue, (self.heuristic(nState, targets) + nState.getCost(), nState.getCost(),
                                                time, nState))
                    visited[str(nextPacman[0]) +',' +str(nextPacman[1])] = nState
                    time += 1
                    if reset:
                        break
        return -1


if __name__ == '__main__':
    time1=time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=float)
    parser.add_argument('--f', type=int)
    args = parser.parse_args()
    test_file_number = args.f  # Change this to use different test files
    filename = 'game%d.txt' % test_file_number
    testfilepath = os.path.join('test', 'singleTarget', filename)
    Solver = PacmanSolver()
    res,path,map = Solver.solve(testfilepath)
    score=vis(path,map, args.t)
    #print(path)
    print('Your final score is %d' % (score+4))

    #print('Your answer is %d' % (res))
