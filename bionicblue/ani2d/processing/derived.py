
### third-party import
from pygame.transform import flip as flip_surface


### local imports

from ...ourstdlibs.wdeque.main import WalkingDeque

from .constants import EMPTY_SURF, TRANSP_COLORKEY



def process_derived_animations(metadata, values, timing):

    ### derived animations

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

        elif operation_name == 'whiten':

            for obj_name, target_obj_values in target_anim_values.items():

                obj_values = anim_values[obj_name] = {}

                surfs = []

                for surf in target_obj_values['surfaces']:

                    if surf != EMPTY_SURF:

                        new_surf = surf.copy()
                        new_surf.fill(TRANSP_COLORKEY)
                        w, h = new_surf.get_size()

                        for x in range(w):

                            for y in range(h):

                                c = surf.get_at((x, y))[:3]

                                if c != TRANSP_COLORKEY:
                                    new_surf.set_at((x, y), (255, 255, 255))

                    else:
                        new_surf = EMPTY_SURF

                    surfs.append(new_surf)

                obj_values['surfaces'] = tuple(surfs)
                obj_values['positions'] = target_obj_values['positions']

            ##

            for obj_name, target_obj_timing in target_anim_timing.items():

                obj_timing = anim_timing[obj_name] = {}

                for key in ('surface_indices', 'position_indices'):
                    obj_timing[key] = WalkingDeque(target_obj_timing[key])

        elif operation_name == 'backwards':

            for obj_name, target_obj_values in target_anim_values.items():

                obj_values = anim_values[obj_name] = {}

                obj_values['surfaces'] = target_obj_values['surfaces']
                obj_values['positions'] = target_obj_values['positions']


            for obj_name, target_obj_timing in target_anim_timing.items():

                obj_timing = anim_timing[obj_name] = {}

                for key in ('surface_indices', 'position_indices'):
                    obj_timing[key] = WalkingDeque(reversed(target_obj_timing[key]))
