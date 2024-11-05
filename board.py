from itertools import chain
from random import randint

import pygame as pg

from const import Color, BOARD_INNER_OFFSET, DIE_SPRITE_SIZE, SCREEN_SIZE, \
                  TILE_SIZE
from dice import Dice
from image import SpriteSheet


class Board(pg.sprite.Sprite):
    def __init__(self, dimensions: tuple[int], sprite_sheet: SpriteSheet):
        pg.sprite.Sprite.__init__(self)

        self.num_cols = dimensions[0]
        self.num_rows = dimensions[1]
        self.sprite_sheet = sprite_sheet

        self.color = Color()
        self.dice      = []
        self.heightmap = []

        self.image = pg.Surface(
            (DIE_SPRITE_SIZE.x * self.num_cols + BOARD_INNER_OFFSET.x * 2,
             SCREEN_SIZE.y / 2 - TILE_SIZE.y * 2)
        )
        self.rect = self.image.get_rect()

        self.spawn_dice()

    def draw(self):
        self.image.fill(self.color.red)

        for row in range(self.num_rows):
            for col in range(self.num_cols - 1, -1, -1):
                die = self.dice[row][col]
                self.image.blit(die.image, self.get_die_coords(row, col))

    def get_all_dice(self) -> list[Dice]:
        """Returns flattened list from 2D list"""
        return list(chain(*self.dice))

    def get_die_coords(self, row: int, col: int) -> pg.math.Vector2:
        """
        Translates row & col into pixel position
        on an isometric map
        """
        x_step = TILE_SIZE.x / 2
        y_step = TILE_SIZE.y / 2

        x, y = DIE_SPRITE_SIZE.x, self.rect.height - DIE_SPRITE_SIZE.y * 3
        x += x_step * col
        y -= y_step * col
        x += x_step * row
        y += y_step * row
        y -= self.dice[row][col].height

        return pg.math.Vector2(x, y)

    def spawn_dice(self):
        self.dice = []

        image = self.sprite_sheet.dice
        for row in range(self.num_rows):
            dice_row = []
            for col in range(self.num_cols):
                value = randint(1, 6)
                starting_height = 200 + row * 128 + col * 32 + randint(0, 64)
                image = self.sprite_sheet.dice[value]
                dice_row.append(Dice(value, starting_height, image))

            self.dice.append(dice_row)

    def update(self, images: dict):
        for die in self.get_all_dice():
            die.update()

        self.draw()
