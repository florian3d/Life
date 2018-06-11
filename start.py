''' Game of Life'''
from life import Life
from board import Board

LIFE = Life(columns=100, rows=100)
BOARD = Board(LIFE, box=8)

while not BOARD.quit:

    BOARD.update()

    if LIFE.stabilized_at > 0:
        BOARD.pause = True

    if (BOARD.pause and BOARD.step) or (not BOARD.pause and not BOARD.step):
        BOARD.step = False
        LIFE.next()
