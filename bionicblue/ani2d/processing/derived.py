
### third-party import
from pygame.transform import flip as flip_surface


### local import
from ...ourstdlibs.wdeque.main import WalkingDeque



def process_derived_animations(metadata, values, timing):

    sorted_derived_animations = sorted(

        (
            item
            for item in metadata.get('derived_animations', {}).items()
        ),

        key = lambda item: item[1].get('priority', 0)

    )

    for anim_name, data in sorted_derived_animations:

        anim_values = values[anim_name] = {}
        anim_timing = timing[anim_name] = {}

        target_anim_name = data['target']

        target_anim_values = values[target_anim_name]
        target_anim_timing = timing[target_anim_name]

        operation_name = data['operation_name']

        if operation_name == 'flip_x':

            for obj_name, target_obj_values in target_anim_values.items():

                obj_values = anim_values[obj_name] = {}

                ## surfaces

                surfc_map = obj_values['surface_collections_map'] = {}

                for version, target_surf_collection in (
                    target_obj_values['surface_collections_map'].items()
                ):

                    if version == 'invisible':
                        surfc_map[version] = target_surf_collection
                        continue

                    surfc_map[version] = tuple(
                        flip_surface(surf, True, False)
                        for surf in target_surf_collection
                    )

                ## positions
                obj_values['positions'] = target_obj_values['positions']

            ##

            for obj_name, target_obj_timing in target_anim_timing.items():

                obj_timing = anim_timing[obj_name] = {}

                for key in ('surface_indices', 'position_indices'):
                    obj_timing[key] = WalkingDeque(target_obj_timing[key])

        elif operation_name == 'backwards':

            for obj_name, target_obj_values in target_anim_values.items():

                obj_values = anim_values[obj_name] = {}

                ## surfaces

                surfc_map = obj_values['surface_collections_map'] = {}

                surfc_map.update(
                    target_obj_values['surface_collections_map']
                )

                ### positions
                obj_values['positions'] = target_obj_values['positions']


            for obj_name, target_obj_timing in target_anim_timing.items():

                obj_timing = anim_timing[obj_name] = {}

                for key in ('surface_indices', 'position_indices'):
                    obj_timing[key] = WalkingDeque(reversed(target_obj_timing[key]))
