#!/usr/bin/env python3
from __future__ import annotations

import numpy as np
from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape


class ExternalControllerMountModel(ControllerMountModel):
    @property
    def external_holder_width(self) -> float:
        return self.config.external_holder_width

    @property
    def external_holder_height(self) -> float:
        return self.config.external_holder_height

    @property
    def external_holder_x_offset(self) -> float:
        return self.config.external_holder_xoffset

    @property
    def external_holder_y_offset(self) -> float:
        return self.config.external_holder_yoffset

    @property
    def external_start(self) -> Shape:
        return list(
            np.array([self.external_holder_width / 2, 0, 0])
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

    def apply(self, shape: Shape) -> Shape:
        self.log.debug("external_mount_hole()")
        mount_shape = self.engine.box(
            self.external_holder_width, 20.0, self.external_holder_height + 0.1
        )
        undercut = self.engine.box(
            self.external_holder_width + 8, 10.0, self.external_holder_height + 8 + 0.1
        )
        mount_shape = self.engine.union(
            [mount_shape, self.engine.translate(undercut, (0, -5, 0))]
        )

        mount_shape = self.engine.translate(
            mount_shape,
            (
                self.external_start[0] + self.external_holder_x_offset,
                self.external_start[1] + self.external_holder_y_offset,
                self.external_holder_height / 2 - 0.05,
            ),
        )

        return self.engine.difference(shape, [mount_shape])
