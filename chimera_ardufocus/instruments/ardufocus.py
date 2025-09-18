import logging
import sys

from chimera.core.lock import lock
from chimera.interfaces.focuser import FocuserFeature, InvalidFocusPositionException, FocuserAxis
from chimera.instruments.focuser import FocuserBase
from chimera.core.chimeraobject import ChimeraObject
from chimera.core.constants import SYSTEM_CONFIG_DIRECTORY

class ArduFocus(FocuserBase):
    def __init__(self):
        FocuserBase.__init__(self)
        self.tty = None
        self._supports = {FocuserFeature.TEMPERATURE_COMPENSATION: False,
                          FocuserFeature.POSITION_FEEDBACK: True,
                          FocuserFeature.ENCODER: True,
                          FocuserFeature.CONTROLLABLE_X: False,
                          FocuserFeature.CONTROLLABLE_Y: False,
                          FocuserFeature.CONTROLLABLE_Z: True,
                          FocuserFeature.CONTROLLABLE_U: False,
                          FocuserFeature.CONTROLLABLE_V: False,
                          FocuserFeature.CONTROLLABLE_W: False}
        self._position = 1

    def __start__(self):
        self["model"] = "Ardufocus 0.1"
        self.tty = self["device"]
        return True

    def savePostion(self, position):
        try:
            with open("~/.chimera/current_focus_position.txt", 'w') as f:
              f.write(str(position))
            print "Successfully saved position", position, "to", filename
        except IOError as e:
            print "Error: Could not save position to file:", e

    @lock
    def moveIn(self, n, axis=FocuserAxis.Z):
        self._checkAxis(axis)

        target = self.getPosition() - n

        if self._inRange(target):
            self._setPosition(target)
            self.savePostion(target)
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % target)

    @lock
    def moveOut(self, n, axis=FocuserAxis.Z):
        self._checkAxis(axis)

        target = self.getPosition() + n

        if self._inRange(target):
            self._setPosition(target)
            self.savePostion(target)
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % target)

    @lock
    def moveTo(self, position, axis=FocuserAxis.Z):
        # Check if axis is on the permitted axis list
        self._checkAxis(axis)

        if self._inRange(position):
            self._setPosition(position)
            self.savePostion(position)
        else:
            raise InvalidFocusPositionException("%d is outside focuser "
                                                "boundaries." % int(position))

    @lock
    def getPosition(self, axis=FocuserAxis.Z):
        self._checkAxis(axis)
        return self._position


    def getRange(self, axis=FocuserAxis.Z):
        self._checkAxis(axis)

        return 0, 6600

    def _setPosition(self, n):
        self.log.info("Changing focuser to %s" % n)
        self._position = n


    def _inRange(self, n):
        min_pos, max_pos = self.getRange()
        return (min_pos <= n <= max_pos)
