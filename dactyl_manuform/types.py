#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from enum import Enum

from pydantic import BaseModel as PydanticBaseModel

XY = t.Tuple[float, float]
XYZ = t.Tuple[float, float, float]
Shape = t.TypeVar("Shape")
Shapes = t.Sequence[Shape]


class ControllerMount(str, Enum):
    NONE = "NONE"
    USB_WALL = "USB_WALL"
    RJ9_USB_WALL = "RJ9_USB_WALL"
    USB_TEENSY = "USB_TEENSY"
    RJ9_USB_TEENSY = "RJ9_USB_TEENSY"
    EXTERNAL = "EXTERNAL"
    PCB_MOUNT = "PCB_MOUNT"


class OledMount(str, Enum):
    NONE = "NONE"
    CLIP = "CLIP"
    SLIDING = "SLIDING"
    UNDERCUT = "UNDERCUT"


class ScrewOffset(str, Enum):
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    ORIGINAL = "ORIGINAL"


class RenderEngine(str, Enum):
    SOLID = "solid"
    CADQUERY = "cadquery"


class Side(str, Enum):
    LEFT = "left"
    RIGHT = "right"
    BOTH = "both"


class ColumnStyle(str, Enum):
    DEFAULT = "standard"
    ORTHOGRAPHIC = "orthographic"
    FIXED = "fixed"


class PlateStyle(str, Enum):
    NUB = "NUB"
    HS_NUB = "HS_NUB"
    NOTCH = "NOTCH"
    HS_NOTCH = "HS_NOTCH"
    UNDERCUT = "UNDERCUT"
    HS_UNDERCUT = "HS_UNDERCUT"
    HOLE = "HOLE"


class Symmetry(str, Enum):
    SYMMETRIC = "symmetric"
    ASYMMETRIC = "asymmetric"


class ThumbStyle(str, Enum):
    # 6-key
    DEFAULT = "DEFAULT"
    # 5-key
    MINI = "MINI"
    # Carbonfet 6-key
    CARBONFET = "CARBONFET"
    # Minidox 3-key
    MINIDOX = "MINIDOX"
    # Trackball: Orbyl
    TRACKBALL_ORBYL = "TRACKBALL_ORBYL"
    # Trackball: CJ
    TRACKBALL_CJ = "TRACKBALL_CJ"


class KeyCapType(str, Enum):
    NONE = "NONE"
    MX = "MX"
    CHOC = "CHOC"


class TrackballComponents(PydanticBaseModel):
    precut: Shape
    shape: Shape
    cutout: Shape
    sensor: Shape
    ball: Shape


class ShiftValues(PydanticBaseModel):
    up: bool
    down: bool
    left: bool
    right: bool

    up_adjust: float
    down_adjust: float
    left_adjust: float
    right_adjust: float
