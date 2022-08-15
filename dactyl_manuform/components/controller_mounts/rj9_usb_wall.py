#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.components.controller_mounts.mixins.rj9_holder import (
    RJ9HolderMixin,
)
from dactyl_manuform.components.controller_mounts.usb_wall import (
    UsbWallControllerMountModel,
)

from dactyl_manuform.types import Shape


class RJ9UsbWallControllerMountModel(UsbWallControllerMountModel, RJ9HolderMixin):
    def apply(self, shape: Shape) -> Shape:
        shape2 = super().apply(shape=shape)
        shape2 = self.engine.difference(shape2, [self.rj9_space()])

        # TODO: Maybe this breaks things - screw inserts were added first in orig code
        shape2 = self.engine.union([shape2, self.rj9_holder()])

        return shape2
