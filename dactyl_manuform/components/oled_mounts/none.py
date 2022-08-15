#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.config import OledMountConfiguration
from dactyl_manuform.interfaces.oled_mount import OledMountComponent
from dactyl_manuform.types import Shape, Side


class NoOledMountModel(OledMountComponent):
    @property
    def oled_config(self) -> OledMountConfiguration:
        raise RuntimeError("No oled mount configured")

    def render_frame(self, side: Side = Side.RIGHT) -> t.Tuple[Shape, Shape]:
        hole = self.engine.union([])
        shape = self.engine.union([])

        return hole, shape

    def render_clip(self, side: Side = Side.RIGHT) -> Shape:
        raise RuntimeError("No oled mount configured")
