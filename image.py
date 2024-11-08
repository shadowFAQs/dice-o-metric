from pathlib import Path

import pygame as pg

from const import Color, ARROW_SIZE, DIE_SPRITE_SIZE, SELECTION_SIZE


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

        self.highlight = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.highlight.blit(self.sprite_sheet, (-7 * 32, 0))

        self.selection = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.selection.blit(self.sprite_sheet, (-8 * 32, 0))

        arrow_names = ['ne', 'nw', 'se', 'sw']
        self.arrows = {}
        for n in range(4):
            self.arrows[arrow_names[n]] = pg.Surface(ARROW_SIZE, pg.SRCALPHA)
            self.arrows[arrow_names[n]].blit(
                self.sprite_sheet, (-ARROW_SIZE.x * (n + 1), -32))

        self.arrow_bg = pg.Surface(ARROW_SIZE, pg.SRCALPHA)
        self.arrow_bg.blit(self.sprite_sheet, (-ARROW_SIZE.x * 4, -32))
