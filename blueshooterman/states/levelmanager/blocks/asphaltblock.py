
### third-party import
from pygame import Surface


### local import
from ....pygameconstants import blit_on_screen


class AsphaltBlock:

    surf_map = {}

    def __init__(self, name, size, pos_name, pos_value):

        self.name = name

        surf_map = self.surf_map

        if size in surf_map:
            self.image = surf_map[size]

        else:
            self.image = surf_map[size] = Surface(size).convert()
            self.image.fill('gray')

        self.rect = self.image.get_rect()
        setattr(self.rect, pos_name, pos_value)
        self.colliderect = self.rect.colliderect

    def update(self): pass

    def draw(self):
        blit_on_screen(self.image, self.rect)
