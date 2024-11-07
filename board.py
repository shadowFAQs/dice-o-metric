from itertools import chain
from pathlib import Path
from random import randint

import pygame as pg

from const import Color, DIE_SPRITE_SIZE, SCREEN_SIZE, TILE_GAP, TILE_SIZE
from dice import Dice
from image import SpriteSheet


class Board(pg.sprite.Sprite):
    def __init__(self, sprite_sheet: SpriteSheet):
        pg.sprite.Sprite.__init__(self)

        self.num_cols         = 8
        self.num_rows         = 8
        self.sprite_sheet     = sprite_sheet

        self.color            = Color()
        self.dice             = []
        self.heightmap        = []
        self.offset           = pg.math.Vector2(8, 8)
        self.selection_coords = pg.math.Vector2(0, 0)
        self.show_selection   = True

        self.background_image = pg.image.load(Path('img') / 'bg.bmp')
        self.rect = self.background_image.get_rect()
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)

        self.spawn_dice()

    def draw(self):
        self.image.fill(self.color.black)
        self.image.blit(self.background_image, (0, 0))

        for row in range(self.num_rows):
            for col in range(self.num_cols - 1, -1, -1):
                die = self.dice[row][col]
                self.image.blit(die.image, die.coords - (0, die.height))

        if self.show_selection:
            self.image.blit(self.sprite_sheet.selection, self.selection_coords)

    def get_all_dice(self) -> list[Dice]:
        """Returns flattened list from 2D list"""
        return list(chain(*self.dice))

    def get_die_coords(self, row: int, col: int) -> pg.math.Vector2:
        """
        Translates row & col into pixel position
        on an isometric map
        """
        x_step = TILE_SIZE.x / 2 + TILE_GAP
        y_step = TILE_SIZE.y / 2 + TILE_GAP

        x = (self.rect.width - (DIE_SPRITE_SIZE.x * 8 + 14 * TILE_GAP)) // 2
        y = self.rect.height - DIE_SPRITE_SIZE.y * 3
        x += x_step * col
        y -= y_step * col
        x += x_step * row
        y += y_step * row

        return pg.math.Vector2(x, y)

    def highlight_hovered_die(self, position: tuple[int]):
        die_top = pg.Rect(0, 0, 32, 17)
        for die in self.get_all_dice():
            if die_top.move(die.coords).collidepoint(position):
                self.selection_coords = die.coords + (0, -3)  # TODO: Why offset
                self.show_selection = True
                return
        else:
            self.show_selection = False

    def spawn_dice(self):
        self.dice = []

        image = self.sprite_sheet.dice
        for row in range(self.num_rows):
            dice_row = []
            for col in range(self.num_cols):
                value = randint(0, 6)
                starting_height = 200 + row * 128 + col * 32 + randint(0, 64)
                image = self.sprite_sheet.dice[value]
                coords = self.get_die_coords(row, col)
                dice_row.append(Dice(value, coords, starting_height, image))

            self.dice.append(dice_row)

    def update(self, images: dict):
        for die in self.get_all_dice():
            die.update()

        self.draw()
