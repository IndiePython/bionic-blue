### standard library import
from functools import partial


### third-party import
from pygame.time import get_ticks as get_msecs


### local imports

from ....config import ACTORS, FRONT_PROPS, append_task

from ....ani2d.player import AnimationPlayer2D

from ....ourstdlibs.behaviour import do_nothing

from ..frontprops.defaultexplosion import DefaultExplosion


class GruntBot:

    def __init__(self, name, pos_name, pos_value):

        self.health = 5

        self.name = name

        self.aniplayer = (
            AnimationPlayer2D(
                self, name, 'idle_left', pos_name, pos_value
            )
        )

        self.last_damage = get_msecs()
        self.update = do_nothing

    def check_damage_whitening(self):

        if get_msecs() - self.last_damage > 70:

            self.aniplayer.blend('-white')
            self.update = do_nothing

    def draw(self):
        self.aniplayer.draw()

    def damage(self, amount):

        self.health += -amount

        if self.health <= 0:

            center = self.rect.center

            FRONT_PROPS.add(DefaultExplosion('center', center))
            append_task(partial(ACTORS.remove, self,))

        else:
            self.aniplayer.blend('+white')
            self.update = self.check_damage_whitening
