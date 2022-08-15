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
    # No openings in the back
    NONE = "NONE"
    # Standard internal plate with a square cutout for connection, no RJ9.
    USB_WALL = "USB_WALL"
    # Standard internal plate with RJ9 opening and square cutout for connection.
    RJ9_USB_WALL = "RJ9_USB_WALL"
    # Teensy holder, no RJ9
    USB_TEENSY = "USB_TEENSY"
    # Teensy holder
    RJ9_USB_TEENSY = "RJ9_USB_TEENSY"
    # square cutout for a holder such as the one from lolligagger
    EXTERNAL = "EXTERNAL"
    # PCB based controller mount
    PCB_MOUNT = "PCB_MOUNT"


class OledMount(str, Enum):
    # No OLED mount
    NONE = "NONE"
    # Features to set the OLED in a frame a snap a bezel down to hold it in place.
    CLIP = "CLIP"
    # Features to slide the OLED in place and use a pin or block to secure from underneath.
    SLIDING = "SLIDING"
    # Simple rectangle with undercut for clip in item
    UNDERCUT = "UNDERCUT"


class ScrewOffset(str, Enum):
    INSIDE = "INSIDE"
    OUTSIDE = "OUTSIDE"
    ORIGINAL = "ORIGINAL"


class RenderEngine(str, Enum):
    # SolidPython / OpenSCAD
    SOLID = "solid"
    # CadQuery / OpenCascade
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
    # original side nubs.
    NUB = "NUB"
    # hot swap underside with nubs.
    HS_NUB = "HS_NUB"
    # snap fit undercut only near switch clip.
    # May require CLIP_THICKNESS and possibly CLIP_UNDERCUT tweaking and/or filing to get proper snap.
    NOTCH = "NOTCH"
    # hot swap underside with notch.  Does not generate properly.  Hot swap step needs to be modified.
    HS_NOTCH = "HS_NOTCH"
    # snap fit undercut.
    # May require CLIP_THICKNESS and possibly CLIP_UNDERCUT tweaking and/or filing to get proper snap.
    UNDERCUT = "UNDERCUT"
    # hot swap underside with undercut. Does not generate properly. Hot swap step needs to be modified.
    HS_UNDERCUT = "HS_UNDERCUT"
    # a square hole.  Also useful for applying custom plate files.
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
