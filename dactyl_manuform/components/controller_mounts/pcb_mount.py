#!/usr/bin/env python3
from __future__ import annotations

import numpy as np
from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape, XYZ


class PcbMountControllerMountModel(ControllerMountModel):
    @property
    def pcb_mount_ref_offset(self) -> XYZ:
        return self.config.pcb_mount_ref_offset

    @property
    def pcb_usb_hole_offset(self) -> XYZ:
        return self.config.pcb_usb_hole_offset

    @property
    def pcb_usb_hole_size(self) -> XYZ:
        return self.config.pcb_usb_hole_size

    @property
    def usb_holder_thickness(self) -> float:
        return 4.0

    @property
    def pcb_holder_position(self) -> XYZ:
        pcb_holder_position = self.pcb_mount_ref_position
        pcb_holder_position[0] = (
            pcb_holder_position[0] + self.config.pcb_holder_offset[0]
        )
        pcb_holder_position[1] = (
            pcb_holder_position[1] + self.config.pcb_holder_offset[1]
        )
        pcb_holder_position[2] = (
            pcb_holder_position[2] + self.config.pcb_holder_offset[2]
        )

        return pcb_holder_position

    @property
    def pcb_holder_thickness(self) -> float:
        return self.config.pcb_holder_size[2]

    @property
    def pcb_screw_position(self) -> XYZ:
        pcb_screw_position = self.pcb_mount_ref_position
        pcb_screw_position[1] = pcb_screw_position[1] + self.config.pcb_screw_y_offset

        return pcb_screw_position

    @property
    def pcb_mount_ref_position(self) -> Shape:
        pcb_mount_ref_position = self.placement.key_position(
            # TRRS POSITION IS REFERENCE BY CONVENIENCE
            list(
                np.array(self.wall_locate3(0, 1))
                + np.array([0, (self.properties.mount_height / 2), 0])
            ),
            0,
            0,
        )

        pcb_mount_ref_position[0] = (
            pcb_mount_ref_position[0] + self.pcb_mount_ref_offset[0]
        )
        pcb_mount_ref_position[1] = (
            pcb_mount_ref_position[1] + self.pcb_mount_ref_offset[1]
        )
        pcb_mount_ref_position[2] = 0.0 + self.pcb_mount_ref_offset[2]

        return pcb_mount_ref_position

    def pcb_usb_hole(self) -> Shape:
        self.log.debug("pcb_holder()")

        pcb_usb_position = self.pcb_mount_ref_position
        pcb_usb_position[0] = pcb_usb_position[0] + self.pcb_usb_hole_offset[0]
        pcb_usb_position[1] = pcb_usb_position[1] + self.pcb_usb_hole_offset[1]
        pcb_usb_position[2] = pcb_usb_position[2] + self.pcb_usb_hole_offset[2]

        shape = self.engine.box(*self.pcb_usb_hole_size)
        shape = self.engine.translate(
            shape,
            (
                pcb_usb_position[0],
                pcb_usb_position[1],
                self.pcb_usb_hole_size[2] / 2 + self.usb_holder_thickness,
            ),
        )
        return shape

    def trrs_hole(self) -> Shape:
        self.log.debug("trrs_hole()")
        trrs_position = self.pcb_mount_ref_position
        trrs_position[0] = trrs_position[0] + self.config.trrs_offset[0]
        trrs_position[1] = trrs_position[1] + self.config.trrs_offset[1]
        trrs_position[2] = trrs_position[2] + self.config.trrs_offset[2]

        # TODO: Backport fix
        trrs_hole_size = [3, 20]

        shape = self.engine.cylinder(*self.config.trrs_hole_size)
        shape = self.engine.rotate(shape, (0, 90, 90))
        shape = self.engine.translate(
            shape,
            (
                trrs_position[0],
                trrs_position[1],
                trrs_hole_size[0] + self.pcb_holder_thickness,
            ),
        )
        return shape

    def pcb_holder(self) -> Shape:
        self.log.debug("pcb_holder()")
        shape = self.engine.box(*self.config.pcb_holder_size)
        shape = self.engine.translate(
            shape,
            (
                self.pcb_holder_position[0],
                self.pcb_holder_position[1] - self.config.pcb_holder_size[1] / 2,
                self.pcb_holder_thickness / 2,
            ),
        )
        return shape

    def wall_thinner(self) -> Shape:
        self.log.debug("wall_thinner()")
        shape = self.engine.box(*self.config.wall_thinner_size)
        shape = self.engine.translate(
            shape,
            (
                self.pcb_holder_position[0],
                self.pcb_holder_position[1] - self.config.wall_thinner_size[1] / 2,
                self.config.wall_thinner_size[2] / 2 + self.pcb_holder_thickness,
            ),
        )
        return shape

    def pcb_screw_hole(self) -> Shape:
        self.log.debug("pcb_screw_hole()")
        holes = []
        hole = self.engine.cylinder(*self.config.pcb_screw_hole_size)
        hole = self.engine.translate(hole, self.pcb_screw_position)
        hole = self.engine.translate(
            hole, (0, 0, self.config.pcb_screw_hole_size[1] / 2 - 0.1)
        )
        for offset in self.config.pcb_screw_x_offsets:
            holes.append(self.engine.translate(hole, (offset, 0, 0)))

        return holes

    def apply(self, shape: Shape) -> Shape:
        shape2 = self.engine.difference(shape, [self.pcb_usb_hole()])
        shape2 = self.engine.difference(shape2, [self.trrs_hole()])
        shape2 = self.engine.union([shape2, self.pcb_holder()])
        shape2 = self.engine.difference(shape2, [self.wall_thinner()])
        shape2 = self.engine.difference(shape2, self.pcb_screw_hole())

        return shape2
