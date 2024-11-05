from pathlib import Path
from random import randint

import pygame as pg

from const import Color


class Dice(pg.sprite.Sprite):
    def __init__(self, value: int, starting_height: int, image: pg.Surface):
        pg.sprite.Sprite.__init__(self)

        self.value = value
        self.height = starting_height
        self.image = image
        self.rect = self.image.get_rect()

        self.color = Color()

    def animate_descent(self):
        """Handles "falling" animation at stage load"""
        if self.height:
            self.height -= min(self.height // 4, 12)

    def draw(self):
        pass

    def update(self):
        self.animate_descent()
        # self.draw()
