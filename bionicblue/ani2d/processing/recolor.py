

### standard library import
from collections import defaultdict


### local imports

from ...ourstdlibs.color.constants import (
    HLS_NAMES,
    HLS_FACTORS,
    HUE_MID_POINTS_MAP,
)

from ...ourstdlibs.color.conversion import (
    full_rgb_to_hls,
    full_hls_to_rgb,
)



NEW_SPRITE_DATA = defaultdict(list)

def get_recolored_sprites_data(sprites_data, recolor_instructions):

    ### get existing colors

    existing_colors = {
        color
        for sprite_data in sprites_data
        for color in sprite_data
    }

    ### created a map containing their respective converted versions
    ### according to instructions

    recolor_map = {
        color: get_new_color(color, recolor_instructions)
        for color in existing_colors
    }

    ### populate a new list of sprites data with the points
    ### remapped to the new colors

    ## create list
    recolored_sprites_data = []

    ## iterate over current sprites data

    for sprite_data in sprites_data:

        ## for each existing color and associated points,
        ## extend a pre-existent or created-on-the-spot
        ## list of points for the respective new color
        ##
        ## we could just assign the points to the new color,
        ## but sometimes the new color may be the same for
        ## more than one color, which would cause previous
        ## points associated with the key to be lost as they
        ## are replaced completely, which is undesirable;
        ## this could happen, for instance, when turning
        ## the lightness to 100%, which would cause all
        ## colors to be converted to pure white;

        for color, points in sprite_data.items():

            new_color = recolor_map[color]
            NEW_SPRITE_DATA[new_color].extend(points)

        ## now, before appending the new sprite data,
        ## convert it into a regular dict and the list
        ## of points into a tuple of points

        recolored_sprites_data.append(

            {
                new_color: tuple(points)
                for new_color, points in NEW_SPRITE_DATA.items()
            }

        )

        ## clear the new sprite data
        NEW_SPRITE_DATA.clear()

    ### finally, return the list of recolored sprites data
    return recolored_sprites_data

def get_new_color(color, recolor_instructions):

    for name, *args in recolor_instructions:

        if name in HLS_NAMES:

            h, l, s = full_rgb_to_hls(color)

            if name == 'hue':

                operation, *remaining_args = args

                if operation == 'set':
                    new_h = remaining_args[0]

                elif operation == 'increment':
                    new_h = h + remaining_args[0]

                elif operation == 'set_from_basic':

                    basic_hue_name, increment = remaining_args

                    new_h = HUE_MID_POINTS_MAP[basic_hue_name]
                    new_h += increment

                new_h %= HLS_FACTORS[0]

                color = full_hls_to_rgb((new_h, l, s))

            elif name == 'lightness':

                operation, value = args

                if operation == 'increment':
                    new_l = l + value
                elif operation == 'set':
                    new_l = value

                if new_l not in range(0, HLS_FACTORS[1]+1):

                    new_l = min(

                        (
                            (boundary, abs(new_l - boundary))
                            for boundary in (0, HLS_FACTORS[1])
                        ),

                        key = lambda item: item[1],

                    )[0]

                color = full_hls_to_rgb((h, new_l, s))

            elif name == 'saturation':

                operation, value = args

                if operation == 'increment':
                    new_s = s + value
                elif operation == 'set':
                    new_s = value

                if new_s not in range(0, HLS_FACTORS[2]+1):

                    new_s = min(

                        (
                            (boundary, abs(new_s - boundary))
                            for boundary in (0, HLS_FACTORS[2])
                        ),

                        key = lambda item: item[1],

                    )[0]

                new_s %= HLS_FACTORS[2]

                color = full_hls_to_rgb((h, l, new_s))

    return color
