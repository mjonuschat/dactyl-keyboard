#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.components.controller_mounts.mixins.usb_holder import (
    UsbHolderMixin,
)
from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape


class NoControllerMountModel(UsbHolderMixin, ControllerMountModel):
    def apply(self, shape: Shape) -> Shape:
        # Nothing to do, return unmodified shape
        return shape
