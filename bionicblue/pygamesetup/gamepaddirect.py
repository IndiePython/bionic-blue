"""Utility for gamepad directionals controls management.

Directional controls refer not only to the buttons on the
D-pad, but also the axes' controls, since they also convey
direction information.
"""

### standard library import
from functools import partial


### third-party imports

from pygame.joystick import get_count, Joystick

from pygame.event import post as post_event


### local imports

from .constants import (
    GAMEPADUPPRESSED,
    GAMEPADDOWNPRESSED,
    GAMEPADLEFTPRESSED,
    GAMEPADRIGHTPRESSED,
    GAMEPADUPRELEASED,
    GAMEPADDOWNRELEASED,
    GAMEPADLEFTRELEASED,
    GAMEPADRIGHTRELEASED,
)

from ..ourstdlibs.behaviour import do_nothing



### constants

## anonymous object to store gamepad state
GAMEPAD_NS = type('Object', (), {})()

## mock gamepad states

mock_gamepad_dict = {

    ## data

    '_last_x_hat': 0,
    '_last_y_hat': 0,
    '_last_x_axis': 0,
    '_last_y_axis': 0,
    'x_sum': 0,
    'y_sum': 0,

    ## behaviour
    'prepare_data_and_events': do_nothing,
}

### main function

def setup_gamepad_if_existent():

    if get_count():
        _prepare_existing_gamepad()

    else:
        GAMEPAD_NS.__dict__.update(mock_gamepad_dict)


### support functions/utilities

_get_0 = lambda: 0
_get_0_0 = lambda: (0, 0)

round_axis = lambda axis: 0 if abs(axis) < .2 else (1 if axis > 0 else -1)


def _prepare_existing_gamepad():

    ### instantiate gamepad
    gamepad = Joystick(0)


    ### store gamepad behaviour depending on existence of hats/axes

    ## hats

    if gamepad.get_numhats() >= 1:
        GAMEPAD_NS.get_hat_pos = partial(gamepad.get_hat, 0)

    else:
        GAMEPAD_NS.get_hat_pos = _get_0_0

    ## axes

    if gamepad.get_numaxes() >= 2:

        GAMEPAD_NS.get_x_axis = partial(gamepad.get_axis, 0)
        GAMEPAD_NS.get_y_axis = partial(gamepad.get_axis, 1)

    else:

        GAMEPAD_NS.get_x_axis = _get_0
        GAMEPAD_NS.get_y_axis = _get_0

    ### store gamepad states

    GAMEPAD_NS._last_x_hat, _last_y_hat = GAMEPAD_NS.get_hat_pos()

    # make so -1 means up and 1 means down for vertical orientation
    # of hat
    GAMEPAD_NS._last_y_hat = _last_y_hat * (-1 if _last_y_hat else 0)

    GAMEPAD_NS._last_x_axis = round_axis(GAMEPAD_NS.get_x_axis())
    GAMEPAD_NS._last_y_axis = round_axis(GAMEPAD_NS.get_y_axis())

    ### store directional states derived from the gamepad states

    GAMEPAD_NS.x_sum = GAMEPAD_NS._last_x_hat + GAMEPAD_NS._last_x_axis
    GAMEPAD_NS.y_sum = GAMEPAD_NS._last_y_hat + GAMEPAD_NS._last_y_axis

    ### store
    GAMEPAD_NS.prepare_data_and_events = _prepare_data_and_events


def _prepare_data_and_events():

    ### check hat

    _last_x_hat = GAMEPAD_NS._last_x_hat
    _last_y_hat = GAMEPAD_NS._last_y_hat

    x_hat, y_hat = GAMEPAD_NS.get_hat_pos()

    # make so -1 means up and 1 means down for vertical orientation
    # of hat
    y_hat *= -1 if y_hat else 0


    ## x hat

    if _last_x_hat != x_hat:

        if x_hat == 0:

            post_event(
                GAMEPADRIGHTRELEASED
                if _last_x_hat == 1
                else GAMEPADLEFTRELEASED
            )

        elif x_hat == 1:

            post_event(GAMEPADRIGHTPRESSED)

            if _last_x_hat == -1:
                post_event(GAMEPADLEFTRELEASED)

        else: # x_hat == -1

            post_event(GAMEPADLEFTPRESSED)

            if _last_x_hat == 1:
                post_event(GAMEPADRIGHTRELEASED)

    ## y hat

    if _last_y_hat != y_hat:

        if y_hat == 0:

            post_event(
                GAMEPADDOWNRELEASED
                if _last_y_hat == 1
                else GAMEPADUPRELEASED
            )

        elif y_hat == 1:

            post_event(GAMEPADDOWNPRESSED)

            if _last_y_hat == -1:
                post_event(GAMEPADUPRELEASED)

        else: # y_hat == -1

            post_event(GAMEPADUPPRESSED)

            if _last_y_hat == 1:
                post_event(GAMEPADDOWNRELEASED)


    ### store current hat

    GAMEPAD_NS._last_x_hat = x_hat
    GAMEPAD_NS._last_y_hat = y_hat

    ### check axes

    _last_x_axis = GAMEPAD_NS._last_x_axis
    _last_y_axis = GAMEPAD_NS._last_y_axis

    x_axis = round_axis(GAMEPAD_NS.get_x_axis())
    y_axis = round_axis(GAMEPAD_NS.get_y_axis())

    ## x axis

    if _last_x_axis != x_axis:

        if x_axis == 0:

            post_event(
                GAMEPADRIGHTRELEASED
                if _last_x_axis == 1
                else GAMEPADLEFTRELEASED
            )

        elif x_axis == 1:

            post_event(GAMEPADRIGHTPRESSED)

            if _last_x_axis == -1:
                post_event(GAMEPADLEFTRELEASED)

        else: # x_axis == -1

            post_event(GAMEPADLEFTPRESSED)

            if _last_x_axis == 1:
                post_event(GAMEPADRIGHTRELEASED)

    ## y axis

    if _last_y_axis != y_axis:

        if y_axis == 0:

            post_event(
                GAMEPADDOWNRELEASED
                if _last_y_axis == 1
                else GAMEPADUPRELEASED
            )

        elif y_axis == 1:

            post_event(GAMEPADDOWNPRESSED)

            if _last_y_axis == -1:
                post_event(GAMEPADUPRELEASED)

        else: # y_axis == -1

            post_event(GAMEPADUPPRESSED)

            if _last_y_axis == 1:
                post_event(GAMEPADDOWNRELEASED)


    ### store current axes

    GAMEPAD_NS._last_x_axis = x_axis
    GAMEPAD_NS._last_y_axis = y_axis


    ### store sum of directional states

    GAMEPAD_NS.x_sum = x_hat + x_axis
    GAMEPAD_NS.y_sum = y_hat + y_axis

