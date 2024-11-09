from pathlib import Path

import pygame as pg

from const import Color, ARROW_SIZE, DIE_SPRITE_SIZE, MOVE_QUEUE_POS, \
                  SCREEN_SIZE, SELECTION_SIZE


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

        self.dimlight = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.dimlight.blit(self.sprite_sheet, (-8 * 32, 0))

        arrow_names = ['ne', 'nw', 'sw', 'se']
        self.arrows = {}
        self.dark_arrows = {}
        for n in range(4):
            self.arrows[arrow_names[n]] = pg.Surface(ARROW_SIZE, pg.SRCALPHA)
            self.arrows[arrow_names[n]].blit(
                self.sprite_sheet, (-ARROW_SIZE.x * n, -48))

            self.dark_arrows[arrow_names[n]] = pg.Surface(
                ARROW_SIZE, pg.SRCALPHA)
            self.dark_arrows[arrow_names[n]].blit(
                self.sprite_sheet, (-ARROW_SIZE.x * n, -112))

        self.next_badge = pg.Surface((47, 16), pg.SRCALPHA)
        self.next_badge.blit(self.sprite_sheet, (-264, -52))

        # Move queue "track"
        queue_bg = pg.Surface((96, 14), pg.SRCALPHA)
        queue_bg.blit(self.sprite_sheet, (-224, -17))
        self.queue_bg = pg.Surface((SCREEN_SIZE.x / 2, 14), pg.SRCALPHA)
        for n in range(5):
            self.queue_bg.blit(queue_bg, (96 * n, 0))

        self.info_bg = pg.image.load(Path('img') / 'info_bg.bmp')
