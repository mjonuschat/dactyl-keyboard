#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC

from dactyl_manuform.interfaces.trackball_parts import TrackballPartsComponent

from dactyl_manuform.types import Shape, XYZ


class ModularTrackballPartsComponent(TrackballPartsComponent, ABC):
    @property
    def hole_diameter(self) -> float:
        return self.config.ball_diameter + 2 * (
            self.config.ball_gap
            + self.config.ball_wall_thickness
            + self.config.trackball_modular_clearance
        )

    @property
    def ring_diameter(self) -> float:
        return self.hole_diameter + 2 * self.config.trackball_modular_lip_width

    @property
    def ring_height(self) -> float:
        return self.config.trackball_modular_ring_height

    @property
    def ring_z_offset(self) -> float:
        return (
            self.properties.mount_thickness - self.config.trackball_modular_ball_height
        )

    def precut_shape(self) -> Shape:
        shape = self.engine.cylinder(
            self.trackball_hole_diameter / 2, self.trackball_hole_height
        )

        return shape

    def socket_shape(self) -> Shape:
        shape = self.engine.cylinder(self.ring_diameter / 2, self.ring_height)
        shape = self.engine.translate(
            shape, (0, 0, -self.ring_height / 2 + self.ring_z_offset)
        )

        return shape

    def cutout_shape(self) -> Shape:
        shape = self.engine.cylinder(self.hole_diameter / 2, self.ring_height + 0.2)
        shape = self.engine.translate(
            shape, (0, 0, -self.ring_height / 2 + self.ring_z_offset)
        )

        return shape

    def sensor_shape(self, position: XYZ, rotation: XYZ) -> Shape:
        return self.engine.union([])  # TODO: Was None
