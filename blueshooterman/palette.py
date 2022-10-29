"""Facility for color definitions and related tools.

Variable names for colors either describe the color names
(for instance, BLACK, WHITE, etc.), approximate color names
(for instance, SHALIMAR, which doesn't describe the SHALIMAR
color, but it is very close and don't have a specific name, so
we use SHALIMAR instead) or their roles in the package
(for instance, PRIMARY_COLOR_MEDIUM).
"""


### Neutral colors
BLACK = (0, 0, 0)
WHITE = HIGHLIGHT = (255, 255, 255)
SHADOW = (102, 102, 102)

GRAY_LIGHTER = (212, 212, 212)
GRAY_LIGHT = (170, 170, 170)
GRAY_MEDIUM = (128, 128, 128)
GRAY_DARK = (84, 84, 84)
GRAY_DARKER = (42, 42, 42)

ARBITRARY_COLORKEY = (129, 129, 129)

### Game art pallete and aliases
# (aliases are color names for approximate colors)
PRIMARY_COLOR_LIGHTER = SHALIMAR = (255, 253, 195)
PRIMARY_COLOR_LIGHT = WITCH_HAZE = (255, 251, 155)
PRIMARY_COLOR_MEDIUM = CHENIM = (227, 222, 100)
PRIMARY_COLOR_DARK = EARLS_GREEN = (193, 188, 63)
PRIMARY_COLOR_DARKER = LEMON_GINGER = (159, 154, 31)

SECONDARY_COLOR01_LIGHTER = PASTEL_GREEN = (114, 222, 121)
SECONDARY_COLOR01_LIGHT = EMERALD = (72, 206, 81)
SECONDARY_COLOR01_MEDIUM = FOREST_GREEN = (36, 193, 47)
SECONDARY_COLOR01_DARK = SALEM = (10, 170, 20)
SECONDARY_COLOR01_DARKER = JAPANESE_LAUREL = (1, 133, 9)

SECONDARY_COLOR02_LIGHTER = DEEP_BLUSH = (218, 92, 161)
SECONDARY_COLOR02_LIGHT = MEDIUM_RED_VIOLET = (207, 54, 137)
SECONDARY_COLOR02_MEDIUM = LIPSTICK = (201, 6, 113)
SECONDARY_COLOR02_DARK = FRESH_EGGPLANT = (159, 1, 87)
SECONDARY_COLOR02_DARKER = SIREN = (125, 0, 68)

COMPLEMENT_COLOR_LIGHTER = PICTON_BLUE = (44, 184, 237)
COMPLEMENT_COLOR_LIGHT = CERULEAN = (7, 178, 244)
COMPLEMENT_COLOR_MEDIUM = CERULEAN_02 = (1, 153, 211)
COMPLEMENT_COLOR_DARK = ALLPORTS = (1, 111, 154)
COMPLEMENT_COLOR_DARKER = ORIENT = (1, 87, 119)

### Other colors for specific usage
SKY_COLOR = (108, 166, 205)
DIALOGUEBOX_BACKGROUND = (255, 246, 143)
PROMPT_BACKGROUND = (84, 255, 159)
SIGN_POLE_COLOR = (185, 185, 185)
ORANGE = (255, 128, 0)
RED = (255, 0, 0)


def has_same_rgb(color1, color2):
    """Return True if rgb values are the same.

    The advantage of this function is that it doesn't
    care if color are represented by lists or tuples,
    as long as their respective rgb values have the same
    index.

    Without this functions, using
    [x, y, z] == (x, y, z) would equal False, since
    though their values are the same, they have different
    types. This would be an undesired answer, since those
    values represent the same color and thus are equal.

    Also, this functions works with color objects from
    pygame.color.Color.

    >>> has_same_rgb([22, 33, 44], [22, 33, 44])
    True
    >>> has_same_rgb([22, 33, 44], [ 2, 33, 44])
    False
    >>> has_same_rgb([22, 33, 44], (22, 33, 44))
    True
    >>> has_same_rgb([22, 33, 44, 12], [22, 33, 44])
    True
    """
    return all(color1[i] == color2[i] for i in range(3))
