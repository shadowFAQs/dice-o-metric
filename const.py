import pygame as pg


ARROW_SIZE         = pg.math.Vector2(64, 64)
BOARD_POS          = pg.math.Vector2(8, 8)
DIE_SPRITE_SIZE    = pg.math.Vector2(32, 36)
INFO_POS           = BOARD_POS + (328, 28)
MOVE_QUEUE_SIZE    = pg.math.Vector2(480, 72)
NEXT_BADGE_POS     = pg.math.Vector2(8, 52)
SCREEN_SIZE        = pg.math.Vector2(960, 640)
SELECTION_SIZE     = pg.math.Vector2(32, 17)
TILE_SIZE          = pg.math.Vector2(32, 16)

TILE_GAP           = 2

MOVES = [
    ('se', 'row', 1),
    ('nw', 'row', -1),
    ('ne', 'col', 1),
    ('sw', 'col', -1),
]


class Color():
    def __init__(self):
        self.black       = pg.Color('#121212')
        self.red         = pg.Color('#ff5555')
        self.transparent = pg.Color('#ff00ff00')
