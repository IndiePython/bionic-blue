
### third-party imports

from pygame import (
    quit as quit_pygame,
    Surface,
)

from pygame.locals import QUIT

from pygame.color import THECOLORS

from pygame.display import update


### local imports

from ...config import (
    BLOCKS, BLOCKS_ON_SCREEN,
    ACTORS, ACTORS_ON_SCREEN,
    PROJECTILES,
    FRONT_PROPS,
    execute_tasks
)

from ...pygameconstants import (
    screen_colliderect, blit_on_screen, SCREEN_RECT, SCREEN
)

from ...ourstdlibs.behaviour import do_nothing

from .player import Player

from .blocks.asphaltblock import AsphaltBlock

from .actors.gruntbot import GruntBot


LAYER_DATA_PAIRS = [
    (BLOCKS, 'blocks'),
    (ACTORS, 'actors'),
]


class LevelManager:

    def __init__(self):

        self.control = self.control_player

        ###

        self.camera_tracking_area = SCREEN_RECT.copy()
        self.camera_tracking_area.w //= 5
        self.camera_tracking_area.h += -40
        self.camera_tracking_area.center = SCREEN_RECT.center

        self.disable_player_tracking()

        ###
        self.floor_level = 124

    def enable_player_tracking(self):
        self.camera_tracking_routine = self.track_player

    def disable_player_tracking(self):
        self.camera_tracking_routine = do_nothing

    def prepare(self):

        if not hasattr(self, 'player'):
            self.player = Player()

        self.state = self

        ### instantiate objects

        level_data = {

            'background_color': (69, 174, 255),

            'layered_objects': {

                'blocks': [
                    {
                        'name': 'asphalt_block',
                        'size': (16, 100),
                        'pos_name': 'bottomleft',
                        'pos_value': (0, 124),
                    },
                    {
                        'name': 'asphalt_block',
                        'size': (320, 16),
                        'pos_name': 'bottomleft',
                        'pos_value': (0, 140),
                    },
                    {
                        'name': 'asphalt_block',
                        'size': (160, 16),
                        'pos_name': 'bottomleft',
                        'pos_value': (320, 140),
                    },
                    {
                        'name': 'asphalt_block',
                        'size': (320, 16),
                        'pos_name': 'bottomleft',
                        'pos_value': (480, 100),
                    },
                    {
                        'name': 'asphalt_block',
                        'size': (16, 30),
                        'pos_name': 'bottomleft',
                        'pos_value': (520, 84),
                    },

                ],

                'actors': [
                    {
                        'name': 'grunt_bot',
                        'pos_name': 'midbottom',
                        'pos_value': (260, 124),
                    },
                    {
                        'name': 'grunt_bot',
                        'pos_name': 'midbottom',
                        'pos_value': (360, 124),
                    },
                    {
                        'name': 'grunt_bot',
                        'pos_name': 'midbottom',
                        'pos_value': (490, 84),
                    },
                    {
                        'name': 'grunt_bot',
                        'pos_name': 'midbottom',
                        'pos_value': (660, 84),
                    },
                ],

            },

        }

        ### bg

        self.bg = Surface((320, 180)).convert()
        self.bg.fill(level_data['background_color'])

        ###
        layered_objects = level_data['layered_objects']

        for layer, layer_name in LAYER_DATA_PAIRS:

            try: objs_data = layered_objects[layer_name]
            except KeyError: continue

            for obj_data in objs_data:
                layer.add(instantiate(obj_data))

    def control_player(self):
        self.player.control()

    def update(self):
        
        BLOCKS_ON_SCREEN.clear()
        BLOCKS_ON_SCREEN.update(
            block
            for block in BLOCKS
            if screen_colliderect(block.rect)
        )

        for block in BLOCKS_ON_SCREEN:
            block.update()

        self.player.update()

        ACTORS_ON_SCREEN.clear()
        ACTORS_ON_SCREEN.update(
            actor
            for actor in ACTORS
            if screen_colliderect(actor.rect)
        )

        for actor in ACTORS_ON_SCREEN:
            actor.update()

        for projectile in PROJECTILES:
            projectile.update()

        for prop in FRONT_PROPS:
            prop.update()


        ###
        execute_tasks()

        ###
        self.camera_tracking_routine()

        ###
        self.floor_level_routine()

    def track_player(self):

        player_rect = self.player.rect

        clamped_rect = player_rect.clamp(self.camera_tracking_area)

        if clamped_rect != player_rect:

            diff = tuple(a - b for a, b in zip(clamped_rect.topleft, player_rect.topleft))
            self.move_level(diff)

    def floor_level_routine(self):

        if self.player.midair: return

        y_diff = self.player.rect.bottom - self.floor_level

        if y_diff:
            
            multiplier = (
                1
                if abs(y_diff) == 1
                else 2
            )

            dy = (-1 if y_diff > 0 else 1) * multiplier

            self.move_level((0, dy))

    def move_level(self, diff):

        for block in BLOCKS:
            block.rect.move_ip(diff)

        for actor in ACTORS:
            actor.rect.move_ip(diff)

        self.player.rect.move_ip(diff)

        for projectile in PROJECTILES:
            projectile.rect.move_ip(diff)

        for prop in FRONT_PROPS:
            prop.rect.move_ip(diff)

    def draw(self):

        blit_on_screen(self.bg, (0, 0))

        for projectile in PROJECTILES:
            projectile.draw()

        for block in BLOCKS_ON_SCREEN:
            block.draw()

        self.player.draw()

        for actor in ACTORS_ON_SCREEN:
            actor.draw()

        for prop in FRONT_PROPS:
            prop.draw()

        ############################
#        from pygame.draw import rect, line
#
#        cam_area = self.camera_tracking_area
#
#        rect(SCREEN, 'red', cam_area, 1)
#
#        line(
#            SCREEN,
#            'magenta',
#            (cam_area.left , self.floor_level),
#            (cam_area.right-1, self.floor_level),
#            1,
#        )
        ############################

        update()

    def next(self):
        return self.state


def instantiate(obj_data):

    name = obj_data['name']

    if name == 'asphalt_block':
        return AsphaltBlock(**obj_data)

    elif name == 'grunt_bot':
        return GruntBot(**obj_data)
