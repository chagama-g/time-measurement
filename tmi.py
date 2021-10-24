import time
from enum import Enum, auto
from typing import List


class TimeUnit(Enum):
    # second
    s = 1
    # millisecond
    ms = 1000


class SpecialPoint(Enum):
    START = auto()
    END = auto()


class Point:
    def __init__(self, _label, _unique=None):
        self.label = _label
        self.time = time.time()
        self.unique = _unique


def convert_time(time_s: float, digits: int = 2, unit: TimeUnit = TimeUnit.s) -> str:
    time_conv = time_s * unit.value
    time_str = f"{time_conv:.{digits}f} [{unit.name}]"

    return time_str


class FPS:
    def __init__(self):
        self.frame: List[Point] = []
        pass

    def check_format(self):
        check = self.frame[0].unique is SpecialPoint.START and self.frame[-1].unique is SpecialPoint.END
        if not check:
            raise Exception("Need to record start and end")

    def add_midpoint(self, label: str):
        self.frame.append(Point(label))

    def start(self):
        self.frame = []
        self.frame.append(Point(SpecialPoint.START.name, _unique=SpecialPoint.START))

    def end(self):
        self.frame.append(Point(SpecialPoint.END.name, _unique=SpecialPoint.END))

    def print_statistics(self, digits=2, timeunit=TimeUnit.s):
        self.check_format()

        timeline = {}

        elapsed = self.frame[-1].time - self.frame[0].time
        print("elapsed time: {}".format(convert_time(elapsed, digits, timeunit)))

        for i in range(len(self.frame) - 2):
            timeline[self.frame[i + 1].label] = self.frame[i + 1].time - self.frame[i].time

            print(self.frame[i + 1].label + ":", convert_time(timeline[self.frame[i + 1].label], digits, timeunit))
