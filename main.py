import pygame as pg

from const import Color, BOARD_POS, MOVE_QUEUE_POS, SCREEN_SIZE
from dice import Dice
from game import Game


def main():
    screen_2x = pg.display.set_mode(SCREEN_SIZE)
    screen    = pg.Surface(SCREEN_SIZE / 2)
    clock     = pg.time.Clock()
    color     = Color()
    game      = Game()
    mouse_motion = False
    running   = True

    while running:
        clock.tick(30)  # FPS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEMOTION:
                mouse_motion = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    game.select_die()

        game.update(mouse_motion)

        # Draw small screen
        screen.fill(color.black)
        screen.blit(game.board.image, BOARD_POS)
        screen.blit(game.sprite_sheet.arrow_bg, MOVE_QUEUE_POS)
        # screen.blit(game.next_move_image, MOVE_QUEUE_POS)

        # Double and draw 2x screen
        screen_2x.fill(color.black)
        pg.transform.scale2x(screen, screen_2x)
        pg.display.flip()

        mouse_motion = False


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Dice')

    main()
