from random import randint

import pygame as pg

from const import Color, MOVE_QUEUE_SIZE, MOVES, NEXT_BADGE_POS, SCREEN_SIZE
from image import SpriteSheet


class Move():
    def __init__(self, name: str, axis: str, value: int):
        self.name  = name   # [ne, nw, se, sw]
        self.axis  = axis   # [row, col]
        self.value = value  # [-1, 1]

        self.active_image = None
        self.base_image   = None
        self.dark_image   = None

    def __repr__(self) -> str:
        operator = '+' if self.value > 0 else ''
        return f'Move: {self.name.upper()} ({self.axis} {operator}{self.value})'

    def activate(self):
        self.active_image = self.base_image

    def deactivate(self):
        self.active_image = self.dark_image


class Queue():
    def __init__(self, sprite_sheet: SpriteSheet):
        self.sprite_sheet = sprite_sheet

        self.active_move_index = 3
        self.color             = Color()
        self.image             = pg.Surface(MOVE_QUEUE_SIZE, pg.SRCALPHA)
        self.max_moves         = 7
        self.move_width        = 68
        self.moves             = [None, None, None]
        self.offset_x          = 0

        while len(self.moves) < self.max_moves:
            self.spawn_move()
        self.moves[self.active_move_index].activate()

    def __getitem__(self, index: int) -> Move:
        return self.moves[index]

    def advance(self):
        self.spawn_move()
        self.active_move_index = 4
        self.offset_x = -1

    def animate(self):
        if self.offset_x:
            if self.offset_x > -self.move_width:
                self.offset_x -= 1
            else:
                self.delete_offscreen_move()
                self.offset_x = 0

    def delete_offscreen_move(self):
        self.moves.pop(0)
        self.active_move_index = 3

    def draw(self):
        self.image.fill(self.color.transparent)
        self.image.blit(self.sprite_sheet.queue_track, (0, 25))

        for n, move in enumerate(self.moves):
            if not move:
                continue

            if n == self.active_move_index:
                move.activate()
            else:
                move.deactivate()

            self.image.blit(
                move.active_image, (self.move_width * n + self.offset_x, 0))

        self.image.blit(
            self.sprite_sheet.next_badge,
            NEXT_BADGE_POS + \
                (self.move_width * self.active_move_index + self.offset_x, 0))

    def get_active_move(self) -> Move:
        return self.moves[self.active_move_index]

    def is_animating(self) -> bool:
        return bool(self.offset_x)

    def spawn_move(self):
            self.moves.append(Move(*MOVES[randint(0, 3)]))
            self.moves[-1].base_image = self.sprite_sheet.arrows[self.moves[-1].name]
            self.moves[-1].dark_image = self.sprite_sheet.dark_arrows[
                self.moves[-1].name]
            self.moves[-1].active_image = self.moves[-1].dark_image

    def update(self):
        self.animate()
        self.draw()
