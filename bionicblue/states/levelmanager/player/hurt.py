
### third-party imports

from pygame.locals import (

    QUIT,

    KEYDOWN,
    KEYUP,
    K_j,
    K_ESCAPE,

)



### local imports

from ....config import quit_game

from ....constants import (
    DAMAGE_STANCE_FRAMES,
    DAMAGE_REBOUND_FRAMES,
)

from ....pygamesetup import SERVICES_NS

from ....pygamesetup.constants import GENERAL_NS



class Hurt:

    def hurt_control(self):

        ###

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit_game()

            elif event.type == KEYUP:

                if event.key == K_j:
                    self.stop_charging()

    def hurt_update(self):

        x = self.rect.x

        self.rect.x += self.x_speed

        current_frame = GENERAL_NS.frame_index

        if current_frame - self.last_damage >= DAMAGE_STANCE_FRAMES:

            self.x_speed = 0

            ap = self.aniplayer

            new_state = (
                'idle_right'
                if 'right' in ap.anim_name
                else 'idle_left'
            )

            self.set_state(new_state)

            ap.switch_animation(
                ##
                (
                    'idle_climbing_right'
                    if new_state == 'idle_right'
                    else 'idle_climbing_left'
                )
                if self.ladder

                ##
                else new_state

            )

        if self.charge_start:
            self.check_charge()

        if not self.ladder:

            if self.rect.x != x:
                self.avoid_blocks_horizontally()

            self.react_to_gravity()

        if current_frame - self.last_damage > DAMAGE_REBOUND_FRAMES:
            self.check_invisibility()
