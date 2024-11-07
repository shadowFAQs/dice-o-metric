from pathlib import Path

import pygame as pg

from const import Color, DIE_SPRITE_SIZE, SELECTION_SIZE


class SpriteSheet():
    def __init__(self):
        base_filepath = Path('img') / 'sprites.bmp'

        color = Color()

        self.sprite_sheet = pg.image.load(base_filepath).convert_alpha()

        self.dice = dict()
        for n in range(7):
            self.dice[n] = pg.Surface(DIE_SPRITE_SIZE, pg.SRCALPHA)
            self.dice[n].blit(
                self.sprite_sheet, (DIE_SPRITE_SIZE.x * -n, 0))

        self.selection = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.selection.blit(self.sprite_sheet, (-7 * 32, 0))
