### standard library import
from functools import partial


### local imports

from ....config import ACTORS, FRONT_PROPS, append_task

from ....ani2d.player import AnimationPlayer2D

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

    def update(self): pass

    def draw(self):
        self.aniplayer.draw()

    def damage(self, amount):

        self.health += -amount

        if self.health <= 0:

            center = self.rect.center

            FRONT_PROPS.add(DefaultExplosion('center', center))
            append_task(partial(ACTORS.remove, self,))
