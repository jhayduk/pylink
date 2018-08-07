"""Title screen event loop processing

Presents the animated title screen and waits for the user to hit
a key. Then transitions off the screen.

To go to the title screen, use title_screen.execute()
"""
import time
import itertools
import pygame
import pygame.locals
import pylink_config
import tile_loader
import title_waterfall
import title_intro_text
import game_screen

_START_TITLE_FADE_AT_SECS = 8.0
_FINISH_TITLE_FADE_AT_SECS = 16.0
_PAUSE_STORY_SCROLL_AT_SECS = 23.5
_RESUME_STORY_SCROLL_AT_SECS = 27.5
_FINISH_STORY_SCROLL_AT_SECS = 74.5
_RESTART_TITLE_SHOT_AT_SECS = 82.75

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

#pylint: disable-msg=too-many-branches
def event_loop(
        background_tiles,
        waterfall_background,
        waterfall_waves,
        waterfall_spray,
        intro_text):
    """
    Run the event loop for the title screen

    Args:
        background_tiles: An array of the tiles to loop through to
            animate the background.
        waterfall_background: The tile for the background of the
            waterfall.
        waterfall_waves: The tile for the waves on the waterfall.
        waterfall_spray: An array of the tiles to loop through to
            animate the spray at the top of the waterfall.
        intro_text: The intro text to scroll as one image.

    Returns:
        continue: True if the game should continue when this returns
            and False if it should exit.
    """
    title_frametime_msecs = 75
    shift_waves = False

    game_screen.fill((0, 0, 0))
    pygame.display.flip()
    start_time_secs = time.time()
    pygame.mixer.music.play()
    background_loop = itertools.cycle(background_tiles)
    spray_loop = itertools.cycle(waterfall_spray)
    #pylint: disable-msg=too-many-function-args
    alpha_surface = pygame.Surface(pylink_config.WINDOW_SIZE)
    #pylint: enable-msg=too-many-function-args
    alpha_surface.fill((0, 0, 0))
    alpha_surface.set_alpha(0)
    while 1:
        elapsed_secs = time.time() - start_time_secs
        if elapsed_secs >= _RESTART_TITLE_SHOT_AT_SECS:
            elapsed_secs = 0
            start_time_secs = time.time()
            pygame.mixer.music.play()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return False
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                return True

        if elapsed_secs < _FINISH_TITLE_FADE_AT_SECS:
            # Show waterfall from the start of the display of the
            # title shot until it fully fades out
            game_screen.blit(next(background_loop), (0, 0))
            game_screen.blit(next(spray_loop), (237, 528))
            game_screen.blit(waterfall_background, (240, 543))
            if shift_waves:
                game_screen.blit(waterfall_waves, (240, 543))
            else:
                game_screen.blit(waterfall_waves, (240, 513))
            shift_waves = not shift_waves
            alpha_surface.set_alpha(alpha_value(elapsed_secs))
            game_screen.blit(alpha_surface, (0, 0))
            pygame.display.flip()
            pygame.time.wait(title_frametime_msecs)
        elif elapsed_secs < _PAUSE_STORY_SCROLL_AT_SECS:
            # Once the title shot fades out, scroll the intro story up
            # until just it is displayed
            game_screen.fill((0, 0, 0))
            game_screen.blit(
                intro_text,
                title_intro_text.location(elapsed_secs)
            )
            pygame.display.flip()
        elif elapsed_secs < _RESUME_STORY_SCROLL_AT_SECS:
            # pause intro story
            pass
        elif elapsed_secs < _FINISH_STORY_SCROLL_AT_SECS:
            # scroll rest of intro/items list
            game_screen.fill((0, 0, 0))
            game_screen.blit(
                intro_text,
                title_intro_text.location(elapsed_secs)
            )
            pygame.display.flip()
        else:
            # pause item list
            pass
#pylint: enable-msg=too-many-branches

def execute():
    """
    Show the title screen and wait for the user to hit 'start'

    Returns:
        continue: True if the game should continue when this returns
            and False if it should exit.
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
    pygame.mixer.init()
    pygame.mixer.music.load('assets/01Intro.mp3')
    return_code = event_loop(
        background_tiles,
        waterfall_background,
        waterfall_waves,
        waterfall_spray,
        intro_text
    )
    pygame.mixer.music.stop()
    return return_code

if __name__ == '__main__':
    # Load and display the title screen
    game_screen.init()
    execute()
