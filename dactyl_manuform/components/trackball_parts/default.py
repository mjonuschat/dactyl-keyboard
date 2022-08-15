#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC

from dactyl_manuform.interfaces.trackball_parts import TrackballPartsComponent

from dactyl_manuform.types import Shape, XYZ


class DefaultTrackballPartsComponent(TrackballPartsComponent, ABC):
    def precut_shape(self) -> Shape:
        shape = self.engine.cylinder(
            self.trackball_hole_diameter / 2, self.trackball_hole_height
        )

        return shape

    def socket_shape(self) -> Shape:
        shape = self.engine.import_file(self.parts_path / "trackball_socket_body_34mm")

        return shape

    def cutout_shape(self) -> Shape:
        cutter = self.engine.import_file(
            self.parts_path / "trackball_socket_cutter_34mm"
        )
        sensor_cutter = self.engine.import_file(
            self.parts_path / "trackball_sensor_cutter"
        )
        shape = self.engine.union([cutter, sensor_cutter])

        return shape

    def sensor_shape(self, position: XYZ, rotation: XYZ) -> Shape:
        shape = self.engine.import_file(self.parts_path / "trackball_sensor_mount")

        return shape
