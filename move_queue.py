from random import randint

import pygame as pg
import pytweening

from const import Color, MOVE_QUEUE_SIZE, MOVES, NEXT_BADGE_POS, SCREEN_SIZE
from image import SpriteSheet


class Move():
    def __init__(self, name: str, axis: str, value: int, pos: pg.math.Vector2):
        self.name  = name   # [ne, nw, se, sw]
        self.axis  = axis   # [row, col]
        self.value = value  # [-1, 1]
        self.pos   = pos

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
        self.offset_step       = 0
        self.offsets           = []

        while len(self.moves) < self.max_moves:
            self.spawn_move()
        self.moves[self.active_move_index].activate()

        self.build_animation()

    def __getitem__(self, index: int) -> Move:
        return self.moves[index]

    def advance(self):
        self.spawn_move()
        self.active_move_index = 4
        self.offset_step = 1

    def animate(self):
        if self.offset_step:
            if self.offset_step < len(self.offsets) - 1:
                self.offset_step += 1
            else:
                self.delete_offscreen_move()
                self.offset_step = 0

    def build_animation(self):
        from game import _convert_raw_positions_to_offsets

        num_frames = 20
        target_x = -68

        raw_positions = [
            pytweening.easeInOutQuad((n / num_frames)) * target_x \
                for n in range(num_frames + 1)
        ]
        raw_positions = [pg.math.Vector2(x, 0) for x in raw_positions]
        self.offsets = _convert_raw_positions_to_offsets(raw_positions)

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

            if self.offset_step:
                move.pos += self.offsets[self.offset_step]
            else:
                move.pos = pg.math.Vector2(self.move_width * n, 0)

            self.image.blit(move.active_image, move.pos)

        self.image.blit(self.sprite_sheet.next_badge, NEXT_BADGE_POS)

    def get_active_move(self) -> Move:
        return self.moves[self.active_move_index]

    def is_animating(self) -> bool:
        return bool(self.offset_step)

    def spawn_move(self):
        num_moves = len(self.moves)
        move = Move(*MOVES[randint(0, 3)], pos=(self.move_width * num_moves, 0))
        move.base_image = self.sprite_sheet.arrows[move.name]
        move.dark_image = self.sprite_sheet.dark_arrows[move.name]
        move.active_image = move.dark_image

        self.moves.append(move)

    def update(self):
        self.animate()
        self.draw()
