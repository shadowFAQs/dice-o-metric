from random import randint

import pygame as pg

from board import Board
from const import MOVES, SCREEN_SIZE
from dice import Dice
from image import SpriteSheet


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
                    self.execute_move(self.board.chosen_die)
                    self.advance_move_queue()

    def execute_move(self, die: Dice):
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
        blocker = self.board.get_blocker_in_direction(
            start=die, move=self.move_queue[0])
        if blocker:
            if blocker.value == die.value:
                for die in self.get_matching_neighbors(
                    matching_value = die.value, match=die):
                    die.kill()
            elif blocker.value == -1:  # No die at destination tile
                print(f'Move into empty space: {blocker}')
            else:
                print(f'No match: {blocker}')  # Bump (not allowed / no effect)

    def get_matching_neighbors(self, matching_value: int,
                               match: Dice) -> list[Dice]:
        def explore(row: int, col: int, visited: set[Dice] | None = None):
            if visited is None:
                visited = set()

            die = self.board.get_die_from_coords(row, col)
            if die in visited:
                return

            visited.add(die)

            if die.value == matching_value:
                result.add(die)

                for neighbor in self.get_neighbors(die):
                    explore(neighbor.row, neighbor.col, visited)

        result = set([match])
        explore(match.row, match.col)
        return list(result)

    def get_neighbors(self, die: Dice) -> list[Dice]:
        neighbors = []
        nw_neighbor = die.row - 1, die.col
        ne_neighbor = die.row, die.col + 1
        se_neighbor = die.row + 1, die.col
        sw_neighbor = die.row, die.col - 1
        neighbor_coords = [nw_neighbor, ne_neighbor, se_neighbor, sw_neighbor]
        for coord in neighbor_coords:
            try:
                neighbor = self.board.get_die_from_coords(*coord)
                if neighbor:
                    neighbors.append(neighbor)
            except IndexError:
                continue

        return neighbors

    def update(self, mouse_motion: bool):
        self.board.update(mouse_motion)
