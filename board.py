from itertools import chain
from pathlib import Path
from random import randint

import pygame as pg
from shapely import Point, Polygon

from const import Color, BOARD_POS, DIE_SPRITE_SIZE, SCREEN_SIZE, TILE_GAP, \
                  TILE_SIZE
from dice import Dice
from image import SpriteSheet


def _roll_d6() -> int:
    return randint(1, 6)


def _transform_by_coords(x: int, y: int, coords: tuple[int]) -> tuple[int]:
    return x + coords[0], y + coords[1]


class Board(pg.sprite.Sprite):
    def __init__(self, sprite_sheet: SpriteSheet):
        pg.sprite.Sprite.__init__(self)

        self.chosen_die       = None
        self.num_cols         = 8
        self.num_rows         = 8
        self.sprite_sheet     = sprite_sheet

        self.color            = Color()
        self.dice             = []
        self.highlight_coords = pg.math.Vector2(0, 0)
        self.show_highlight   = False

        self.background_image = pg.image.load(Path('img') / 'bg.bmp')
        self.rect = self.background_image.get_rect()
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)  # (320, 304)

        self.spawn_dice()

    def choose_die_under_mouse(self):
        self.chosen_die = self.get_hovered_die()

    def draw(self):
        self.image.fill(self.color.black)
        self.image.blit(self.background_image, (0, 0))

        for row in range(self.num_rows):
            for col in range(self.num_cols - 1, -1, -1):
                die = self.dice[row][col]
                die_image = die.ghost_image if die.ghost else die.image
                self.image.blit(die_image, die.coords - (0, die.get_height()))

        if self.show_highlight:
            highlight = self.sprite_sheet.highlight \
                if self.show_highlight == 1 else self.sprite_sheet.dimlight
            self.image.blit(highlight, self.highlight_coords)

    def get_all_dice(self) -> list[Dice]:
        """Returns flattened list from 2D list"""
        return list(chain(*self.dice))

    def get_blocker_in_direction(self, start: Dice,
                                 move: 'Move') -> Dice | None:
        print(move)
        print(f'Starting at {start}')
        try:
            if move.axis == 'row':
                blocker = self.get_die_from_coords(row=start.row + move.value,
                                                   col=start.col)
            else:
                blocker = self.get_die_from_coords(row=start.row,
                                                   col=start.col + move.value)
        except IndexError:
            print(f'Off the edge of the board @ row == {start.row + move.value}')
            return None

        return blocker

    def get_die_from_coords(self, row: int, col: int) -> Dice:
        if not (-1 < col < 8) or not (-1 < row < 8):
            raise IndexError

        return self.dice[row][col]

    def get_die_pos(self, row: int, col: int) -> pg.math.Vector2:
        """Translates row & col into pixel position"""
        x_step = TILE_SIZE.x / 2 + TILE_GAP
        y_step = TILE_SIZE.y / 2 + TILE_GAP

        x = (self.rect.width - (DIE_SPRITE_SIZE.x * 8 + 14 * TILE_GAP)) // 2
        y = self.rect.height - DIE_SPRITE_SIZE.y * 3
        x += x_step * col
        y -= y_step * col
        x += x_step * row
        y += y_step * row

        return pg.math.Vector2(x, y)

    def get_hovered_die(self) -> Dice | None:
        mouse_pos = self.get_mouse_pos()
        if self.rect.collidepoint(mouse_pos):
            mouse_point = Point(mouse_pos)

            for die in self.get_all_dice():
                hitbox = Polygon(
                    (die.coords + (0, 8), die.coords + (15, 0),
                     die.coords + (31, 8), die.coords + (15, 16))
                )
                if hitbox.contains(mouse_point):
                    return die

        return None

    def get_mouse_pos(self) -> pg.math.Vector2:
        return (
            pg.mouse.get_pos() - BOARD_POS) / 2 - (TILE_GAP * 2, TILE_GAP * 2)

    def highlight_hovered_die(self):
        self.show_highlight = 0

        die = self.get_hovered_die()
        if die:
            self.highlight_coords = die.coords
            self.show_highlight = -1 if die.value == -1 else 1

    def spawn_dice(self):
        self.dice = []

        image = self.sprite_sheet.dice
        for row in range(self.num_rows):
            dice_row = []
            for col in range(self.num_cols):
                if _roll_d6() > 1:
                    animation_delay = row * 5 + col * 2 + randint(0, 8)
                    value = randint(0, 6)
                    image = self.sprite_sheet.dice[value]
                    ghost_image = self.sprite_sheet.dice_ghosts[value]
                else:  # Create empty spot
                    animation_delay = 0
                    value = -1
                    image = pg.Surface((DIE_SPRITE_SIZE), pg.SRCALPHA)
                    image.fill(self.color.transparent)
                    ghost_image = None

                coords = self.get_die_pos(row, col)
                dice_row.append(Dice(row, col, value, coords, animation_delay,
                                     image, ghost_image))

            self.dice.append(dice_row)

    def update(self, mouse_motion: bool):
        if mouse_motion:
            self.highlight_hovered_die()

        for die in self.get_all_dice():
            die.update()

        self.draw()
