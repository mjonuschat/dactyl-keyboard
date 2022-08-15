#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.single_plate import SinglePlateComponent


class SquareCutoutSinglePlate(SinglePlateComponent):
    @property
    def keyswitch_width(self) -> float:
        return self.config.hole_keyswitch_width

    @property
    def keyswitch_height(self) -> float:
        return self.config.hole_keyswitch_height
