### standard library import
from ast import literal_eval



KEY_ERROR_FORMATTER = ("{!r} key not present in user preferences").format

def validate_prefs_dict(prefs_dict):
    """Raise exception if dict doesn't validate."""

    ### key existence

    for key in (
        "FULLSCREEN",
        "MUSIC_VOLUME",
        "SFX_VOLUME",
        "LAST_USED_SAVE_SLOT",
    ):

        if key not in prefs_dict:
            raise KeyError(KEY_ERROR_FORMATTER(key))

    ### volumes values

    for key in ("MUSIC_VOLUME", "SFX_VOLUME"):

        vol = prefs_dict[key]

        if not isinstance(vol, float):
            raise TypeError(f"'{key}' option must be a float")

        if not (0. <= vol <= 1.):
            raise ValueError(f"'{key}' option's value must be from 0. to 1.")

    ### fullscreen values

    fullscreen_value = prefs_dict['FULLSCREEN']

    if not isinstance(fullscreen_value, bool):
        raise TypeError("FULLSCREEN option must be a boolean (False or True)")

    ### slot

    value = prefs_dict['LAST_USED_SAVE_SLOT']

    if value is None or isinstance(value, str):
        pass

    else:
        raise TypeError("LAST_USED_SLOT must be None or a string")
