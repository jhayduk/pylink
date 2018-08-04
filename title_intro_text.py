"""Scrolling intro text for the title screen."""
import pygame
import pygame.locals
import numpy
import pylink_config
import tile_loader

_FINISH_TITLE_FADE_AT_SECS = 16.0

def location(elaspsed_secs):
    """
    Return where the title should be at the given time.

    Args:
        elapsed_secs: The amount of time, in seconds, that the title
            screen itself has been displayed.

    Returns:
        The (x, y) coordinates where the top left of the intro text
            should be placed.
    """
    if elaspsed_secs < _FINISH_TITLE_FADE_AT_SECS:
        return tuple(
            map(
                int,
                numpy.multiply(
                    (2, pylink_config.NES_WINDOW_SIZE[1]),
                    pylink_config.TILE_SCALING
                )
            )
        )

    if 16.0 <= elaspsed_secs < 23.5:
        return tuple(
            map(
                int,
                numpy.multiply(
                    (
                        2,
                        pylink_config.NES_WINDOW_SIZE[1]
                        - (29.467 * (elaspsed_secs - 16.0))
                    ),
                    pylink_config.TILE_SCALING
                )
            )
        )

    if 23.5 <= elaspsed_secs < 27.5:
        return tuple(
            map(
                int,
                numpy.multiply(
                    (2, pylink_config.NES_WINDOW_SIZE[1] - 221.25),
                    pylink_config.TILE_SCALING
                )
            )
        )

    if 27.5 <= elaspsed_secs < 74.5:
        return tuple(
            map(
                int,
                numpy.multiply(
                    (
                        2,
                        pylink_config.NES_WINDOW_SIZE[1]
                        - 221.25
                        - (
                            (713.0 / (74.5 - 27.5))
                            * (elaspsed_secs - 27.5)
                        )
                    ),
                    pylink_config.TILE_SCALING
                )
            )
        )

    # elaspsed_secs >= 74.5
    return tuple(
        map(
            int,
            numpy.multiply(
                (
                    2,
                    pylink_config.NES_WINDOW_SIZE[1]
                    - 221.25
                    - (
                        (713.0 / (74.5 - 27.5))
                        * (74.5 - 27.5)
                    )
                ),
                pylink_config.TILE_SCALING
            )
        )
    )

def intro_text():
    """
    Load the intro text and treasure list.
    """
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(252, 960),
        border=(0, 0),
        offset=(523, 14),
        tile_scaling=pylink_config.TILE_SCALING,
        colorkey_location=(0, 0))
    return table[0][0]

if __name__ == '__main__':
    # Draw the loaded and scaled tiles on the screen
    pygame.init()
    MAIN_SCREEN = pygame.display.set_mode(pylink_config.WINDOW_SIZE)
    MAIN_SCREEN.fill((0, 0, 0))
    MAIN_SCREEN.blit(
        intro_text(),
        (2 * pylink_config.TILE_SCALING[0], 0)
    )
    pygame.display.flip()
    while pygame.event.wait().type != pygame.locals.QUIT:
        pass
