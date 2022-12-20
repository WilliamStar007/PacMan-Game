# PacMan Game Pathfinding w/ A* Search Algorithm

import os
import heapq
import time
from visualization import vis


class PacmanSolver:
    class State:
        # the class object for state
        def __init__(self, pacman, targets, prev, score):
            # the person's position
            self.pacman = pacman
            # the food dots' position
            self.targets = targets
            # current player score
            self.score = score
            # previous state
            self.prev = prev

        def get_pacman(self):
            return self.pacman

        def get_targets(self):
            return self.targets

        def get_score(self):
            return self.score

        def get_prev(self):
            return self.prev

    def __load_input(self, filename):
        f = open(filename, 'r')
        rawinput = []
        for line in f.readlines():
            rawinput.append(line.strip())
        return rawinput

    def heuristic(self, pacman, tgt_pair):
        pac_x, pac_y = pacman[0], pacman[1]
        tgt_one, tgt_two = tgt_pair[0], tgt_pair[1]

        man_distance_one = abs(pac_x - tgt_one[0]) + abs(pac_y - tgt_one[1])
        man_distance_two = abs(pac_x - tgt_two[0]) + abs(pac_y - tgt_two[1])
        return tgt_one if man_distance_one < man_distance_two else tgt_two

    def solve(self, filename):
        def distance(tgt_list):
            distance_dict = dict()
            for idx, tgt_one in enumerate(tgt_list):
                for tgt_two in tgt_list[idx+1:]:
                    man_distance = abs(tgt_one[0]-tgt_two[0]) + abs(tgt_one[1]-tgt_two[1])
                    distance_dict[(tgt_one, tgt_two)] = man_distance
            return dict(sorted(distance_dict.items(), key=lambda x: x[1], reverse=True))

        def get_moves(pacman_loc):
            pac_x, pac_y = pacman_loc[0], pacman_loc[1]
            move_lst = list()
            if maze[pac_x + 1][pac_y] != '#':
                move_lst.append((pac_x + 1, pac_y))
            if maze[pac_x - 1][pac_y] != '#':
                move_lst.append((pac_x - 1, pac_y))
            if maze[pac_x][pac_y + 1] != '#':
                move_lst.append((pac_x, pac_y + 1))
            if maze[pac_x][pac_y - 1] != '#':
                move_lst.append((pac_x, pac_y - 1))
            return move_lst

        rawinput = self.__load_input(filename)
        rows = len(rawinput)
        cols = len(rawinput[0])
        maze = [[''] * cols] * rows

        pacman = tuple()
        target_lst = list()

        for i in range(rows):
            for j in range(cols):
                if rawinput[i][j] == 'P':
                    # pacman
                    pacman = (i, j)
                    maze[i][j] = 'P'
                elif rawinput[i][j] == '.':
                    # food dots
                    maze[i][j] = '.'
                    target_lst.append((i, j))
                else:
                    # wall
                    maze[i][j] = '#'
                    continue

        # init_state = self.State(pacman, targets, None, 0)
        distance_lst = distance(target_lst)
        target = self.heuristic(pacman, distance_lst.pop(0))

        return 0


if __name__ == '__main__':
    test_file_number = 3  # Change this to use different test files
    filename = 'game%d.txt' % test_file_number
    testfilepath = os.path.join('test', filename)
    Solver = PacmanSolver()
    Solver.solve(testfilepath)
    # res,path,map = Solver.solve(testfilepath)
    # score=vis(path,map)
    # print(path)
    # print('Your score is %d' % (score))
    # print('Your answer is %d' % (res))
