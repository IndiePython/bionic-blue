
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,

    KEYDOWN,
    K_ESCAPE,

)

from pygame.event import get as get_events


### local import
from ....config import REFS, SOUND_MAP



class TeleportingIn:

    def teleporting_in_control(self):

        for event in get_events():

            if event.type == QUIT:
                quit_pygame()
                quit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_pygame()
                    quit()

    def teleporting_in_update(self):

        ap = self.aniplayer

        if ap.anim_name == 'materializing':

            surf_indices = ap.timing['materializing']['body']['surface_indices']

            if surf_indices.get_original_index(0) == 0:
                SOUND_MAP['blue_shooter_man_materialization.wav'].play()

            if surf_indices.peek_loops_no(1) == 1:
                self.set_state('idle_right')
                REFS.enable_player_tracking()
