from random import randint
from statistics import mean

import pygame as pg

from board import Board, Info
from const import BASE_SCORE
from dice import Dice
from image import SpriteSheet
from move_queue import Move, Queue


def _convert_raw_positions_to_offsets(
    raw_positions: list[pg.math.Vector2],
    start_value: pg.math.Vector2 | None = None) -> list[pg.math.Vector2]:
    offsets = [] if start_value is None else [start_value]

    for n in range(1, len(raw_positions)):
        offsets.append(raw_positions[n] - raw_positions[n - 1])

    return offsets


def _get_avg_pos(positions: list[pg.math.Vector2]) -> pg.math.Vector2:
    x, y = mean([p.x for p in positions]), mean([p.y for p in positions])
    return pg.math.Vector2(x, y)


def _roll_d6() -> int:
    return randint(1, 6)


def _sort_by_z_index(d: Dice) -> int:
    return d.pos.y


class Game():
    def __init__(self, font: pg.font.Font):
        self.sprite_sheet = SpriteSheet()
        self.board        = Board(self.sprite_sheet)
        self.info         = Info(self.sprite_sheet, font)
        self.level        = 1
        self.move_queue   = Queue(self.sprite_sheet)
        self.num_moves    = 0
        self.paused       = False
        self.score        = 0

    def check_win(self) -> int:
        """
        Returns:
            0: At least 1 possible match remains (game continues)
            1: Some dice remain, but no possible moves (misson complete)
            2: No non-rock dice remain (mission accomplished)
            3: No legal moves remain (game over)
        """
        if not self.board.legal_move_exists:
            return 3

        counts = [0] * 7
        for die in self.board.get_all_dice():
            counts[die.value] += 1

        try:
            counts.pop(0)  # Ignore "rock" dice
            if not sum(counts):
                return 2
        except IndexError:
            return 2

        if any([c > 1 for c in counts]):
            return 0

        return 1

    def choose_die(self):
        self.board.choose_die_under_mouse()
        if self.board.chosen_die:
            if self.board.chosen_die.value:   # Can't move rock dice
                status = self.execute_move(self.board.chosen_die)
                if status == 0:  # Successful move
                    self.move_queue.advance()
                    self.num_moves += 1

    def execute_move(self, die: Dice) -> int:
        """Main game logic"""
        self.board.show_highlight = 0

        try:                # Match with bumped neighbor
            coords = self.board.get_coords_in_direction(
                die.row, die.col, self.move_queue.get_active_move().axis,
                self.move_queue.get_active_move().value)
            neighbor_die = self.board.get_die_from_coords(*coords)
            if neighbor_die:
                return self.board.try_match_and_store_score(die, neighbor_die)
            else:           # Slide
                target_coords = self.get_destination_coords(
                    die, move=self.move_queue.get_active_move())
                start_pos = self.board.get_die_pos(die.row, die.col)
                end_pos = self.board.get_die_pos(*target_coords)
                die.set_coords(*target_coords)
                die.slide(start_pos, end_pos, self.move_queue.get_active_move())
                return 0
        except IndexError:  # At edge of board
            return 2

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
        if self.move_queue.is_animating():
            return True

        for die in self.board.dice:
            if die.is_animating():
                return True

        return False

    def score_move(self):
        die_value = self.board.scoring_move['dice'][0]
        num_dice = len(self.board.scoring_move['dice'])
        total = BASE_SCORE * num_dice * 2 + die_value * self.level
        self.score += total

        self.board.spawn_score_display(
            self.board.scoring_move['pos'] + (0, -16), die_value, total)

        self.board.scoring_move = []

    def update(self, mouse_motion: bool):
        if self.board.scoring_move:
            self.score_move()

        self.board.update(mouse_motion, self.move_queue.get_active_move())

        self.move_queue.update()
        self.info.update(self.score, self.level, self.num_moves)

        if self.paused:
            return

        win_status = self.check_win()
        if win_status:
            self.win(win_status)

    def win(self, status: int):
        self.paused = True
        if status == 1:
            self.board.banner = 'puzzle_complete'
        elif status == 2:
            self.board.banner = 'puzzle_won'
        elif status == 3:
            self.board.banner = 'game_over'
