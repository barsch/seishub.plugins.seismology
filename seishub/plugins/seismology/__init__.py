# -*- coding: utf-8 -*-

from package import *
from station import *
from event import *
from waveform import *


path = os.path.dirname(__file__)
__version__ = open(os.path.join(path, "VERSION.txt")).read().strip()