
### third-party imports
from pygame import Rect, Surface


### local import
from .config import COLORKEY



def get_seamless_surf(surf, size):

    rect = surf.get_rect()
    area = Rect(0, 0, *size)

    area_surf = Surface(size).convert()

    if surf.get_colorkey():

        area_surf.fill(COLORKEY)
        area_surf.set_colorkey(COLORKEY)

    blit_on_area = area_surf.blit

    while rect.top < area.bottom:

        blit_on_area(surf, rect)

        rect.left = rect.right

        if rect.left > area.right:

            rect.top = rect.bottom
            rect.left = 0

    return area_surf
