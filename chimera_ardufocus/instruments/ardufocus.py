import logging
import sys

from chimera.core.lock import lock
from chimera.interfaces.focuser import FocuserFeature, InvalidFocusPositionException, FocuserAxis
from chimera.instruments.focuser import FocuserBase
from chimera.core.chimeraobject import ChimeraObject

class ARDUFocus(FocuserBase):
    __config__ = {"param1": "a string parameter"}

    def __init__(self):
        ChimeraObject.__init__(self)

    def __start__(self):
        self.doSomething("test argument")

    def doSomething(self, arg):
        self.log.warning("Hello world")
        self.log.warning("My arg=%s" % arg)
        self.log.warning("My param1=%s" % self["param1"])
