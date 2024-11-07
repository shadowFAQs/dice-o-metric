from board import Board
from image import SpriteSheet


class Game():
    def __init__(self):
        self.sprite_sheet = SpriteSheet()
        self.board = Board(sprite_sheet=self.sprite_sheet)

    def select_die(self):
        self.board.select_die_under_mouse()

    def update(self, mouse_motion: bool):
        self.board.update(mouse_motion)
