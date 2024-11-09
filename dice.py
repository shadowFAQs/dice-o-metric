from pathlib import Path
from random import randint

import pygame as pg
import pytweening

from const import Color


class Dice(pg.sprite.Sprite):
    def __init__(self, row: int, col: int, value: int, coords: pg.math.Vector2,
                 animation_delay: int, image: pg.Surface):
        pg.sprite.Sprite.__init__(self)

        self.row     = row
        self.col     = col
        self.value   = value
        self.coords  = coords  # Pixel coords (where to draw)
        self.heights = []
        self.image   = image
        self.rect    = self.image.get_rect()

        self.color   = Color()

        self.build_height_animation(animation_delay)

    def __repr__(self) -> str:
        return f'Die {self.value} @ ({self.col},{self.row})'

    def animate_descent(self):
        """Handles "falling" animation at stage load"""
        if self.height_step:
            self.height_step -= 1
        else:
            self.heights = []

    def build_height_animation(self, animation_delay: int):
        animation_frames = 40 + randint(-4, 4)
        delay = animation_delay
        starting_height = 320
        self.heights = [
            pytweening.easeInQuad((n / animation_frames)) * starting_height \
            for n in range(animation_frames + 1)
        ]
        self.heights += [starting_height for _ in range(delay)]
        self.height_step = len(self.heights) - 1

    def draw(self):
        pass

    def get_height(self) -> float:
        if self.heights:
            return self.heights[self.height_step]
        else:
            return 0

    def update(self):
        self.animate_descent()
        # self.draw()
