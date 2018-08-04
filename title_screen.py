"""Title screen event loop processing

Presents the animated title screen and waits for the user to hit
a key. Then transitions off the screen.

To go to the title screen, use title_screen.go()
"""
import time
import itertools
import pygame
import pygame.locals
import pylink_config
import tile_loader
import title_waterfall
import title_intro_text

_START_TITLE_FADE_AT_SECS = 8.0
_FINISH_TITLE_FADE_AT_SECS = 16.0

def alpha_value(elapsed_secs):
    """
    Return an alpha value to fade the title out.

    Args:
        elapsed_secs: The elapsed time, in seconds, that the title has
            been displayed.

    Returns:
        An integer between 0 and 255 that can be used for the fade.
        The value 0 is completely transparent and the value 255 is
        completely opaque.
    """
    if elapsed_secs < _START_TITLE_FADE_AT_SECS:
        return 0
    if elapsed_secs > _FINISH_TITLE_FADE_AT_SECS:
        return 255
    return int(
        (elapsed_secs - _START_TITLE_FADE_AT_SECS)
        * (255.0 / _START_TITLE_FADE_AT_SECS)
    )

#pylint: disable-msg=too-many-arguments
def event_loop(
        screen,
        background_tiles,
        waterfall_background,
        waterfall_waves,
        waterfall_spray,
        intro_text):
    """
    Run the event loop for the title screen

    Args:
        screen: A pygame screen instance.
        background_tiles: An array of the tiles to loop through to
            animate the background.
        waterfall_background: The tile for the background of the
            waterfall.
        waterfall_waves: The tile for the waves on the waterfall.
        waterfall_spray: An array of the tiles to loop through to
            animate the spray at the top of the waterfall.
        intro_text: The intro text to scroll as one image.
    """
    title_frametime_msecs = 75
    shift_waves = False
    start_time_secs = time.time()

    screen.fill((0, 0, 0))
    pygame.display.flip()
    background_loop = itertools.cycle(background_tiles)
    spray_loop = itertools.cycle(waterfall_spray)
    #pylint: disable-msg=too-many-function-args
    alpha_surface = pygame.Surface(pylink_config.WINDOW_SIZE)
    #pylint: enable-msg=too-many-function-args
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(0)
    while 1:
        elapsed_secs = time.time() - start_time_secs
        if elapsed_secs >= 82.75:
            elapsed_secs = 0
            start_time_secs = time.time()
            pygame.mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return

        if elapsed_secs < _FINISH_TITLE_FADE_AT_SECS:
            # Show waterfall
            screen.blit(next(background_loop), (0, 0))
            screen.blit(next(spray_loop), (237, 528))
            screen.blit(waterfall_background, (240, 543))
            if shift_waves:
                screen.blit(waterfall_waves, (240, 543))
            else:
                screen.blit(waterfall_waves, (240, 513))
            shift_waves = not shift_waves
            alpha_surface.set_alpha(alpha_value(elapsed_secs))
            screen.blit(alpha_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(title_frametime_msecs)
        elif 16 <= elapsed_secs < 23.5:
            # scroll intro story up
            screen.fill((0, 0, 0))
            screen.blit(
                intro_text,
                title_intro_text.location(elapsed_secs)
            )
            pygame.display.flip()
        elif 23.5 <= elapsed_secs < 27.5:
            # pause intro story
            pass
        elif 27.5 <= elapsed_secs < 74.5:
            # scroll rest of intro/items list
            screen.fill((0, 0, 0))
            screen.blit(
                intro_text,
                title_intro_text.location(elapsed_secs)
            )
            pygame.display.flip()
        elif elapsed_secs >= 74.5:
            # pause item list
            pass
#pylint: enable-msg=too-many-arguments

def execute(game_screen):
    """
    Show the title screen and waits for the user to hit 'start'

    Args:
        game_screen: A pygame screen instance.

    Returns:
        Nothing.

    """
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=pylink_config.NES_WINDOW_SIZE,
        border=(3, 3),
        offset=(0, 1),
        final_tile_size=pylink_config.WINDOW_SIZE)
    # When the animation loop runs, the same background is shown
    # for two frames in a row. The waterfall, moves at twice the rate
    # and this allows for that movement to occur on every loop through.
    # Note that the background images undulate back and forth through
    # the list
    background_tiles = [
        table[0][0], table[0][0],
        table[0][1], table[0][1],
        table[1][0], table[1][0],
        table[1][1], table[1][1],
        table[1][0], table[1][0],
        table[0][1], table[0][1]
    ]
    table = tile_loader.load_tile_table(
        filename="assets/NES-TheLegendofZelda-IntroAndFileSelect.png",
        original_tile_size=(32, 59),
        border=(6, 0),
        offset=(340, 51),
        final_tile_size=pylink_config.WINDOW_SIZE)
    waterfall_background = title_waterfall.background()
    waterfall_waves = title_waterfall.waves()
    waterfall_spray = title_waterfall.spray()
    intro_text = title_intro_text.intro_text()
    pygame.mixer.music.load('assets/01Intro.mp3')
    pygame.mixer.music.play()
    event_loop(
        game_screen,
        background_tiles,
        waterfall_background,
        waterfall_waves,
        waterfall_spray,
        intro_text
    )
    pygame.mixer.music.stop()

if __name__ == '__main__':
    # Load and display the title screen
    pygame.init()
    pygame.display.set_caption('The Legend of Zelda')
    MAIN_SCREEN = pygame.display.set_mode(pylink_config.WINDOW_SIZE)
    execute(MAIN_SCREEN)
