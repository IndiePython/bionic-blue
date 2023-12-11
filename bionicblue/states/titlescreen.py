
### standard library import
from itertools import cycle


### third-party imports

from pygame.locals import QUIT

from pygame.display import update

from pygame.math import Vector2

from pygame.mixer import music


### local imports

from ..config import REFS, MUSIC_DIR, quit_game

from ..pygamesetup import SERVICES_NS

from ..pygamesetup.constants import (
    SCREEN_RECT,
    BLACK_BG,
    FPS,
    GAMEPAD_PLUGGING_OR_UNPLUGGING_EVENTS,
    KEYBOARD_OR_GAMEPAD_PRESSED_EVENTS,
    blit_on_screen,
)

from ..pygamesetup.gamepaddirect import setup_gamepad_if_existent

from ..exceptions import SwitchStateException

from ..textman import render_text

from ..classes2d.single import UIObject2D



class TitleScreen:

    def prepare(self):

        ###

        title_rect = self.title_rect = REFS.bb_title.rect

        title_rect.midtop = SCREEN_RECT.move(0, 10).midtop

        end_midtop = title_rect.midtop

        title_rect.midbottom = SCREEN_RECT.move(0, -10).midtop

        start_midtop = title_rect.midtop

        _movement_duration_msecs = 3000 # milliseconds
        self.movement_duration_frames = round(_movement_duration_msecs / 1000 * FPS)

        self.current_movement_frame = 0
        self.last_movement_frame = self.movement_duration_frames - 1

        self.start_midtop = Vector2(start_midtop)
        self.end_midtop = Vector2(end_midtop)

        ###

        self.update = self.update_title_position

        ###

        self.press_any_button = (
            UIObject2D.from_surface(render_text('Press any button', 'regular', 16))
        )

        self.press_any_button.rect.midbottom = SCREEN_RECT.move(0, -10).midbottom

        _show_duration_msecs = 1000
        _hide_duration_msecs = 500

        show_duration_frames = round(_show_duration_msecs / 1000 * FPS)
        hide_duration_frames = round(_hide_duration_msecs / 1000 * FPS)

        self.must_draw_label = cycle(
            ((True,) * show_duration_frames)
            + ((False,) * hide_duration_frames)
        ).__next__

        self.draw_label_flag = False

        ###

        music.set_volume(.1)
        music.load(str(MUSIC_DIR / 'title_screen_by_juhani_junkala.ogg'))
        music.play(-1)

    def control(self):

        for event in SERVICES_NS.get_events():

            if event.type in KEYBOARD_OR_GAMEPAD_PRESSED_EVENTS:

                if self.update == self.update_draw_label_flag:

                    main_menu = REFS.states.main_menu
                    main_menu.prepare()

                    raise SwitchStateException(main_menu)

            elif event.type in GAMEPAD_PLUGGING_OR_UNPLUGGING_EVENTS:
                setup_gamepad_if_existent()

            elif event.type == QUIT:
                quit_game()

    def update_title_position(self):

        if self.current_movement_frame <= self.last_movement_frame:

            progress = self.current_movement_frame / self.movement_duration_frames
            self.title_rect.midtop = self.start_midtop.lerp(self.end_midtop, progress)

            REFS.blue_boy.rect.midright = self.title_rect.move(-10, 5).midleft

            self.current_movement_frame += 1

        else:
            self.update = self.update_draw_label_flag

    def update_draw_label_flag(self):
        self.draw_label_flag = self.must_draw_label()

    def draw(self):

        blit_on_screen(BLACK_BG, (0, 0))

        REFS.bb_title.draw()

        REFS.blue_boy.ap.draw()

        if self.draw_label_flag:
            self.press_any_button.draw()

        update()
