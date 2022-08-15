#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.components.controller_mounts.mixins.teensy_holder import (
    TeensyHolderMixin,
)
from dactyl_manuform.components.controller_mounts.mixins.usb_holder import (
    UsbHolderMixin,
)
from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape


class TeensyControllerMountModel(
    TeensyHolderMixin, UsbHolderMixin, ControllerMountModel
):
    def apply(self, shape: Shape) -> Shape:
        shape2 = self.engine.union([shape, self.teensy_holder()])
        shape2 = self.engine.union([shape2, self.usb_holder()])
        shape2 = self.engine.difference(shape2, [self.usb_holder_hole()])

        return shape2
