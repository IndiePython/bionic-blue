
### standard library imports
from itertools import repeat, chain


### third-party imports

from pygame import quit as quit_pygame, Surface

from pygame.locals import QUIT

from pygame.event import get as get_events

from pygame.time import get_ticks as get_msecs

from pygame.display import update

from pygame.image import load as load_image

from pygame.time import get_ticks as get_msecs

from pygame.mixer import Sound


### local imports

from ..config import (
    REFS,
    COLORKEY,
    SURF_MAP,
    ANIM_DATA_MAP,
    SOUND_MAP,
    ALPHA_IMAGES_DIR,
    NO_ALPHA_IMAGES_DIR,
    ANIMATIONS_DIR,
    SOUNDS_DIR,
)

from ..pygameconstants import MSECS_PER_FRAME, WHITE_BG, blit_on_screen

from ..textman import render_text

from ..ani2d.processing import process_animation_data


ALLOWED_SOUND_FILE_EXTENSIONS = frozenset(('.ogg', '.wav'))


### gather animation resources

class ResourceLoader:

    def __init__(self):

        self.loading_surf = render_text('loading...', 'regular', 12)

        self.resources_to_process = chain(

            zip(
                repeat(SURF_MAP),
                ALPHA_IMAGES_DIR.iterdir(),
                repeat(load_alpha_image_from_filepath),
            ),

            zip(
                repeat(SURF_MAP),
                NO_ALPHA_IMAGES_DIR.iterdir(),
                repeat(load_image_from_filepath),
            ),

            zip(
                repeat(ANIM_DATA_MAP),
                (path for path in ANIMATIONS_DIR.iterdir() if path.is_dir()),
                repeat(load_anim_from_dir),
            ),

            zip(
                repeat(SOUND_MAP),
                (
                    path for path in SOUNDS_DIR.iterdir()
                    if path.is_file()
                    if path.suffix.lower() in ALLOWED_SOUND_FILE_EXTENSIONS
                ),
                repeat(load_sound_from_filepath),
            ),

        )

        self.next_state = self

    def control(self):

        for event in get_events():

            if event.type == QUIT:

                quit_pygame()
                quit()

    def update(self):

        now = get_msecs()

        resources_to_process = self.resources_to_process

        try:

            while True:

                a_map, filepath, processing_op = next(resources_to_process)
                a_map[filepath.name] = processing_op(filepath)

                if (get_msecs() - now) >= MSECS_PER_FRAME:

                    blit_on_screen(WHITE_BG, (0, 0))
                    blit_on_screen(self.loading_surf, (10, 10))

                    break

        except StopIteration:
            logo_screen = REFS.states.logo_screen
            logo_screen.prepare()
            self.next_state = logo_screen

    def draw(self):
        update()

    def next(self):
        return self.next_state


### utility functions

def load_alpha_image_from_filepath(filepath):
    image = load_image(str(filepath)).convert_alpha()
    surf = Surface(image.get_size()).convert()
    surf.set_colorkey(COLORKEY)
    surf.fill(COLORKEY)
    surf.blit(image, (0, 0))
    return surf

def load_image_from_filepath(filepath):
    return load_image(str(filepath)).convert()

def load_anim_from_dir(dirpath):
    return process_animation_data(dirpath)

def load_sound_from_filepath(filepath):
    sound = Sound(str(filepath))
    sound.set_volume(.6)
    return sound
