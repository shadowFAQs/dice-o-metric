import pygame as pg


BOARD_INNER_OFFSET = pg.math.Vector2(32, 32)
BOARD_OFFSET       = pg.math.Vector2(32, 16)
DIE_SPRITE_SIZE    = pg.math.Vector2(32, 36)
SCREEN_SIZE        = pg.math.Vector2(960, 640)
TILE_SIZE          = pg.math.Vector2(32, 16)


class Color():
    def __init__(self):
        self.black       = pg.Color('#121212')
        self.red         = pg.Color('#ff5555')
        self.transparent = pg.Color('#ff00ff00')
