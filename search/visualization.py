import os
from time import sleep


def vis(path, maze, delay):
    # config terminal clear command
    clear = 'cls' if os.name == 'nt' else 'clear'

    # initial maze
    score = 0
    for row in maze:
        print(row)

    for idx, coord in enumerate(path[1:], 1):
        # delay between steps
        sleep(delay)
        os.system(clear)

        # calculate score
        score -= 1
        if maze[coord[0]][coord[1]] == '.':
            score += 5

        # modify string for display
        maze[path[idx - 1][0]] = maze[path[idx - 1][0]].replace('P', ' ')
        maze[coord[0]] = maze[coord[0]][:coord[1]] + 'P' + maze[coord[0]][coord[1]+1:]

        # display on terminal
        for row in maze:
            print(row)
        print('Your score is %d' % score)

    # print final score
    sleep(delay)
    os.system(clear)
    for row in maze:
        print(row.replace('P', ' ').replace('.', 'P'))
    print('Your final score is %d' % (score + 4))
