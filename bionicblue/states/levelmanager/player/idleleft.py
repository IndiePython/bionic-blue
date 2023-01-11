
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,
    K_w, K_a, K_s, K_d,

    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    K_j, K_k,

)

from pygame.event import get as get_events

from pygame.key import get_pressed as get_pressed_state


### local imports

from ....config import (
    REFS,
    PROJECTILES,
    SHOOTING_STANCE_MSECS,
    DAMAGE_REBOUND_MSECS,
)

from .projectiles.default import DefaultProjectile
from .projectiles.chargedshot import ChargedShot



class IdleLeft:

    def idle_left_control(self):

        ### must get events before the pressed state, so
        ### pygame internals work as expected, which is
        ### why we store the events so we can iterate over
        ### them next

        events = get_events()
        pressed_state = get_pressed_state()

        ### iterate over events

        for event in events:

            if event.type == QUIT:
                quit_pygame()
                quit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:

                    quit_pygame()
                    quit()

                elif event.key == K_j:
                    self.idle_left_shoot()

                elif event.key == K_k:

                    if self.ladder and pressed_state[K_s]:
                        self.release_ladder()

                    else:
                        self.jump()

                elif event.key == K_w:
                    self.check_ladder()

            elif event.type == KEYUP:

                if event.key == K_j and self.charge_start:

                    result = self.stop_charging()

                    if result:
                        self.idle_left_release_charge(result)

        ###

        pressed_state = get_pressed_state()

        if self.ladder:

            ap = self.aniplayer

            if REFS.msecs - self.last_shot < SHOOTING_STANCE_MSECS:
                dy = 0

            elif pressed_state[K_w]:

                dy = -1
                ap.ensure_animation('climbing')

            elif pressed_state[K_s]:

                dy = 3
                ap.ensure_animation('descending')

            else:
                dy = 0

            if dy:

                moved_rect = self.rect.move(0, dy)

                if self.ladder.rect.contains(moved_rect):
                    self.rect.y += dy

                else:

                    if moved_rect.bottom > self.ladder.rect.bottom:

                        self.ladder = None
                        self.set_state('idle_left')
                        ap.switch_animation('idle_left')

            else:

                if pressed_state[K_d]:

                    self.set_state('idle_right')
                    ap.switch_animation('idle_climbing_right')

                elif 'shooting' in ap.anim_name:
                    ap.ensure_animation('shooting_climbing_left')

                else:
                    ap.ensure_animation('idle_climbing_left')

        elif pressed_state[K_a]:

            self.x_accel += -1
            self.set_state('walk_left')
            self.aniplayer.switch_animation('walk_left')

        elif pressed_state[K_d]:

            self.x_accel += 1
            self.set_state('walk_right')
            self.aniplayer.switch_animation('walk_right')

    def idle_left_update(self):

        msecs = REFS.msecs

        if msecs - self.last_shot >= SHOOTING_STANCE_MSECS:
            self.aniplayer.blend('-shooting')

        if self.charge_start:
            self.check_charge()

        if not self.ladder:
            self.react_to_gravity()

        if msecs - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.check_invisibility()

    def idle_left_shoot(self):

        pos_value = self.rect.move(2, -2).midleft

        PROJECTILES.add(
            DefaultProjectile(
                x_orientation=-1,
                pos_name='center',
                pos_value=pos_value,
            )
        )

        if self.ladder:
            self.aniplayer.ensure_animation('shooting_climbing_left')
        else:
            self.aniplayer.blend('+shooting')

        self.charge_start = self.last_shot = REFS.msecs

    def idle_left_release_charge(self, charge_type):

        pos_value = self.rect.move(-7, -2).midleft

        PROJECTILES.add(
            ChargedShot(
                charge_type,
                x_orientation=-1,
                pos_name='center',
                pos_value=pos_value,
            )
        )

        if self.ladder:
            self.aniplayer.ensure_animation('shooting_climbing_left')
        else:
            self.aniplayer.blend('+shooting')

        self.last_shot = REFS.msecs
