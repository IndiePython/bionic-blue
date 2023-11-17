
### standard library import
from functools import partial


### third-party import
from pygame import Surface


### local imports

from .....config import (
    SOUND_MAP,
    PROJECTILES,
    ACTORS_ON_SCREEN,
    BLOCKS_ON_SCREEN,
    append_task,
)

from .....pygamesetup.constants import SCREEN_RECT, blit_on_screen


class DefaultProjectile:

    surf = Surface((3, 2)).convert()
    surf.fill('yellow')

    abs_speed = 10

    def __init__(self, x_orientation, pos_name, pos_value):

        self.x_speed = x_orientation * self.abs_speed

        self.image = self.surf
        self.rect = self.image.get_rect()
        setattr(self.rect, pos_name, pos_value)
        SOUND_MAP['default_projectile_shot.wav'].play()

    def trigger_kill(self):
        append_task(partial(PROJECTILES.remove, self))

    def update(self):

        self.rect.x += self.x_speed
        colliderect = self.rect.colliderect

        if not colliderect(SCREEN_RECT):
            self.trigger_kill()
            return

        for actor in ACTORS_ON_SCREEN:

            if colliderect(actor.rect):

                if actor.health > 0:

                    try: actor.damage(1)
                    except AttributeError:
                        pass

                    self.trigger_kill()
                    SOUND_MAP['default_projectile_hit.wav'].play()
                    return

        for block in BLOCKS_ON_SCREEN:

            if colliderect(block.rect):
                self.trigger_kill()
                return

    def draw(self):
        blit_on_screen(self.image, self.rect)
