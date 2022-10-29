
### standard library imports

from collections import defaultdict

from itertools import permutations


### third-party imports

from pygame import Surface

from pygame.math import Vector2

from pygame.transform import flip as flip_surface


### local imports

from ..ourstdlibs.pyl import load_pyl

from ..ourstdlibs.wdeque.main import WalkingDeque

from ..ourstdlibs.tree import get_tree_values



TRANSP_COLORKEY = (192, 192, 192)
EMPTY_SURF = Surface((0, 0)).convert()


def process_animation_data(animation_dir):

    metadata_path = next(p for p in animation_dir.iterdir() if p.suffix.lower() == '.pyl')
    metadata = load_pyl(str(metadata_path))

    ###

    geometry_data = metadata['geometry']

    objects = {}

    for obj_name, obj_data in metadata['objects'].items():
        objects[obj_name] = geometry_data[obj_data['geometry']]


    ###
    existing_structures = metadata['existing_structures']

    for struct_data in existing_structures.values():

        ###
        tree = struct_data['tree']
        optional_order = tuple(get_tree_values(tree, 'name', 'children'))

        ###

        for key in ('updating_order', 'drawing_order'):

            try: struct_data[key]
            except KeyError:
                struct_data[key] = optional_order

        ###
        struct_data['object_names'] = optional_order

    structures = {
        anim_name: existing_structures[anim_data['structure']]
        for anim_name, anim_data in metadata['animations'].items()
    }

    ### pxa value grabbing

    pxa_paths = [
        path
        for path in animation_dir.iterdir()
        if path.suffix.lower() == '.pxa'
    ]

    all_pxa_values = {}
    all_pxa_timing = {}

    for path in pxa_paths:

        pxa_data = load_pyl(str(path))

        pxa_values = all_pxa_values[path.stem] = {}
        pxa_timing = all_pxa_timing[path.stem] = {}

        ###

        for anim_name, anim_data in pxa_data['animations'].items():

            size = anim_data['size']

            anim_values = pxa_values[anim_name] = {}

            ###

            surfaces = anim_values['surfaces'] = []

            sprites_data = anim_data['sprites']

            base_surf = Surface((size, size)).convert()
            base_surf.fill(TRANSP_COLORKEY)
            base_surf.set_colorkey(TRANSP_COLORKEY)

            for sprite_data in sprites_data:

                surf = base_surf.copy()
                surfaces.append(surf)

                for color, points in sprite_data.items():
                    for point in points:
                        surf.set_at(tuple(map(int, point)), color)

            anim_values['positions'] = [(0, 0)]

            ###

            anim_timing = pxa_timing[anim_name] = {}

            ###

            no_of_frames = anim_data['number_of_frames']
            sprite_placement = anim_data['sprite_placement']

            surf_indices = []

            for frame_index in range(no_of_frames):

                if frame_index in sprite_placement:
                    sprite_index = sprite_placement[frame_index]

                surf_indices.append(sprite_index)


            anim_timing['surface_indices'] = tuple(surf_indices)
            anim_timing['position_indices'] = (0,)


    ### storing grabbed values and timing

    ## values

    key_default_pairs = (
        ('surfaces', (EMPTY_SURF,)),
        ('positions', ((0, 0),)),
    )

    raw_values = metadata['values']

    values = {}

    for anim_name, raw_data in raw_values.items():

        anim_values = values[anim_name] = {}

        for obj_name, raw_obj_values in raw_data.items():

            obj_values = anim_values[obj_name] = {}

            for key, default in key_default_pairs:

                if key in raw_obj_values:
                    stem, pxa_anim_name = raw_obj_values[key].split('.')
                    obj_values[key] = all_pxa_values[stem][pxa_anim_name][key]

                else:
                    obj_values[key] = default

    ## timing

    keys = ('surface_indices', 'position_indices')

    raw_timing = metadata['timing']

    timing = {}

    for anim_name, raw_data in raw_timing.items():

        anim_timing = timing[anim_name] = {}

        for obj_name, raw_obj_timing in raw_data.items():

            obj_timing = anim_timing[obj_name] = {}

            for key in keys:

                if key in raw_obj_timing:
                    stem, pxa_anim_name = raw_obj_timing[key].split('.')
                    obj_timing[key] = WalkingDeque(all_pxa_timing[stem][pxa_anim_name][key])

                else:
                    obj_timing[key] = WalkingDeque((0,))


    ### derived animations

    for anim_name, data in metadata.get('derived_animations', {}).items():

        anim_values = values[anim_name] = {}
        anim_timing = timing[anim_name] = {}

        target_anim_name = data['target']

        target_anim_values = values[target_anim_name]
        target_anim_timing = timing[target_anim_name]

        operation_name = data['operation_name']

        if operation_name == 'flip_x':

            for obj_name, target_obj_values in target_anim_values.items():

                obj_values = anim_values[obj_name] = {}

                obj_values['surfaces'] = tuple(
                    flip_surface(surf, True, False)
                    for surf in target_obj_values['surfaces']
                )

                obj_values['positions'] = target_obj_values['positions']

            ##

            for obj_name, target_obj_timing in target_anim_timing.items():

                obj_timing = anim_timing[obj_name] = {}

                for key in ('surface_indices', 'position_indices'):
                    obj_timing[key] = WalkingDeque(target_obj_timing[key])

    ###

    anim_names = tuple(metadata['animations'])
    pairs = permutations(anim_names, 2)

    exchange_map = defaultdict(dict)

    for anim_a, anim_b in pairs:
        exchange_map[anim_a][anim_b] = 'midbottom', 'midbottom', (0, 0)

    exchange_map = dict(exchange_map)
    exchange_map.update(metadata.get('root_pos_exchange_map', {}))

    for value_dict in exchange_map.values():

        for key, value in value_dict.items():

            a, b, c = value
            value_dict[key] = a, b, Vector2(c)

    ###

    return {
      'objects': objects,
      'structure': structures,
      'blending': metadata.get('blending', {}),
      'values': values,
      'timing': timing,
      'root_pos_exchange_map': exchange_map,
    }
