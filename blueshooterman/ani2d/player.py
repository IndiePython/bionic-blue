
### standard library import
from copy import deepcopy

### third-party imports

from pygame import Rect

from pygame.math import Vector2


### local imports

from ..config import ANIM_DATA_MAP

from ..pygameconstants import blit_on_screen


class AnimationPlayer2D:

    def __init__(self, obj, anim_data_key, anim_name, pos_name, pos_value):

        self.obj = obj

        anim_data = ANIM_DATA_MAP[anim_data_key]

        self.structure = anim_data['structure']
        self.blending = anim_data['blending']
        self.values = anim_data['values']
        self.root_pos_exchange_map = anim_data['root_pos_exchange_map']
        self.timing = deepcopy(anim_data['timing'])

        self.object_map = {
            obj_name : AnimationObject2D(obj_data)
            for obj_name, obj_data in anim_data['objects'].items()
        }

        ###
        self.anim_names = self.structure.keys()

        ###

        self.root = root = self.object_map[self.structure[anim_name]['tree']['name']]
        obj.rect = root.rect
        setattr(obj.rect, pos_name, pos_value)

        ###
        self.switch_animation(anim_name)

    def blend(self, directive):

        try: anim_name = self.blending[self.anim_name][directive]
        except KeyError: return

        self.ensure_animation(anim_name)

    def switch_animation(self, anim_name):
        ###
        self.anim_name = anim_name

        ###
        self.clear_rotations()

        ###
        self.set_structure()

        ###
        self.draw = self.delayed_draw

        ###
        #self.store_animation_clock()

    def clear_rotations(self):

        for obj_timing in self.timing[self.anim_name].values():
            for key in ('surface_indices', 'position_indices'):
                obj_timing[key].restore_walking()

    def set_structure(self):

        structure = self.structure[self.anim_name]
        tree = structure['tree']

        root = self.object_map[tree['name']]

        rect = root.rect

        if root is not self.root:

            self.exchange_root_pos(self.root, root)
            self.obj.rect = root.rect

        self.root = root

        ###

        self.root.parent = None
        self.set_parent_references(root, tree.get('children', ()))

        ###
        for key in ('updating_order','drawing_order','object_names'):
            setattr(self, key, structure[key])

    def exchange_root_pos(self, previous_root, new_root):

        exchange_map = self.root_pos_exchange_map
        prev_attr_name, (new_attr_name, offset) = exchange_map[previous_root.name][new_root.name]
        pos = getattr(previous_root.rect, prev_attr_name)
        setattr(new_root.rect, new_attr_name, pos + offset)

    def set_parent_references(self, parent, children_data):

        obmap = self.object_map

        for child_data in children_data:

            child = obmap[child_data['name']]

            child.parent = parent

            self.set_parent_references(
                child,
                child_data.get('children', ())
            )

    def no_walk_pos_update(self):

        anim_name = self.anim_name

        anim_values = self.values[anim_name]
        anim_timing = self.timing[anim_name]

        obmap = self.object_map

        for obj_name in self.updating_order:

            values = anim_values[obj_name]
            timing = anim_timing[obj_name]

            pos_index = timing['position_indices'][0]

            obj = obmap[obj_name]
            obj.set_pos(values['positions'][pos_index])

    def ensure_animation(self, anim_name):
        if self.anim_name != anim_name:
            self.switch_animation(anim_name)

    def normal_draw(self):

        ###
        obmap = self.object_map

        ### 

        anim_name = self.anim_name

        anim_values = self.values[anim_name]
        anim_timing = self.timing[anim_name]

        for obj_name in self.updating_order:

            values = anim_values[obj_name]
            timing = anim_timing[obj_name]

            timing['surface_indices'].walk(1)
            surf_index = timing['surface_indices'][0]

            timing['position_indices'].walk(1)
            pos_index = timing['position_indices'][0]

            obj = obmap[obj_name]
            obj.image = values['surfaces'][surf_index]
            obj.set_pos(values['positions'][pos_index])

        ###

        for obj_name in self.drawing_order:
            obmap[obj_name].draw()

    def delayed_draw(self):

        ###
        obmap = self.object_map

        ### 

        anim_name = self.anim_name

        anim_values = self.values[anim_name]
        anim_timing = self.timing[anim_name]

        for obj_name in self.updating_order:

            values = anim_values[obj_name]
            timing = anim_timing[obj_name]

            surf_index = timing['surface_indices'][0]

            pos_index = timing['position_indices'][0]

            obj = obmap[obj_name]
            obj.image = values['surfaces'][surf_index]
            obj.set_pos(values['positions'][pos_index])

        ###

        for obj_name in self.drawing_order:
            obmap[obj_name].draw()

        ###
        self.draw = self.normal_draw


class AnimationObject2D:

    def __init__(self, obj_data):

        size = obj_data['size']
        self.rect = Rect(0, 0, *size)
        self.art_rect = Rect(0, 0, *obj_data.get('art_size', size))
        self.art_anchorage = obj_data.get('art_anchorage', ('center', 'center'))
        self.anchorage_offset = Vector2(obj_data.get('anchorage_offset', (0, 0)))

    def draw(self):
        blit_on_screen(self.image, self.art_rect)

    def set_pos(self, pos):

        ### position art

        pos_from, pos_to = self.art_anchorage
        art_pos = getattr(self.rect, pos_from) + self.anchorage_offset
        setattr(self.art_rect, pos_to, art_pos)

        ### position relative to parent, if applicable
        ### if self.parent ...
