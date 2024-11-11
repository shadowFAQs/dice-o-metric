from itertools import chain
from pathlib import Path
from random import randint
from typing import Callable

import pygame as pg
from shapely import Point, Polygon

from const import Color, BOARD_POS, DIE_SPRITE_SIZE, SCREEN_SIZE, TILE_GAP, \
                  TILE_SIZE
from dice import Dice
from image import SpriteSheet


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
        self.show_highlight   = 0  # [-1, 0, 1]

        self.background_image = pg.image.load(Path('img') / 'bg.bmp')
        self.rect = self.background_image.get_rect()
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)  # (320, 304)

        self.spawn_dice()

    def choose_die_under_mouse(self):
        self.chosen_die = self.get_hovered_die()

    def draw(self):
        self.image.fill(self.color.black)
        self.image.blit(self.background_image, (0, 0))

        for die in self.get_all_dice(sort=True):
            self.image.blit(die.get_image(), die.pos)

        if self.show_highlight:
            highlight = self.sprite_sheet.highlight \
                if self.show_highlight == 1 else self.sprite_sheet.dimlight
            self.image.blit(highlight, self.highlight_coords)

    def get_all_dice(self, sort: bool = False) -> list[Dice]:
        """Returns flattened list from 2D list"""
        flat_list = list(chain(*self.dice))
        if not sort:
            return flat_list

        return sorted(flat_list, key=lambda d: d.z_index)  # Sort by draw order

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
                    (die.pos + (0, 8), die.pos + (15, 0),
                     die.pos + (31, 8), die.pos + (15, 16))
                )
                if hitbox.contains(mouse_point):
                    return die

        return None

    def get_mouse_pos(self) -> pg.math.Vector2:
        return (
            pg.mouse.get_pos() - BOARD_POS) / 2 - (TILE_GAP * 2, TILE_GAP * 2)

    def get_neighbor_in_direction(self, start: Dice,
                                  move: 'Move') -> Dice | None:
        try:
            if move.axis == 'row':
                return self.get_die_from_coords(row=start.row + move.value,
                                                col=start.col)
            else:
                return self.get_die_from_coords(row=start.row,
                                                col=start.col + move.value)
        except IndexError:
            print('Off the edge of the board')
            return None

    def highlight_hovered_die(self):
        die = self.get_hovered_die()
        if die:
            if die.offsets:  # Don't highlight during animation
                self.show_highlight = 0
                return

            match die.value:
                case -1:  # Empty space; don't show highlight on hover
                    self.show_highlight = 0
                case 0:   # Rock die; show dim highlight
                    self.highlight_coords = die.pos
                    self.show_highlight = -1
                case _:
                    self.highlight_coords = die.pos
                    self.show_highlight = 1
        else:
            self.show_highlight = 0

    def spawn_dice(self):
        from game import _roll_d6

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

                images = {
                    'image': image,
                    'ghost': ghost_image,
                    'flash_solid': pg.Surface((DIE_SPRITE_SIZE), pg.SRCALPHA),
                    'flash_wireframe': pg.Surface((DIE_SPRITE_SIZE),
                                                   pg.SRCALPHA)
                }
                images['flash_solid'].blit(
                    self.sprite_sheet.dice_flash['solid'], (0, 0))
                images['flash_wireframe'].blit(
                    self.sprite_sheet.dice_flash['wireframe'], (0, 0))
                dice_row.append(
                    Dice(row, col, value, self.get_die_pos(row, col),
                         animation_delay, images)
                )

            self.dice.append(dice_row)

    def update(self, mouse_motion: bool):
        if mouse_motion:
            self.highlight_hovered_die()

        for die in self.get_all_dice():
            die.update()

        self.draw()
