import pygame as pg


ARROW_SIZE         = pg.math.Vector2(64, 64)
BOARD_POS          = pg.math.Vector2(8, 8)
DIE_SPRITE_SIZE    = pg.math.Vector2(32, 36)
INFO_POS           = BOARD_POS + (328, 52)
MOVE_QUEUE_POS     = pg.math.Vector2((8 + 320) / 2 - 32, 20)
NEXT_BADGE_POS     = MOVE_QUEUE_POS + (8, 52)
SCREEN_SIZE        = pg.math.Vector2(960, 640)
SELECTION_SIZE     = pg.math.Vector2(32, 17)
TILE_SIZE          = pg.math.Vector2(32, 16)

TILE_GAP           = 2

MOVES = [
    {
        'name': 'se',
        'axis': 'row',
        'direction': 1
    },
    {
        'name': 'nw',
        'axis': 'row',
        'direction': -1
    },
    {
        'name': 'ne',
        'axis': 'col',
        'direction': 1
    },
    {
        'name': 'sw',
        'axis': 'col',
        'direction': -1
    },
]


class Color():
    def __init__(self):
        self.black       = pg.Color('#121212')
        self.red         = pg.Color('#ff5555')
        self.transparent = pg.Color('#ff00ff00')
