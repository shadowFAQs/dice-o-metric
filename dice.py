from pathlib import Path
from random import randint

import pygame as pg
import pytweening

from const import Color


class Dice(pg.sprite.Sprite):
    def __init__(self, row: int, col: int, value: int, coords: pg.math.Vector2,
                 animation_delay: int, images: dict):
        pg.sprite.Sprite.__init__(self)

        self.row         = row
        self.col         = col
        self.value       = value
        self.coords      = coords  # Pixel coords (where to draw)

        self.ghost_image     = images['ghost']
        self.image           = images['image']
        self.fade_counter    = 255
        self.flash_solid     = images['flash_solid']
        self.flash_wireframe = images['flash_wireframe']

        self.animation_frames = []
        self.current_frame    = 0
        self.ghost            = False
        self.heights          = []
        self.rect             = self.image.get_rect()

        self.color   = Color()

        self.build_drop_animation(animation_delay)

    def __repr__(self) -> str:
        return f'Die {self.value} @ (r{self.row}, c{self.col})'

    def animate(self):
        """Handles "falling" animation at stage load"""
        if self.height_step and self.height_step < len(self.heights) - 1:
            self.height_step += 1
            if self.ghost:
                self.fade_counter -= 7
        else:
            self.heights = []
            self.height_step = 0
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

    def kill(self, delay: int):
        self.value = -1

        self.animation_frames  = [self.image for _ in range(delay * 3)]
        self.animation_frames += [self.flash_solid for _ in range(2)]
        self.animation_frames += [self.flash_wireframe for _ in range(2)]
        self.animation_frames += [self.flash_solid for _ in range(2)]

        self.current_frame = 1

    def build_drop_animation(self, animation_delay: int):
        animation_frames = 40 + randint(-4, 4)
        delay = animation_delay
        starting_height = 320
        self.heights = [
            pytweening.easeInQuad((n / animation_frames)) * starting_height \
                for n in range(animation_frames + 1)
        ]
        self.heights += [starting_height for _ in range(delay)]
        self.heights.reverse()
        self.height_step = 1

    def build_flyaway_animation(self):
        animation_frames = self.fade_counter // 7
        target_height = 50 + randint(0, 16)
        self.heights = [
            pytweening.easeInQuad((n / animation_frames)) * target_height \
                for n in range(animation_frames + 1)
        ]
        self.height_step = 1

    def draw(self):
        pass

    def get_height(self) -> float:
        if self.heights:
            return self.heights[self.height_step]
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

    def update(self):
        self.animate()
        # self.draw()
