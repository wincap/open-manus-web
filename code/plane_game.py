#!/usr/bin/env python3

import os
import sys
import time
import curses

# Check if the system is Linux
if not os.name == "posix" or not os.uname().sysname == "Linux":
    print("This script is intended to run on a Linux system.")
    sys.exit(1)

def main(stdscr):
    # Clear screen and initialize
    stdscr.clear()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Get terminal dimensions
    height, width = stdscr.getmaxyx()

    # Set up initial plane position
    plane_x, plane_y = width // 2, height // 2

    # Function to move the plane
    def move_plane(dx, dy):
        nonlocal plane_x, plane_y
        # Update plane's position with bounds checking
        plane_x = max(1, min(width - 2, plane_x + dx))
        plane_y = max(1, min(height - 2, plane_y + dy))
        # Draw the plane at its new position
        stdscr.addstr(plane_y, plane_x, ">")
        stdscr.refresh()

    # Main loop for the game
    try:
        while True:
            # Clear the previous plane position
            stdscr.addstr(plane_y, plane_x, " ")
            # Get user input
            key = stdscr.getch()
            if key == ord('q'):  # Quit the game if 'q' is pressed
                break
            elif key == curses.KEY_UP:
                move_plane(0, -1)
            elif key == curses.KEY_DOWN:
                move_plane(0, 1)
            elif key == curses.KEY_LEFT:
                move_plane(-1, 0)
            elif key == curses.KEY_RIGHT:
                move_plane(1, 0)
            else:
                move_plane(0, 0)
    finally:
        # Restore the terminal settings before exiting
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(False)
        curses.endwin()

if __name__ == "__main__":
    curses.wrapper(main)
    print("Game has ended. Thank you for playing!")