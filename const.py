import pygame as pg


ARROW_SIZE         = pg.math.Vector2(64, 64)
BANNER_POS         = pg.math.Vector2(63, 90)
BOARD_POS          = pg.math.Vector2(8, 8)
BTN_POS_HIGH       = pg.math.Vector2(108, 120)
BTN_POS_LOW        = pg.math.Vector2(108, 150)
DIE_SPRITE_SIZE    = pg.math.Vector2(32, 36)
INFO_POS           = BOARD_POS + (328, 28)
MOVE_QUEUE_SIZE    = pg.math.Vector2(480, 72)
NEXT_BADGE_POS     = pg.math.Vector2(212, 5)
SCORE_LETTER_SIZE  = pg.math.Vector2(12, 10)
SCREEN_SIZE        = pg.math.Vector2(960, 640)
SELECTION_SIZE     = pg.math.Vector2(32, 17)
TILE_SIZE          = pg.math.Vector2(32, 16)

BASE_SCORE         = 6
TILE_GAP           = 2

MOVES = [
    ('se', 'row', 1),
    ('nw', 'row', -1),
    ('ne', 'col', 1),
    ('sw', 'col', -1),
]

SCORE_LETTER_WIDTHS = {  # Because you just had to choose a
    '0': 9,              # non-monospaced font, didn't you?
    '1': 5,
    '2': 8,
    '3': 8,
    '4': 11,
    '5': 8,
    '6': 10,
    '7': 10,
    '8': 10,
    '9': 10,
    '+': 10
}


class Color():
    def __init__(self):
        self.black       = pg.Color('#121212')
        self.blue        = pg.Color('#0cf1ff')
        self.green       = pg.Color('#99e65f')
        self.ice         = pg.Color('#a2cdf1')
        self.orange      = pg.Color('#ffc825')
        self.purple      = pg.Color('#ff5db0')
        self.red         = pg.Color('#ff616b')
        self.transparent = pg.Color('#ff616b00')
        self.white       = pg.Color('#fef4be')
