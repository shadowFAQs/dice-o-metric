from pathlib import Path
from random import randint

import pygame as pg
from shapely import Point, Polygon

from const import Color, BOARD_POS, DIE_SPRITE_SIZE, SCREEN_SIZE, \
                  SCORE_LETTER_SIZE, SCORE_LETTER_WIDTHS, TILE_GAP, TILE_SIZE
from dice import Dice
from image import SpriteSheet


class Board(pg.sprite.Sprite):
    def __init__(self, sprite_sheet: SpriteSheet):
        pg.sprite.Sprite.__init__(self)

        self.sprite_sheet     = sprite_sheet

        self.chosen_die       = None
        self.num_cols         = 8
        self.num_rows         = 8
        self.score_displays   = []
        self.scoring_move     = {}

        self.color            = Color()
        self.dice             = []
        self.shadows          = []
        self.highlight_coords = pg.math.Vector2(0, 0)
        self.show_highlight   = 0  # [-1, 0, 1]

        self.background_image = pg.image.load(Path('img') / 'bg.bmp')
        self.rect = self.background_image.get_rect()
        self.image = pg.Surface(self.rect.size, pg.SRCALPHA)  # (320, 304)

        self.spawn_dice()

    def choose_die_under_mouse(self):
        self.chosen_die = self.get_hovered_die()

    def draw(self):
        self.image.fill(self.color.black)
        self.image.blit(self.background_image, (0, 0))

        for shadow_pos in self.shadows:
            self.image.blit(self.sprite_sheet.shadow, shadow_pos)

        for die in self.get_all_dice(sort=True):
            self.image.blit(die.get_image(), die.pos)

        if self.show_highlight:
            highlight = self.sprite_sheet.highlight \
                if self.show_highlight == 1 else self.sprite_sheet.dimlight
            self.image.blit(highlight, self.highlight_coords)

        for score_display in self.score_displays:
            self.image.blit(score_display['image'], score_display['pos'])

    def get_all_dice(self, sort: bool = False) -> list[Dice]:
        """Returns flattened list from 2D list"""
        if not sort:
            return self.dice

        return sorted(self.dice, key=lambda d: d.z_index)  # Sort by draw order

    def get_coords_in_direction(self, start_row: int, start_col: int, axis: str,
                                value: int) -> tuple[int]:
        if axis == 'row':
            if not -1 < start_row + value < 8:
                raise IndexError
            return start_row + value, start_col
        else:
            if not -1 < start_col + value < 8:
                raise IndexError
            return start_row, start_col + value

    def get_die_from_coords(self, row: int, col: int) -> Dice | None:
        if not (-1 < col < 8) or not (-1 < row < 8):
            raise IndexError

        try:
            return [d for d in self.dice if d.row == row and d.col == col][0]
        except IndexError:
            return None

    def get_die_pos(self, row: int, col: int) -> pg.math.Vector2:
        """Translates row & col into pixel position"""
        x_step = TILE_SIZE.x / 2 + TILE_GAP
        y_step = TILE_SIZE.y / 2 + TILE_GAP

        x = (self.rect.width - (DIE_SPRITE_SIZE.x * 8 + 14 * TILE_GAP)) // 2
        y = self.rect.height - DIE_SPRITE_SIZE.y * 3
        x += x_step * col
        y -= y_step * col
        x += x_step * row
        y += y_step * row

        return pg.math.Vector2(x, y)

    def get_hovered_die(self) -> Dice | None:
        mouse_pos = self.get_mouse_pos()
        if self.rect.collidepoint(mouse_pos):
            mouse_point = Point(mouse_pos)

            for die in self.get_all_dice():
                hitbox = Polygon(
                    (die.pos + (0, 8), die.pos + (15, 0),
                     die.pos + (31, 8), die.pos + (15, 16))
                )
                if hitbox.contains(mouse_point):
                    return die

        return None

    def get_matching_neighbors(self, matching_value: int,
                               match: Dice) -> list[Dice]:
        def explore(row: int, col: int, visited: set[Dice] | None = None):
            if visited is None:
                visited = set()

            die = self.get_die_from_coords(row, col)
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

    def get_mouse_pos(self) -> pg.math.Vector2:
        return (
            pg.mouse.get_pos() - BOARD_POS) / 2 - (TILE_GAP * 2, TILE_GAP * 2)

    def get_neighbor_in_direction(self, start: Dice,
                                  move: 'Move') -> Dice | None:
        if move.axis == 'row':
            return self.get_die_from_coords(row=start.row + move.value,
                                            col=start.col)
        else:
            return self.get_die_from_coords(row=start.row,
                                            col=start.col + move.value)

    def get_neighbors(self, die: Dice) -> list[Dice]:
        neighbors = []
        nw_neighbor = (die.row - 1, die.col)
        ne_neighbor = (die.row, die.col + 1)
        se_neighbor = (die.row + 1, die.col)
        sw_neighbor = (die.row, die.col - 1)
        neighbor_coords = [nw_neighbor, ne_neighbor, se_neighbor, sw_neighbor]
        for coord in neighbor_coords:
            try:
                neighbor = self.get_die_from_coords(*coord)
                if neighbor:
                    neighbors.append(neighbor)
            except IndexError:
                continue

        return neighbors

    def highlight_hovered_die(self):
        die = self.get_hovered_die()
        if die:
            if die.offsets:  # Don't highlight during animation
                self.show_highlight = 0
                return

            match die.value:
                case -1:  # Empty space; don't show highlight on hover
                    self.show_highlight = 0
                case 0:   # Rock die; show dim highlight
                    self.highlight_coords = die.pos
                    self.show_highlight = -1
                case _:
                    self.highlight_coords = die.pos
                    self.show_highlight = 1
        else:
            self.show_highlight = 0

    def remove_die(self, die: Dice):
        self.dice.pop(self.dice.index(die))

    def spawn_dice(self):
        from game import _roll_d6

        image = self.sprite_sheet.dice
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if _roll_d6() > 1:  # ~17% of spaces should be empty
                    animation_delay = row * 5 + col * 2 + randint(0, 8)
                    value = randint(0, 6)
                    image = self.sprite_sheet.dice[value]
                    ghost_image = self.sprite_sheet.dice_ghosts[value]
                    images = {
                    'image': image,
                    'ghost': ghost_image,
                    'flash_solid': pg.Surface((DIE_SPRITE_SIZE), pg.SRCALPHA),
                    'flash_wireframe': pg.Surface((DIE_SPRITE_SIZE),
                                                   pg.SRCALPHA)
                    }
                    images['flash_solid'].blit(
                        self.sprite_sheet.dice_flash['solid'], (0, 0))
                    images['flash_wireframe'].blit(
                        self.sprite_sheet.dice_flash['wireframe'], (0, 0))
                    self.dice.append(
                        Dice(row, col, value, self.get_die_pos(row, col),
                             animation_delay, images)
                    )

                self.shadows.append(self.get_die_pos(row, col) + (0, 19))

    def spawn_score_display(self, pos: pg.math.Vector2, die_value: int,
                            points: int):
        text = f'+{points}'
        width = sum([SCORE_LETTER_WIDTHS[letter] for letter in text])
        image = pg.Surface((width, SCORE_LETTER_SIZE.y), pg.SRCALPHA)
        offset_x = 0
        for letter in text:
            image.blit(self.sprite_sheet.score_font[letter], (offset_x, 0))
            offset_x += SCORE_LETTER_WIDTHS[letter]

        self.score_displays.append({'counter': 60, 'image': image, 'pos': pos})

    def try_match_and_store_score(self, die: Dice, neighbor: Dice) -> int:
        from game import _get_avg_pos

        scoring_move = {'dice': [], 'pos': None}
        positions = []

        if neighbor.value == die.value:
            for n, die in enumerate(
                self.get_matching_neighbors(
                    matching_value = die.value, match=die)):
                scoring_move['dice'].append(die.value)
                positions.append(die.pos)
                die.kill(delay=n)

            scoring_move['pos'] = _get_avg_pos(positions)
            self.scoring_move = scoring_move
            return 0

        return 1

    def update(self, mouse_motion: bool):
        if mouse_motion:
            self.highlight_hovered_die()

        for die in self.get_all_dice():
            die.update()

            if not die.is_animating():
                if die.slide_direction:
                    try:
                        coords = self.get_coords_in_direction(
                            die.row, die.col, die.slide_direction['axis'],
                            die.slide_direction['value'])
                        neighbor_die = self.get_die_from_coords(*coords)
                        self.try_match_and_store_score(die, neighbor_die)
                    except IndexError:  # Bumped into edge of board
                        pass
                    finally:
                        die.end_slide()

                elif die.value == -1:
                    self.remove_die(die)

        if self.score_displays:
            self.score_displays = [s for s in self.score_displays \
                                   if s['counter']]
            for score_display in self.score_displays:
                score_display['counter'] -= 1

        self.draw()


class Info():
    def __init__(self, sprite_sheet: SpriteSheet, font: pg.font.Font):
        self.sprite_sheet = sprite_sheet

        self.color = Color()
        self.font = font
        self.image = self.sprite_sheet.info_bg.copy()

    def update(self, score: int, level: int, moves: int):
        self.image.fill(self.color.black)
        self.image.blit(self.sprite_sheet.info_bg, (0, 0))

        for n, text in enumerate([score, level, moves]):
            image = self.font.render(str(text), False, self.color.white)
            self.image.blit(image, (128 - image.get_width(), 40 + n * 30))
