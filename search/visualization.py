import os
from time import sleep


def vis(path, map, t):
    score = 0
    for row in map:
        print(row)
    sleep(t)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

    for i in range(1, len(path)):
        score -= 1
        tmp1 = list(map[path[i][0]])
        if tmp1[path[i][1]] == '.':
            score += 5
        tmp1[path[i][1]] = 'P'
        map[path[i][0]] = "".join(tmp1)
        tmp2 = list(map[path[i - 1][0]])
        tmp2[path[i - 1][1]] = ' '
        map[path[i - 1][0]] = "".join(tmp2)
        for row in map:
            print(row)
        print('Your score is %d' % score)
        sleep(t)
        if i != len(path) - 1:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
    return score
