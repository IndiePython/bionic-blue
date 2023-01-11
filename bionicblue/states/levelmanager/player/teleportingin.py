
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

            main_timing = ap.main_timing

            if main_timing.get_original_index(0) == 0:
                SOUND_MAP['blue_shooter_man_materialization.wav'].play()

            if main_timing.peek_loops_no(1) == 1:

                self.set_state('idle_right')
                self.aniplayer.switch_animation('idle_right')
                REFS.enable_player_tracking()

        self.react_to_gravity()
