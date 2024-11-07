import pygame as pg


DIE_SPRITE_SIZE    = pg.math.Vector2(32, 36)
SCREEN_SIZE        = pg.math.Vector2(960, 640)
SELECTION_SIZE     = pg.math.Vector2(32, 17)
TILE_SIZE          = pg.math.Vector2(32, 16)

TILE_GAP           = 2


class Color():
    def __init__(self):
        self.black       = pg.Color('#121212')
        self.red         = pg.Color('#ff5555')
        self.transparent = pg.Color('#ff00ff00')
