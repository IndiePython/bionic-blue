
### third-party import
from pygame import Surface


### local imports

from ....config import SURF_MAP

from ....pygameconstants import blit_on_screen

from ....surfsman import get_seamless_surf


class CityWall:

    surf_map = {}

    def __init__(self, name, size, pos):

        self.name = name

        surf_map = self.surf_map

        if size in surf_map:
            self.image = surf_map[size]

        else:
            self.image = surf_map[size] = (
                get_seamless_surf(SURF_MAP['city_wall.png'], size)
            )

        self.rect = self.image.get_rect()
        setattr(self.rect, 'bottomleft', pos)
        self.colliderect = self.rect.colliderect

    def update(self): pass

    def draw(self):
        blit_on_screen(self.image, self.rect)
