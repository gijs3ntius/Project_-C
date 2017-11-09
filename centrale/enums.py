from enum import Enum

class Command(Enum):
    SET_ID = 0
    ROL_OUT = 1
    ROL_IN = 2
    MAX_ROL_OUT = 3
    MIN_ROL_OUT = 4
    TEMP_ROL_IN = 5
    TEMP_ROL_OUT = 6
    LIGHT_ROL_IN = 7
    LIGHT_ROL_OUT = 8


class SensorType(Enum):
    LIGHT = 1
    TEMP = 2
    DIST = 3
