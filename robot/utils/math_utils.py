# utils/math_utils.py
import math


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Clamp value between min_value and max_value.
    """
    return max(min_value, min(max_value, value))


def deg2rad(deg: float) -> float:
    """
    Degrees → radians.
    """
    return deg * math.pi / 180.0


def rad2deg(rad: float) -> float:
    """
    Radians → degrees.
    """
    return rad * 180.0 / math.pi


def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Euclidean distance in 2D.
    """
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
