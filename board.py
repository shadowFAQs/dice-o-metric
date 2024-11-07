from itertools import chain
from pathlib import Path
from random import randint

import pygame as pg
from shapely import Point, Polygon

from const import Color, DIE_SPRITE_SIZE, SCREEN_SIZE, TILE_GAP, TILE_SIZE
from dice import Dice
from image import SpriteSheet


def _transform_by_coords(x: int, y: int, coords: tuple[int]) -> tuple[int]:
    return x + coords[0], y + coords[1]


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
                self.image.blit(die.image, die.coords - (0, die.get_height()))

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

    def highlight_hovered_die(self):
        self.show_selection = False

        mouse_pos = (pg.mouse.get_pos() - self.offset) / 2  + (-4, -4)
        if self.rect.collidepoint(mouse_pos):
            mouse_point = Point(mouse_pos)

            for die in self.get_all_dice():
                hitbox = Polygon(
                    (die.coords + (0, 8), die.coords + (15, 0),
                     die.coords + (31, 8), die.coords + (15, 16))
                )
                if hitbox.contains(mouse_point):
                    self.selection_coords = die.coords
                    self.show_selection = True
                    return

    def spawn_dice(self):
        self.dice = []

        image = self.sprite_sheet.dice
        for row in range(self.num_rows):
            dice_row = []
            for col in range(self.num_cols):
                animation_delay = row * 5 + col * 2 + randint(0, 8)
                value = randint(0, 6)
                image = self.sprite_sheet.dice[value]
                coords = self.get_die_coords(row, col)
                dice_row.append(Dice(value, coords, animation_delay, image))

            self.dice.append(dice_row)

    def update(self):
        self.highlight_hovered_die()

        for die in self.get_all_dice():
            die.update()

        self.draw()
