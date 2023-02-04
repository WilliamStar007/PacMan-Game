from visualization import vis
import argparse
import heapq
import os


class PacmanSolver:
    class State:
        # the class object for state
        def __init__(self, pacman, targets, prev, cost):
            # pacman position
            self.pacman = pacman
            # food dot positions
            self.targets = targets
            self.cost = cost
            self.prev = prev

        def get_pacman(self):
            return self.pacman

        def get_targets(self):
            return self.targets

        def get_cost(self):
            return self.cost

        def get_prev(self):
            return self.prev

    @staticmethod
    def load_input(file):
        f = open(file, 'r')
        raw_input = []
        for line in f.readlines():
            raw_input.append(line.strip())
        return raw_input

    @staticmethod
    def heuristic(state, targets):
        # shortest manhattan distance
        cost = 0
        for target in targets:
            cur = abs(state.get_pacman()[0] - target[0]) + abs(state.get_pacman()[1] - target[1])
            if cur < cost:
                cost = cur
        return cost

    def solve(self, input_filename):
        # load pacman map file
        raw_input = self.load_input(input_filename)
        game_map = raw_input
        num_rows = len(raw_input)
        num_cols = len(raw_input[0])
        map_dict = dict()
        pacman = tuple()
        targets = list()    # TODO: targets should be tuples

        # locate pacman and targets
        for i in range(num_rows):
            for j in range(num_cols):
                if raw_input[i][j] == 'P':
                    pacman = (i, j)
                    map_dict[(i, j)] = ' '
                elif raw_input[i][j] == '.':
                    map_dict[(i, j)] = '.'
                    targets.append([i, j])
                else:
                    map_dict[(i, j)] = raw_input[i][j]
                    continue

        # set initial state
        total_steps = 1
        total_cost = 0
        visited = dict()
        initial_state = self.State(pacman, targets, pacman, total_cost)
        visited[pacman] = initial_state
        aStarQueue = [(self.heuristic(initial_state, targets),
                       total_cost, total_steps, initial_state)]
        heapq.heapify(aStarQueue)

        path = []
        start = pacman
        while aStarQueue:
            reset = False
            cur_state = heapq.heappop(aStarQueue)[3]
            cur_cost = cur_state.get_cost()
            cur_pacman = cur_state.get_pacman()
            cur_targets = cur_state.get_targets()
            next_pacman = list()
            for i in range(4):
                if i == 0:
                    next_pacman = [cur_pacman[0], cur_pacman[1] + 1]
                elif i == 1:
                    next_pacman = [cur_pacman[0], cur_pacman[1] - 1]
                elif i == 2:
                    next_pacman = [cur_pacman[0] + 1, cur_pacman[1]]
                elif i == 3:
                    next_pacman = [cur_pacman[0] - 1, cur_pacman[1]]

                if num_rows > next_pacman[0] >= 0 and num_cols > next_pacman[1] >= 0 \
                        and map_dict[tuple(next_pacman)] != '#' \
                        and tuple(next_pacman) not in visited.keys():
                    if next_pacman in targets:
                        found_path = False
                        prev_pacman = cur_pacman
                        tmp = []
                        # find path to target
                        while not found_path:
                            if prev_pacman == start:
                                found_path = True
                            tmp.append(prev_pacman)
                            if map_dict[tuple(prev_pacman)] == '.':
                                map_dict[tuple(prev_pacman)] = ' '
                            prev_state = visited[tuple(prev_pacman)]
                            prev_pacman = prev_state.get_prev()

                        path += tmp[::-1]
                        targets.remove(next_pacman)
                        total_cost += cur_cost + 1
                        cur_cost = 0

                        start = next_pacman
                        visited = dict()
                        reset = True
                        initial_state = self.State(start, targets, start, 0)
                        visited[tuple(start)] = initial_state

                        # all food dots have been reached
                        if not targets:
                            return total_cost, path, game_map

                    if reset:
                        new_state = self.State(next_pacman, cur_targets, next_pacman, 0)
                        aStarQueue = [(self.heuristic(initial_state, targets),
                                       initial_state.get_cost(), total_steps, initial_state)]
                        heapq.heapify(aStarQueue)
                    else:
                        new_state = self.State(next_pacman, cur_targets, cur_pacman, cur_cost + 1)
                        heapq.heappush(aStarQueue, (self.heuristic(new_state, targets) +
                                                    new_state.get_cost(), new_state.get_cost(),
                                                    total_steps, new_state))

                    visited[tuple(next_pacman)] = new_state
                    total_steps += 1
                    if reset:
                        break
        return -1


if __name__ == '__main__':
    # command line execution support
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=float)
    parser.add_argument('--f', type=int)
    args = parser.parse_args()

    # config test file and display delay
    file_number = args.f if args.f is not None else 2
    sleep_time = args.t if args.t is not None else 0.01
    file_name = 'game%d.txt' % file_number
    file_path = os.path.join('../tests', file_name)

    # runtime visualization
    final_cost, final_path, maze = PacmanSolver().solve(file_path)
    score = vis(final_path, maze, sleep_time)
