from random import randint

import pygame as pg

from board import Board
from const import MOVES, SCREEN_SIZE
from dice import Dice
from image import SpriteSheet


def _roll_d6() -> int:
    return randint(1, 6)


def _sort_by_z_index(d: Dice) -> int:
    return d.pos.y


class Move():
    def __init__(self, name: str, axis: str, value: int):
        self.name  = name   # [ne, nw, se, sw]
        self.axis  = axis   # [row, col]
        self.value = value  # [-1, 1]

        self.image      = None
        self.dark_image = None

    def __repr__(self) -> str:
        operator = '+' if self.value > 0 else ''
        return f'Move: {self.name.upper()} ({self.axis} {operator}{self.value})'


class Queue():
    def __init__(self, arrow_images: list[pg.Surface],
                 dark_arrow_images: list[pg.Surface]):
        self.arrow_images = arrow_images
        self.dark_arrow_images = dark_arrow_images

        self.moves = []
        self.max_moves = 5

        self.populate()

    def __getitem__(self, index: int) -> Move:
        return self.moves[index]

    def pop(self):
        self.moves.pop(0)
        self.populate()

    def populate(self):
        while len(self.moves) < self.max_moves:
            self.moves.append(Move(*MOVES[randint(0, 3)]))
            self.moves[-1].image = self.arrow_images[self.moves[-1].name]
            self.moves[-1].dark_image = self.dark_arrow_images[
                self.moves[-1].name]


class Game():
    def __init__(self):
        self.sprite_sheet = SpriteSheet()
        self.board = Board(sprite_sheet=self.sprite_sheet)

        self.move_queue = Queue(self.sprite_sheet.arrows,
                                self.sprite_sheet.dark_arrows)

    def advance_move_queue(self):
        self.move_queue.pop()

    def choose_die(self):
        self.board.choose_die_under_mouse()
        if self.board.chosen_die:
            if self.board.chosen_die.value:          # Can't move rock dice
                if self.board.chosen_die.value > 0:  # Can't "move" empty spaces
                    status = self.execute_move(self.board.chosen_die)
                    if status == 0:  # Successful move
                        self.advance_move_queue()

    def execute_move(self, die: Dice) -> int:
        """
        Main game logic

        Attempts to move the selected die in the direction indicated by the
        move queue.
        If another die already occupies that spot:
            If it has the same value as the moved die, this is a "match":
                Both dice (and any other neighbors with the same value)
                are removed (recursive neighbor search) and the player's score
                increases.
            Else:
                The move is not allowed.
        Else if the die is on a board edge and the move would put it
        beyond that edge:
            The move is not allowed.
        Else (there is no die in the spot where the selected die moves):
            The moved die continues in that direction until...
                it hits a die, OR...
                    If that die has the same value:
                        This is a match, and the above match rules apply.
                    Else if that die is a rock:
                        The rock is destroyed.
                    Else:
                        The selected die stops next to the die it hits.
                ...it reaches the edge of the board.

        """
        self.board.show_highlight = 0

        try:
            coords = self.board.get_coords_in_direction(
                die.row, die.col, self.move_queue[0].axis,
                self.move_queue[0].value)
            neighbor_die = self.board.get_die_from_coords(*coords)
            if neighbor_die:
                return self.board.try_match(die, neighbor_die)
            else:  # Slide
                target_coords = self.get_destination_coords(
                    die, move=self.move_queue[0])
                start_pos = self.board.get_die_pos(die.row, die.col)
                end_pos = self.board.get_die_pos(*target_coords)
                die.set_coords(*target_coords)
                die.slide(start_pos, end_pos, self.move_queue[0])
                return 0
        except IndexError:
            return 2  # At edge of board

    def get_destination_coords(self, die: Dice, move: Move) -> tuple[int]:
        """
        Checks spaces along {axis} in {move.value} direction until
        it finds and returns coords (row, col) for:
            1. The space adjacent to another die, or
            2. The last space on the board in {move.value} direction
            along {axis}
        """
        empty_coords = (die.row, die.col)

        try:
            coords = self.board.get_coords_in_direction(
                die.row, die.col, move.axis, move.value)
            blocker = self.board.get_die_from_coords(*coords)
        except IndexError:  # Off the edge of the board
            return empty_coords

        try:
            while not blocker:
                empty_coords = coords
                coords = self.board.get_coords_in_direction(
                    coords[0], coords[1], move.axis, move.value)
                blocker = self.board.get_die_from_coords(*coords)
        except IndexError:
            return empty_coords

        return empty_coords

    def is_animating(self) -> bool:
        for die in self.board.dice:
            if die.is_animating():
                return True

        return False

    def update(self, mouse_motion: bool):
        self.board.update(mouse_motion)
