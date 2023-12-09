
### third-party imports

from pygame.locals import (

    QUIT,

    KEYDOWN,
    K_ESCAPE,

)


### local imports

from ....config import REFS, SOUND_MAP, quit_game

from ....pygamesetup import SERVICES_NS

from ....pygamesetup.constants import GAMEPAD_PLUGGING_OR_UNPLUGGING_EVENTS

from ....pygamesetup.gamepaddirect import setup_gamepad_if_existent



class TeleportingIn:

    def teleporting_in_control(self):

        for event in SERVICES_NS.get_events():

            if event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_game()

            elif event.type in GAMEPAD_PLUGGING_OR_UNPLUGGING_EVENTS:
                setup_gamepad_if_existent()

            elif event.type == QUIT:
                quit_game()

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
