#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
A quick Game of Life implementation I wrote for a practice interview.

Stuff that's quite neat (imo):

*   Emoji!
*   Rather than printing a new board every time, it resets the existing board
    with some ASCII control characters (think \r but better)

"""

import collections
import random
import sys


WIDTH = 30
HEIGHT = 30


class Cell(object):
    def __init__(self, is_alive):
        self.is_alive = is_alive

    def __repr__(self):
        return '%s(is_alive=%r)' % (type(self).__name__, self.is_alive)


def random_grid():
    grid = {}
    for x in range(WIDTH):
        for y in range(HEIGHT):
            grid[(x, y)] = Cell(is_alive=random.choice((True, False)))
    return grid


def neighbours(x, y):
    result = []
    for x_diff in (-1, 0, 1):
        for y_diff in (-1, 0, 1):
            p = (x + x_diff, y + y_diff)
            if p[0] < 0:
                p = (WIDTH - 1, p[1])
            elif p[0] >= WIDTH:
                p = (0, p[1])
            if p[1] < 0:
                p = (p[0], HEIGHT - 1)
            elif p[1] >= HEIGHT:
                p = (p[0], 0)
            if p != (x, y):
                result.append(p)
    return result


def next_grid(grid):
    new_grid = {}
    for coordinate, cell in grid.items():
        nghbrs = sum([grid[n].is_alive for n in neighbours(*coordinate)])
        if cell.is_alive:
            is_alive = (nghbrs in (2, 3))
        else:
            is_alive = (nghbrs == 3)
        new_grid[coordinate] = Cell(is_alive=is_alive)
    return new_grid


def print_grid(grid):
    for row_idx in range(HEIGHT):
        row = dict((c, cell) for (c, cell) in grid.items() if c[1] == row_idx)
        row = [cell for c, cell in sorted(row.items(), key=lambda x: x[0][0])]
        row = [C if cell.is_alive else '·' for cell in row]
        print(' '.join(row))


while True:
    # C = random.choice(['🐞', '🍏', '🐱', '♠️', '💜', '💎', '🍊'])
    C = "X"

    grid = random_grid()

    for _ in range(1000):
        try:
            print_grid(grid)
            grid = next_grid(grid)

            import time
            time.sleep(0.25)
            print('\033[F' * (HEIGHT + 1))
        except KeyboardInterrupt:
            sys.exit(0)
