#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC

import numpy as np
from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape, XYZ


class UsbHolderMixin(ControllerMountModel, ABC):
    @property
    def usb_holder_position(self) -> Shape:
        return self.placement.key_position(
            list(
                np.array(self.wall_locate2(0, 1))
                + np.array([0, (self.properties.mount_height / 2), 0])
            ),
            1,
            0,
        )

    @property
    def usb_holder_size(self) -> XYZ:
        return 6.5, 10.0, 13.6

    @property
    def usb_holder_thickness(self) -> float:
        return 4.0

    def usb_holder(self) -> Shape:
        self.log.debug("usb_holder()")
        shape = self.engine.box(
            self.usb_holder_size[0] + self.usb_holder_thickness,
            self.usb_holder_size[1],
            self.usb_holder_size[2] + self.usb_holder_thickness,
        )

        shape = self.engine.translate(
            shape,
            (
                self.usb_holder_position[0],
                self.usb_holder_position[1],
                (self.usb_holder_size[2] + self.usb_holder_thickness) / 2,
            ),
        )
        return shape

    def usb_holder_hole(self) -> Shape:
        self.log.debug("usb_holder_hole()")
        shape = self.engine.box(*self.usb_holder_size)
        shape = self.engine.translate(
            shape,
            (
                self.usb_holder_position[0],
                self.usb_holder_position[1],
                (self.usb_holder_size[2] + self.usb_holder_thickness) / 2,
            ),
        )
        return shape
