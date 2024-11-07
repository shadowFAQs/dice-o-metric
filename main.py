import pygame as pg

from const import Color, SCREEN_SIZE
from dice import Dice
from game import Game


def main():
    screen_2x = pg.display.set_mode(SCREEN_SIZE)
    screen    = pg.Surface(SCREEN_SIZE / 2)
    clock     = pg.time.Clock()
    color     = Color()
    game      = Game()
    running   = True

    while running:
        clock.tick(30)  # FPS

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        mouse_pos = pg.mouse.get_pos()
        # if game.board.rect.collidepoint(mouse_pos):
        game.board.highlight_hovered_die(
            (mouse_pos - game.board.offset) / 2 + (0, -3))  # TODO: Why offset??

        game.update()

        # Draw small screen
        screen.fill(color.black)
        screen.blit(game.board.image, game.board.offset)
        # Double and draw 2x screen
        screen_2x.fill(color.black)
        pg.transform.scale2x(screen, screen_2x)
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Dice')

    main()
