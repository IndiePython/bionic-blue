
### standard library import
from itertools import chain


### third-party imports

from pygame import Surface, Rect

from pygame.draw import rect as draw_rect

from pygame.math import Vector2


### local imports

from ....config import PARTICLES_DIR, COLORKEY

from ....pygamesetup.constants import blit_on_screen

from ....ourstdlibs.pyl import load_pyl

from ....ourstdlibs.wdeque.main import WalkingDeque


rect = Rect(0, 0, 0, 0)
surfs = []

def prepare_charging_particles():

    pos_map = load_pyl(
        PARTICLES_DIR / 'charging_particles_pos_map.pyl'
    )

    all_positions = chain.from_iterable(
        positions
        for positions in pos_map.values()
    )

    max_x = min_x = max_y = min_y = 0

    for x, y in all_positions:

        max_x = max(x, max_x)
        min_x = min(x, min_x)

        max_y = max(y, max_y)
        min_y = min(y, min_y)

    width = round(max_x - min_x)
    height = round(max_y - min_y)

    rect.size = (width, height)
    offset = Vector2(rect.center)

    base_surf = Surface((width, height)).convert()
    base_surf.fill(COLORKEY)
    base_surf.set_colorkey(COLORKEY)

    frames = len(pos_map[0])

    for pos_index in range(frames):

        surf = base_surf.copy()

        for particle_index in range(8):

            pos = pos_map[particle_index][pos_index]
            draw_rect(surf, 'white', (*(pos + offset), 1, 1))

        surfs.append(surf)

prepare_charging_particles()

surfs_wdeque = WalkingDeque(surfs)
walk_surfs = surfs_wdeque.walk

surfs.clear()

def draw_charging_particles():

    rect.center = draw_charging_particles.player.rect.center
    blit_on_screen(surfs_wdeque[0], rect)
    walk_surfs(1)

draw_charging_particles.restore_animation = surfs_wdeque.restore_walking
