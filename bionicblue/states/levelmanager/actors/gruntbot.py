### standard library import
from functools import partial


### third-party import
from pygame.time import get_ticks as get_msecs


### local imports

from ....config import REFS, ACTORS, FRONT_PROPS, append_task

from ....ani2d.player import AnimationPlayer2D

from ....ourstdlibs.behaviour import do_nothing

from ..frontprops.defaultexplosion import DefaultExplosion


class GruntBot:

    def __init__(self, name, pos):

        self.health = 5

        self.player = REFS.states.level_manager.player

        self.name = name

        self.aniplayer = (
            AnimationPlayer2D(
                self, name, 'idle_left', 'midbottom', pos
            )
        )

        self.last_damage = get_msecs()
        self.routine_check = do_nothing

    def update(self):

        if self.player.rect.colliderect(self.rect):
            self.player.damage(3)

        self.routine_check()

    def check_damage_whitening(self):

        if get_msecs() - self.last_damage > 70:

            self.aniplayer.restore_surface_cycling()
            self.routine_check = do_nothing

    def draw(self):
        self.aniplayer.draw()

    def damage(self, amount):

        self.health += -amount

        if self.health <= 0:

            center = self.rect.center

            FRONT_PROPS.add(DefaultExplosion('center', center))
            append_task(partial(ACTORS.remove, self,))

        else:
            self.aniplayer.set_custom_surface_cycling(('whitened', 'default'))
            self.routine_check = self.check_damage_whitening
