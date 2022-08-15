#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.config import OledMountConfiguration
from dactyl_manuform.interfaces.oled_mount import OledMountComponent
from dactyl_manuform.types import Shape, Side

from pydantic import Field


class ClipOledMountConfiguration(OledMountConfiguration):
    thickness: float = Field(alias="oled_thickness")
    mount_bezel_thickness: float = Field(alias="oled_mount_bezel_thickness")
    mount_bezel_chamfer: float = Field(alias="oled_mount_bezel_chamfer")
    mount_connector_hole: float = Field(alias="oled_mount_connector_hole")
    screen_start_from_conn_end: float = Field(alias="oled_screen_start_from_conn_end")
    screen_length: float = Field(alias="oled_screen_length")
    screen_width: float = Field(alias="oled_screen_width")
    clip_thickness: float = Field(alias="oled_clip_thickness")
    clip_width: float = Field(alias="oled_clip_width")
    clip_overhang: float = Field(alias="oled_clip_overhang")
    clip_extension: float = Field(alias="oled_clip_extension")
    clip_width_clearance: float = Field(alias="oled_clip_width_clearance")
    clip_undercut: float = Field(alias="oled_clip_undercut")
    clip_undercut_thickness: float = Field(alias="oled_clip_undercut_thickness")
    clip_y_gap: float = Field(alias="oled_clip_y_gap")
    clip_z_gap: float = Field(alias="oled_clip_z_gap")


class ClipOledMountModel(OledMountComponent):
    @property
    def oled_config(self) -> ClipOledMountConfiguration:
        return ClipOledMountConfiguration.parse_obj(
            self.config.oled_configurations[self.config.oled_mount_type]
        )

    def render_frame(self, side: Side = Side.RIGHT) -> t.Tuple[Shape, Shape]:
        mount_ext_width = self.oled_config.width + 2 * self.oled_config.rim
        mount_ext_height = (
            self.oled_config.height
            + 2 * self.oled_config.clip_thickness
            + 2 * self.oled_config.clip_undercut
            + 2 * self.oled_config.clip_overhang
            + 2 * self.oled_config.rim
        )
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

        clip_slot = self.engine.box(
            self.oled_config.clip_width + 2 * self.oled_config.clip_width_clearance,
            self.oled_config.height
            + 2 * self.oled_config.clip_thickness
            + 2 * self.oled_config.clip_overhang,
            self.oled_config.depth + 0.1,
        )

        shape = self.engine.difference(shape, [clip_slot])

        clip_undercut = self.engine.box(
            self.oled_config.clip_width + 2 * self.oled_config.clip_width_clearance,
            self.oled_config.height
            + 2 * self.oled_config.clip_thickness
            + 2 * self.oled_config.clip_overhang
            + 2 * self.oled_config.clip_undercut,
            self.oled_config.depth + 0.1,
        )

        clip_undercut = self.engine.translate(
            clip_undercut, (0.0, 0.0, self.oled_config.clip_undercut_thickness)
        )
        shape = self.engine.difference(shape, [clip_undercut])

        plate = self.engine.box(
            self.oled_config.width + 0.1,
            self.oled_config.height - 2 * self.oled_config.mount_connector_hole,
            self.oled_config.depth - self.oled_config.thickness,
        )
        plate = self.engine.translate(
            plate, (0.0, 0.0, -self.oled_config.thickness / 2.0)
        )
        shape = self.engine.union([shape, plate])

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
        mount_ext_width = self.oled_config.width + 2 * self.oled_config.rim
        mount_ext_height = (
            self.oled_config.height
            + 2 * self.oled_config.clip_thickness
            + 2 * self.oled_config.clip_overhang
            + 2 * self.oled_config.clip_undercut
            + 2 * self.oled_config.rim
        )

        oled_leg_depth = self.oled_config.depth + self.oled_config.clip_z_gap

        shape = self.engine.box(
            mount_ext_width - 0.1,
            mount_ext_height - 0.1,
            self.oled_config.mount_bezel_thickness,
        )
        shape = self.engine.translate(
            shape, (0.0, 0.0, self.oled_config.mount_bezel_thickness / 2.0)
        )

        hole_1 = self.engine.box(
            self.oled_config.screen_width + 2 * self.oled_config.mount_bezel_chamfer,
            self.oled_config.screen_length + 2 * self.oled_config.mount_bezel_chamfer,
            0.01,
        )
        hole_2 = self.engine.box(
            self.oled_config.screen_width,
            self.oled_config.screen_length,
            2.05 * self.oled_config.mount_bezel_thickness,
        )
        hole = self.engine.hull_from_shapes([hole_1, hole_2])

        shape = self.engine.difference(
            shape,
            [
                self.engine.translate(
                    hole, (0.0, 0.0, self.oled_config.mount_bezel_thickness)
                )
            ],
        )

        clip_leg = self.engine.box(
            self.oled_config.clip_width, self.oled_config.clip_thickness, oled_leg_depth
        )
        clip_leg = self.engine.translate(clip_leg, (0.0, 0.0, -oled_leg_depth / 2.0))

        latch_1 = self.engine.box(
            self.oled_config.clip_width,
            self.oled_config.clip_overhang + self.oled_config.clip_thickness,
            0.01,
        )
        latch_2 = self.engine.box(
            self.oled_config.clip_width,
            self.oled_config.clip_thickness / 2,
            self.oled_config.clip_extension,
        )
        latch_2 = self.engine.translate(
            latch_2,
            (
                0.0,
                -(
                    -self.oled_config.clip_thickness / 2
                    + self.oled_config.clip_thickness
                    + self.oled_config.clip_overhang
                )
                / 2,
                -self.oled_config.clip_extension / 2,
            ),
        )
        latch = self.engine.hull_from_shapes([latch_1, latch_2])
        latch = self.engine.translate(
            latch, (0.0, self.oled_config.clip_overhang / 2, -oled_leg_depth)
        )

        clip_leg = self.engine.union([clip_leg, latch])

        clip_leg = self.engine.translate(
            clip_leg,
            (
                0.0,
                (
                    self.oled_config.height
                    + 2 * self.oled_config.clip_overhang
                    + self.oled_config.clip_thickness
                )
                / 2
                - self.oled_config.clip_y_gap,
                0.0,
            ),
        )

        shape = self.engine.union([shape, clip_leg, self.engine.mirror(clip_leg, "XZ")])

        return shape
