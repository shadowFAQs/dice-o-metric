import pygame as pg

from const import Color, BOARD_POS, INFO_POS, SCREEN_SIZE
from dice import Dice
from game import Game


def main():
    screen_2x    = pg.display.set_mode(SCREEN_SIZE)
    screen       = pg.Surface(SCREEN_SIZE / 2)
    clock        = pg.time.Clock()
    color        = Color()
    game         = Game()
    mouse_motion = False
    running      = True

    while running:
        clock.tick(30)  # FPS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEMOTION:
                mouse_motion = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if not game.is_animating():
                        game.choose_die()

        game.update(mouse_motion)

        # Draw small screen
        screen.fill(color.black)
        screen.blit(game.sprite_sheet.info_bg, INFO_POS)
        screen.blit(game.board.image, BOARD_POS)
        screen.blit(game.move_queue.image, (0, 0))

        # Double and draw 2x screen
        screen_2x.fill(color.black)
        pg.transform.scale2x(screen, screen_2x)
        pg.display.flip()

        mouse_motion = False


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Dice')

    main()
