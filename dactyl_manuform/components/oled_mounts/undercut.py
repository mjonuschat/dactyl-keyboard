#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.config import OledMountConfiguration
from dactyl_manuform.interfaces.oled_mount import OledMountComponent
from dactyl_manuform.types import Shape, Side

from pydantic import Field


class UndercutOledMountConfiguration(OledMountConfiguration):
    undercut: float = Field(alias="oled_mount_undercut")
    undercut_thickness: float = Field(alias="oled_mount_undercut_thickness")


class UndercutOledMountModel(OledMountComponent):
    @property
    def oled_config(self) -> UndercutOledMountConfiguration:
        return UndercutOledMountConfiguration.parse_obj(
            self.config.oled_configurations[self.config.oled_mount_type]
        )

    def render_frame(self, side: Side = Side.RIGHT) -> t.Tuple[Shape, Shape]:
        mount_ext_width = self.oled_config.width + 2 * self.oled_config.rim
        mount_ext_height = self.oled_config.height + 2 * self.oled_config.rim
        hole = self.engine.box(
            mount_ext_width, mount_ext_height, self.oled_config.cut_depth + 0.01
        )

        shape = self.engine.box(
            mount_ext_width, mount_ext_height, self.oled_config.depth
        )
        shape = self.engine.difference(
            shape,
            [
                self.engine.box(
                    self.oled_config.width,
                    self.oled_config.height,
                    self.oled_config.depth + 0.1,
                )
            ],
        )
        undercut = self.engine.box(
            self.oled_config.width + 2 * self.oled_config.undercut,
            self.oled_config.height + 2 * self.oled_config.undercut,
            self.oled_config.depth,
        )
        undercut = self.engine.translate(
            undercut, (0.0, 0.0, -self.oled_config.undercut_thickness)
        )
        shape = self.engine.difference(shape, [undercut])

        oled_mount_location_xyz, oled_mount_rotation_xyz = self.oled_position_rotation(
            side=side
        )

        shape = self.engine.rotate(shape, oled_mount_rotation_xyz)
        shape = self.engine.translate(
            shape,
            (
                oled_mount_location_xyz[0],
                oled_mount_location_xyz[1],
                oled_mount_location_xyz[2],
            ),
        )

        hole = self.engine.rotate(hole, oled_mount_rotation_xyz)
        hole = self.engine.translate(
            hole,
            (
                oled_mount_location_xyz[0],
                oled_mount_location_xyz[1],
                oled_mount_location_xyz[2],
            ),
        )

        return hole, shape

    def render_clip(self, side: Side = Side.RIGHT) -> Shape:
        raise RuntimeError("UNDERCUT Oled Mount has no clip to render")
