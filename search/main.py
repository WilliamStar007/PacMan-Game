import argparse
import heapq
import os

from visualization import vis


class PacmanSolver:
    class State:
        # the class object for state
        def __init__(self, pacman, targets, prev, cost):
            # pacman position
            self.pacman = pacman
            # dots positions
            self.targets = targets
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

    def __loadInput(self, file_name):
        f = open(file_name, 'r')
        raw_input = []
        for line in f.readlines():
            raw_input.append(line.strip())
        return raw_input

    def heuristic(self, state, targets):
        cost = 0
        for target in targets:
            cur = abs(state.getPacman()[0] - target[0]) + abs(state.getPacman()[1] - target[1])
            if cur < cost:
                cost = cur
        return cost

    def solve(self, input_filename):
        raw_input = self.__loadInput(input_filename)
        final_map = raw_input
        num_rows = len(raw_input)
        num_cols = len(raw_input[0])
        map_dict = dict()
        points = []
        targets = []
        for i in range(num_rows):
            for j in range(num_cols):
                if raw_input[i][j] == 'P':
                    pacman = [i, j]
                    map_dict[str(i) + ',' + str(j)] = 'P'
                elif raw_input[i][j] == '.':
                    points.append([i, j])
                    map_dict[str(i) + ',' + str(j)] = '.'
                    targets.append([i, j])
                else:
                    map_dict[str(i) + ',' + str(j)] = raw_input[i][j]
                    continue

        shape = [num_rows, num_cols]
        map_dict[str(pacman[0]) + str(pacman[1])] = ' '

        steps = 1
        visited = dict()
        initial_state = self.State(pacman, targets, pacman, 0)
        visited[str(initial_state.getPacman()[0]) + ',' + str(initial_state.getPacman()[1])] = initial_state
        aStarQueue = [(self.heuristic(initial_state, targets), initial_state.getCost(), steps, initial_state)]
        heapq.heapify(aStarQueue)

        total_cost = 0
        start = pacman
        path = []
        while aStarQueue:
            reset = False
            cur_state = heapq.heappop(aStarQueue)[3]
            cost = cur_state.getCost()
            cur_targets = cur_state.getTargets()
            cur_pacman = cur_state.getPacman()
            for i in range(4):
                if i == 0:
                    next_pacman = [cur_pacman[0], cur_pacman[1] + 1],
                elif i == 1:
                    next_pacman = [cur_pacman[0], cur_pacman[1] - 1],
                elif i == 2:
                    next_pacman = [cur_pacman[0] + 1, cur_pacman[1]],
                else:
                    next_pacman = [cur_pacman[0] - 1, cur_pacman[1]],

                next_pacman = next_pacman[0]
                if shape[0] > next_pacman[0] >= 0 and \
                        shape[1] > next_pacman[1] >= 0 and \
                        map_dict[str(next_pacman[0]) + ',' + str(next_pacman[1])] != '#' and \
                        str(next_pacman[0]) + ',' + str(next_pacman[1]) not in visited.keys():
                    if next_pacman in targets:
                        for target in targets:
                            if next_pacman == target:
                                found_start = False
                                prev_pacman = cur_pacman
                                tmp = []
                                while not found_start:
                                    if prev_pacman == start:
                                        found_start = True
                                    tmp.append(prev_pacman)
                                    if map_dict[str(prev_pacman[0]) + ',' + str(prev_pacman[1])] == '.':
                                        map_dict[str(prev_pacman[0]) + ',' + str(prev_pacman[1])] = ' '
                                    prev_state = visited[str(prev_pacman[0]) + ',' + str(prev_pacman[1])]
                                    prev_pacman = prev_state.getPrev()
                                path += tmp[::-1]
                                targets.remove(target)
                                start = next_pacman
                                total_cost += cost + 1
                                cost = 0
                        visited = dict()
                        reset = True
                        initial_state = self.State(start, targets, start, 0)
                        visited[str(start[0]) + ',' + str(start[1])] = initial_state
                        if len(targets) == 0:
                            ans = [[] for _ in range(num_rows)]
                            for i in range(num_rows):
                                for j in range(num_cols):
                                    if [i, j] in path:
                                        if raw_input[i][j] == '.':
                                            ans[i].append('.')
                                        elif raw_input[i][j] == 'P':
                                            ans[i].append('P')
                                        else:
                                            ans[i].append('R')
                                    else:
                                        ans[i].append(raw_input[i][j])
                            return total_cost, path, final_map
                    if reset:
                        new_state = self.State(next_pacman, cur_targets, next_pacman, 0)
                        aStarQueue = [(self.heuristic(initial_state, targets),
                                       initial_state.getCost(), steps, initial_state)]
                        heapq.heapify(aStarQueue)
                    else:
                        new_state = self.State(next_pacman, cur_targets, cur_pacman, cost + 1)
                        heapq.heappush(aStarQueue, (self.heuristic(new_state, targets) +
                                                    new_state.getCost(), new_state.getCost(),
                                                    steps, new_state))
                    visited[str(next_pacman[0]) + ',' + str(next_pacman[1])] = new_state
                    steps += 1

                    if reset:
                        break
        return -1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=float)
    parser.add_argument('--f', type=int)
    args = parser.parse_args()

    file_number = 2
    sleep_time = 0
    file_name = 'game%d.txt' % file_number
    file_path = os.path.join('../test', file_name)
    Solver = PacmanSolver()
    res, path, maze = Solver.solve(file_path)
    score = vis(path, maze, sleep_time)
    print('Your final score is %d' % (score + 4))
