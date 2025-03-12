import curses
from random import randint

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    snake = [(sh//2, sw//2)]
    direction = curses.KEY_RIGHT
    food = (randint(1, sh-2), randint(1, sw-2))
    score = 0
    w.addch(food[0], food[1], '#')

    while True:
        key = w.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = (head[0], head[1]+1)
        elif direction == curses.KEY_LEFT:
            new_head = (head[0], head[1]-1)
        elif direction == curses.KEY_UP:
            new_head = (head[0]-1, head[1])
        elif direction == curses.KEY_DOWN:
            new_head = (head[0]+1, head[1])

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = None
            while food is None:
                nf = (
                    randint(1, sh-2),
                    randint(1, sw-2)
                )
                food = nf if nf not in snake else None
            w.addch(food[0], food[1], '#')
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        if (new_head[0] in [0, sh-1] or 
            new_head[1] in [0, sw-1] or 
            new_head in snake):
            msg = f'Game Over! Score: {score}'
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
            stdscr.refresh()
            stdscr.getch()
            break

        w.addch(new_head[0], new_head[1], '*')

        stdscr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)

# Note: To run this game, you need to execute it as a script. It can't be run inside the current environment.