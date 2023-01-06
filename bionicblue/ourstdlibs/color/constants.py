"""Common constants."""


### factors for converting from unit to full color values

RGBA_FACTOR = 255

HLS_FACTORS = HSV_FACTORS = 360, 100, 100

### names for color models

RGBA_NAMES = "red", "green", "blue", "alpha"
HLS_NAMES = "hue", "lightness", "saturation"


### map arbitrarily associating names of basic colors with
### more or less central hue values associated to them

HUE_MID_POINTS_MAP = {
  "red": 0,
  "orange": 30,
  "yellow": 60,
  "green": 120,
  "cyan": 180,
  "blue":240,
  "magenta": 300,
}
