

### third-party imports

from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_RETURN,
    K_DOWN,
    K_UP,
)

from pygame.display import update

from pygame.mixer import music


### local imports

from ..config import (
    REFS, SOUND_MAP, MUSIC_DIR, quit_game
)

from ..pygamesetup import SERVICES_NS

from ..pygamesetup.constants import (
    SCREEN_RECT,
    BLACK_BG,
    FPS,
    blit_on_screen,
)

from ..constants import CHARGED_SHOT_SPEED

from ..ourstdlibs.behaviour import do_nothing

from ..exceptions import SwitchStateException

from ..textman import render_text

from ..classes2d.single import UIObject2D

from ..classes2d.collections import UIList2D



class MainMenu:

    def __init__(self):

        ###

        labels_data_tuples = [

            # a 3-tuple containing label title and 02 surfaces
            # representing it (unhighlighted and highlighted

            (

                label_title,

                *(
                    render_text(label_title.title(), 'regular', 16, color)
                    for color in ('cyan', 'orange')
                )

            )

            for label_title in (
                'continue',
                'new game',
                'load game',
                'options',
            )

        ]

        ###

        self.unhighlighted_surf_map = unhighlighted_surf_map = {}
        self.highlighted_surf_map = highlighted_surf_map = {}

        obj_map = {}

        for (
            title,
            unhighlighted_surf,
            highlighted_surf,
        ) in labels_data_tuples:

            unhighlighted_surf_map[title] = unhighlighted_surf
            highlighted_surf_map[title] = highlighted_surf

            obj = UIObject2D.from_surface(unhighlighted_surf)
            obj.title = title
            obj_map[title] = obj

        ###

        self.compact_items = (
            UIList2D(obj_map[title] for title in ('new game', 'options'))
        )

        self.full_items = (
            UIList2D(
                obj_map[title]
                for title in ('continue', 'new game', 'load game', 'options')
            )
        )


        self.control = self.control_item_selection
        self.update = do_nothing

    def prepare(self):

        items = self.items = self.compact_items

        self.item_count = len(items)

        items.rect.snap_rects_ip(
            retrieve_pos_from='midbottom',
            assign_pos_to='midtop', 
            offset_pos_by=(0, 5),
        )

        items.rect.midbottom = SCREEN_RECT.move(0, -10).midbottom

        self.items_left = items.rect.left

        self.current_index = 0

        REFS.blue_boy.ap.switch_animation('idle_right')

        self.highlight_selected()

    def highlight_selected(self):

        unhighlighted_surf_map = self.unhighlighted_surf_map

        for obj in self.items:
            obj.image = unhighlighted_surf_map[obj.title]

        highlighted_obj = self.items[self.current_index]
        highlighted_obj.image = self.highlighted_surf_map[highlighted_obj.title]

        REFS.blue_boy.rect.centery = highlighted_obj.rect.centery
        REFS.blue_boy.rect.right = self.items_left - 20

    def execute_selected(self):

        item_title = self.compact_items[self.current_index].title

        if item_title == 'new game':

            game_state = REFS.get_game_state()
            game_state.prepare()

            raise SwitchStateException(game_state)

    def control_item_selection(self):

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_game()

                elif event.key == K_RETURN:

                    self.control = self.control_wait_shot_animation
                    self.update  = self.update_shot_appearing

                    REFS.blue_boy.ap.blend('+shooting')
                    REFS.middle_shot.ap.switch_animation('appearing_right')

                    shot_center = REFS.blue_boy.rect.move(7, -2).midright
                    REFS.middle_shot.rect.center = shot_center

                elif event.key in (K_UP, K_DOWN):

                    increment = -1 if event.key == K_UP else 1

                    self.current_index = (self.current_index + increment) % self.item_count
                    self.highlight_selected()

    def control_wait_shot_animation(self):

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

    def update_shot_appearing(self):

        ap = REFS.middle_shot.ap

        if ap.main_timing.peek_loops_no(1) == 1:

            ap.switch_animation('idle_right')
            SOUND_MAP['middle_charged_shot_shot.wav'].play()

            self.update = self.update_shot_leaving_screen

    def update_shot_leaving_screen(self):

        shot_rect = REFS.middle_shot.rect

        shot_rect.x += CHARGED_SHOT_SPEED

        if not SCREEN_RECT.colliderect(shot_rect):

            self.control = self.control_item_selection
            self.update = do_nothing
            REFS.blue_boy.ap.switch_animation('idle_right')

            shot_rect.right = SCREEN_RECT.left

            self.execute_selected()

    def draw(self):

        blit_on_screen(BLACK_BG, (0, 0))

        REFS.bb_title.draw()

        self.items.draw()

        REFS.blue_boy.ap.draw()

        REFS.middle_shot.ap.draw()

        update()
