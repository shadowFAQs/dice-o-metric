from board import Board
from image import SpriteSheet


class Game():
    def __init__(self):
        self.sprite_sheet = SpriteSheet()
        self.board = Board(sprite_sheet=self.sprite_sheet)

    def update(self):
        self.board.update()
