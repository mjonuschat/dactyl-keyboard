#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC

import numpy as np
from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape, XYZ


class RJ9HolderMixin(ControllerMountModel, ABC):
    @property
    def rj9_start(self) -> Shape:
        return list(
            np.array([0, -3, 0])
            + np.array(
                self.placement.key_position(
                    list(
                        np.array(self.wall_locate3(0, 1))
                        + np.array([0, (self.properties.mount_height / 2), 0])
                    ),
                    0,
                    0,
                )
            )
        )

    @property
    def rj9_position(self) -> XYZ:
        return self.rj9_start[0], self.rj9_start[1], 11.0

    def rj9_cube(self) -> Shape:
        self.log.debug("rj9_cube()")
        shape = self.engine.box(14.78, 13, 22.38)

        return shape

    def rj9_space(self) -> Shape:
        self.log.debug("rj9_space()")
        return self.engine.translate(self.rj9_cube(), self.rj9_position)

    def rj9_holder(self) -> Shape:
        self.log.debug("rj9_holder()")
        shape = self.engine.union(
            [
                self.engine.translate(self.engine.box(10.78, 9, 18.38), (0, 2, 0)),
                self.engine.translate(self.engine.box(10.78, 13, 5), (0, 0, 5)),
            ]
        )
        shape = self.engine.difference(self.rj9_cube(), [shape])
        shape = self.engine.translate(shape, self.rj9_position)

        return shape
