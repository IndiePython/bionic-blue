
### third-party imports

from pygame import Surface

from pygame.font import Font


### local import
from .config import FONTS_DIR



REGULAR_FONT_PATH = FONTS_DIR / 'ark_pixel_12px_latin.ttf'

STYLE_TO_FONT = {
  'regular': REGULAR_FONT_PATH,
}

class FontMap(dict):

    def __missing__(self, key):

        if not isinstance(key, tuple):
            raise TypeError("'key' must be a tuple")

        elif not isinstance(key[0], str):
            raise TypeError("first item must be a str")

        elif not isinstance(key[1], int):
            raise TypeError("second item must be an int")

        elif key[0] not in STYLE_TO_FONT.keys():
            raise ValueError(
                "first item must one of the values inside the tuple:"
                f" {tuple(STYLE_TO_FONT.keys())}"
            )

        elif key[1] <= 0:
            raise ValueError("second item must be a positive integer")

        style, size = key

        return self.setdefault(key, Font(str(STYLE_TO_FONT[style]), size))

FONT_MAP = FontMap()

def render_text(
    text,
    style,
    size,
    padding = 0,
    foreground_color='white',
    background_color='black',
):

    surf = (

        FONT_MAP

        [(style, size)]

        .render(
            text,
            False,
            foreground_color,
            background_color,
        )

        .convert()

    )

    if padding > 0:

        double_padding = padding * 2

        padded_surf = (
            Surface(
                tuple(
                    dimension + double_padding
                    for dimension in surf.get_size()
                )
            ).convert()
        )

        padded_surf.fill(background_color)

        padded_surf.blit(surf, (padding, padding))

        return padded_surf

    else:
        return surf

