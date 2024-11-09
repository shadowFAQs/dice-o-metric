from random import randint

import pygame as pg

from board import Board
from const import MOVES
from image import SpriteSheet


class Queue():
    def __init__(self, arrow_images: list[pg.Surface],
                 dark_arrow_images: list[pg.Surface]):
        self.arrow_images = arrow_images
        self.dark_arrow_images = dark_arrow_images

        self.moves = []
        self.max_moves = 5

        self.populate()

    def populate(self):
        while len(self.moves) < self.max_moves:
            self.moves.append(MOVES[randint(0, 3)])
            self.moves[-1]['image'] = self.arrow_images[self.moves[-1]['name']]
            self.moves[-1]['dark_image'] = self.dark_arrow_images[self.moves[-1]['name']]


class Game():
    def __init__(self):
        self.sprite_sheet = SpriteSheet()
        self.board = Board(sprite_sheet=self.sprite_sheet)

        self.move_queue = Queue(self.sprite_sheet.arrows,
                                self.sprite_sheet.dark_arrows)

    def select_die(self):
        self.board.select_die_under_mouse()

    def update(self, mouse_motion: bool):
        self.board.update(mouse_motion)
