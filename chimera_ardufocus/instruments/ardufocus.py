from chimera.core.lock import lock

from chimera.interfaces.focuser import (
    FocuserFeature,
    InvalidFocusPositionException,
    FocuserAxis,
)

from chimera.instruments.focuser import FocuserBase


class ArduFocus(FocuserBase):

    def __init__(self):
        FocuserBase.__init__(self)

        self._position = 0

        self._supports = {
            FocuserFeature.TEMPERATURE_COMPENSATION: False,
            FocuserFeature.POSITION_FEEDBACK: True,
            FocuserFeature.ENCODER: True,
            FocuserFeature.CONTROLLABLE_X: False,
            FocuserFeature.CONTROLLABLE_Y: False,
            FocuserFeature.CONTROLLABLE_Z: True,
            FocuserFeature.CONTROLLABLE_U: False,
            FocuserFeature.CONTROLLABLE_V: False,
            FocuserFeature.CONTROLLABLE_W: False,
        }

    @lock
    def move_in(self, n, axis=FocuserAxis.Z):
        self._check_axis(axis)
        target = self.get_position() - n

        if self._in_range(target):
            self._set_position(target)
        else:
            raise InvalidFocusPositionException(
                f"{target} is outside focuser boundaries."
            )

    @lock
    def move_out(self, n, axis=FocuserAxis.Z):
        self._check_axis(axis)
        target = self.get_position() + n

        if self._in_range(target):
            self._set_position(target)
        else:
            raise InvalidFocusPositionException(
                f"{target} is outside focuser boundaries."
            )

    @lock
    def move_to(self, position, axis=FocuserAxis.Z):
        self._check_axis(axis)
        if self._in_range(position):
            self._set_position(position)
        else:
            raise InvalidFocusPositionException(
                f"{int(position)} is outside focuser boundaries."
            )

    @lock
    def get_position(self, axis=FocuserAxis.Z):
        self._check_axis(axis)
        return self._position

    def get_range(self, axis=FocuserAxis.Z):
        self._check_axis(axis)
        return (0, 7000)

    def _set_position(self, n):
        self.log.info(f"Changing focuser to {n}")
        self._position = n

    def _in_range(self, n):
        min_pos, max_pos = self.get_range()
        return min_pos <= n <= max_pos
