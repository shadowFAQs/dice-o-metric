from pathlib import Path
from random import randint

import pygame as pg
import pytweening

from const import Color


class Dice(pg.sprite.Sprite):
    def __init__(self, row: int, col: int, value: int, pos: pg.math.Vector2,
                 animation_delay: int, images: dict):
        pg.sprite.Sprite.__init__(self)
        """
        For {value}, 0 means a "rock" die;
        -1 means "kill me once I'm done animating".
        Everything else is just the number of dimples showing.
        """

        self.row         = row
        self.col         = col
        self.value       = value
        self.pos         = pos  # Pixel position (where to draw)

        self.ghost_image     = images['ghost']
        self.image           = images['image']
        self.fade_counter    = 255
        self.flash_solid     = images['flash_solid']
        self.flash_wireframe = images['flash_wireframe']

        self.animation_frames = []  # List of pg.Surface
        self.current_frame    = 0
        self.freeze_z_index   = False
        self.ghost            = False
        self.rect             = self.image.get_rect()
        self.slide_direction  = None
        self.offset_step      = 0
        self.offsets          = []  # List of pg.math.Vector2
        self.z_index          = 0

        self.color   = Color()

        self.build_drop_animation(animation_delay)

    def __repr__(self) -> str:
        return f'Die {self.value} @ (r{self.row}, c{self.col})'

    def animate(self):
        if self.offsets and self.offset_step < len(self.offsets) - 1:
            self.offset_step += 1
            if self.ghost:
                self.fade_counter -= 7
        else:
            self.offsets = []
            self.offset_step = 0
            self.freeze_z_index = False
            self.z_index = self.pos.y
            if self.ghost:
                self.fade_counter = 0

        if self.current_frame:
            if self.current_frame < len(self.animation_frames) - 1:
                self.current_frame += 1
            else:
                self.current_frame = 0
                self.animation_frames = []
                self.build_flyaway_animation()
                self.ghost = True

    def build_drop_animation(self, animation_delay: int):
        num_frames = 40 + randint(-4, 4)
        delay = animation_delay
        starting_y = -320

        raw_positions = [
            pytweening.easeInQuad((n / num_frames)) * starting_y \
                for n in range(num_frames + 1)
        ]
        raw_positions += [starting_y for _ in range(delay)]
        raw_positions.reverse()
        raw_positions = [pg.math.Vector2(0, y) for y in raw_positions]
        self.set_offsets_from_raw_positions(
            raw_positions, start_value=pg.math.Vector2(0, starting_y))
        self.z_index = self.pos.y
        self.freeze_z_index = True

    def build_flyaway_animation(self):
        num_frames = self.fade_counter // 7
        target_y = randint(-66, -50)
        raw_positions = [
            pytweening.easeInQuad((n / num_frames)) * target_y \
                for n in range(num_frames + 1)
        ]
        raw_positions = [pg.math.Vector2(0, y) for y in raw_positions]
        self.set_offsets_from_raw_positions(raw_positions)
        self.z_index = self.pos.y
        self.freeze_z_index = True

    def build_slide_animation(self, start_pos: tuple[int], end_pos: tuple[int]):
        raw_positions = []
        for x, y in pytweening.iterLinear(
            start_pos[0], start_pos[1], end_pos[0], end_pos[1], 0.1):
            raw_positions.append(pg.math.Vector2(x, y))

        self.set_offsets_from_raw_positions(raw_positions)

    def end_slide(self):
        self.slide_direction = None

    def get_height(self) -> float:
        if self.offsets:
            return self.offsets[self.offset_step]
        else:
            return 0

    def get_image(self) -> pg.Surface:
        if self.current_frame:
            return self.animation_frames[self.current_frame]
        elif self.ghost:
            self.ghost_image.set_alpha(self.fade_counter)
            return self.ghost_image
        else:
            return self.image

    def is_animating(self) -> bool:
        return self.offsets or self.animation_frames

    def kill(self, delay: int):
        self.value = -1

        self.animation_frames  = [self.image for _ in range(delay * 3)]
        self.animation_frames += [self.flash_solid for _ in range(2)]
        self.animation_frames += [self.flash_wireframe for _ in range(2)]
        self.animation_frames += [self.flash_solid for _ in range(2)]

        self.current_frame = 1

    def set_coords(self, row: int, col: int):
        self.row = row
        self.col = col

    def set_offsets_from_raw_positions(
        self, raw_positions: list[pg.math.Vector2],
        start_value: pg.math.Vector2 | None = None):
        if start_value is None:
            self.offsets = []
        else:
            self.offsets = [start_value]

        for n in range(1, len(raw_positions)):
            self.offsets.append(raw_positions[n] - raw_positions[n - 1])

    def set_pos(self):
        if self.offsets:
            self.pos += self.offsets[self.offset_step]

            if not self.freeze_z_index:
                self.z_index = self.pos.y

    def slide(self, start_pos: tuple[int], end_pos: tuple[int], move: 'Move'):
        self.build_slide_animation(start_pos, end_pos)
        self.slide_direction = {'axis': move.axis, 'value': move.value}

    def update(self):
        self.set_pos()
        self.animate()
