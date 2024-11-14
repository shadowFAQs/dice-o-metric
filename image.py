from pathlib import Path

import pygame as pg

from const import Color, ARROW_SIZE, DIE_SPRITE_SIZE, SCORE_LETTER_SIZE, \
                  SCREEN_SIZE, SELECTION_SIZE


class SpriteSheet():
    def __init__(self):
        base_filepath = Path('img') / 'sprites.bmp'

        color = Color()

        self.sprite_sheet = pg.image.load(base_filepath).convert_alpha()

        self.dice = dict()
        self.dice_ghosts = dict()
        for n in range(7):
            self.dice[n] = pg.Surface(DIE_SPRITE_SIZE, pg.SRCALPHA)
            self.dice[n].blit(
                self.sprite_sheet, (DIE_SPRITE_SIZE.x * -n, 0))
            self.dice_ghosts[n] = pg.Surface(DIE_SPRITE_SIZE, pg.SRCALPHA)
            self.dice_ghosts[n].blit(
                self.sprite_sheet, (DIE_SPRITE_SIZE.x * -n, -48))

        self.dice_flash = {}
        self.dice_flash['solid'] = pg.Surface(DIE_SPRITE_SIZE, pg.SRCALPHA)
        self.dice_flash['solid'].blit(
            self.sprite_sheet, (DIE_SPRITE_SIZE.x * -7, -48))
        self.dice_flash['wireframe'] = pg.Surface(
            DIE_SPRITE_SIZE, pg.SRCALPHA)
        self.dice_flash['wireframe'].blit(
            self.sprite_sheet, (DIE_SPRITE_SIZE.x * -8, -48))

        self.highlight = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.highlight.blit(self.sprite_sheet, (-224, 0))

        self.dimlight = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.dimlight.blit(self.sprite_sheet, (-256, 0))

        self.shadow = pg.Surface(SELECTION_SIZE, pg.SRCALPHA)
        self.shadow.blit(self.sprite_sheet, (-288, 0))
        self.shadow.set_alpha(32)

        arrow_names = ['ne', 'nw', 'sw', 'se']
        self.arrows = {}
        self.dark_arrows = {}
        for n in range(4):
            self.arrows[arrow_names[n]] = pg.Surface(ARROW_SIZE, pg.SRCALPHA)
            self.arrows[arrow_names[n]].blit(
                self.sprite_sheet, (-ARROW_SIZE.x * n, -96))

            self.dark_arrows[arrow_names[n]] = pg.Surface(
                ARROW_SIZE, pg.SRCALPHA)
            self.dark_arrows[arrow_names[n]].blit(
                self.sprite_sheet, (-ARROW_SIZE.x * n, -160))

        self.next_badge = pg.Surface(ARROW_SIZE + (0, 6), pg.SRCALPHA)
        self.next_badge.blit(self.sprite_sheet, (-264, -95))

        queue_track = pg.Surface((96, 14), pg.SRCALPHA)
        queue_track.blit(self.sprite_sheet, (-224, -17))
        self.queue_track = pg.Surface((SCREEN_SIZE.x / 2, 14), pg.SRCALPHA)
        for n in range(5):
            self.queue_track.blit(queue_track, (96 * n, 0))

        self.info_bg = pg.image.load(Path('img') / 'info_bg.bmp')

        self.score_font = {}
        for n in range(10):
            self.score_font[str(n)] = pg.Surface(SCORE_LETTER_SIZE, pg.SRCALPHA)
            self.score_font[str(n)].blit(
                self.sprite_sheet, (n * -SCORE_LETTER_SIZE.x, -224))
        self.score_font['+'] = pg.Surface(SCORE_LETTER_SIZE, pg.SRCALPHA)
        self.score_font['+'].blit(
                self.sprite_sheet, (10 * -SCORE_LETTER_SIZE.x, -224))

        self.puzzle_complete = pg.Surface((195, 19), pg.SRCALPHA)
        self.puzzle_complete.blit(self.sprite_sheet, (0, -240))
        self.puzzle_won = pg.Surface((195, 19), pg.SRCALPHA)
        self.puzzle_won.blit(self.sprite_sheet, (0, -259))
        self.game_over = pg.Surface((195, 19), pg.SRCALPHA)
        self.game_over.blit(self.sprite_sheet, (0, -278))

        self.continue_button = pg.Surface((105, 23), pg.SRCALPHA)
        self.continue_button.blit(self.sprite_sheet, (-208, -224))

        self.restart_button = pg.Surface((105, 23), pg.SRCALPHA)
        self.restart_button.blit(self.sprite_sheet, (-208, -247))
