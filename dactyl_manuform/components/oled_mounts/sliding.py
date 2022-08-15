#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.config import OledMountConfiguration
from dactyl_manuform.interfaces.oled_mount import OledMountComponent
from dactyl_manuform.types import Shape, Side

from pydantic import Field


class SlidingOledMountConfiguration(OledMountConfiguration):
    thickness: float = Field(alias="oled_thickness")
    edge_overlap_end: float = Field(alias="oled_edge_overlap_end")
    edge_overlap_connector: float = Field(alias="oled_edge_overlap_connector")
    edge_overlap_thickness: float = Field(alias="oled_edge_overlap_thickness")
    edge_overlap_clearance: float = Field(alias="oled_edge_overlap_clearance")
    edge_chamfer: float = Field(alias="oled_edge_chamfer")


class SlidingOledMountModel(OledMountComponent):
    @property
    def oled_config(self) -> SlidingOledMountConfiguration:
        return SlidingOledMountConfiguration.parse_obj(
            self.config.oled_configurations[self.config.oled_mount_type]
        )

    def render_frame(self, side: Side = Side.RIGHT) -> t.Tuple[Shape, Shape]:
        mount_ext_width = self.oled_config.width + 2 * self.oled_config.rim
        mount_ext_height = (
            self.oled_config.height
            + 2 * self.oled_config.edge_overlap_end
            + self.oled_config.edge_overlap_connector
            + self.oled_config.edge_overlap_clearance
            + 2 * self.oled_config.rim
        )
        mount_ext_up_height = self.oled_config.height + 2 * self.oled_config.rim
        top_hole_start = (
            -mount_ext_height / 2.0
            + self.oled_config.rim
            + self.oled_config.edge_overlap_end
            + self.oled_config.edge_overlap_connector
        )
        top_hole_length = self.oled_config.height

        hole = self.engine.box(
            mount_ext_width, mount_ext_up_height, self.oled_config.cut_depth + 0.01
        )
        hole = self.engine.translate(
            hole, (0.0, top_hole_start + top_hole_length / 2, 0.0)
        )

        hole_down = self.engine.box(
            mount_ext_width,
            mount_ext_height,
            self.oled_config.depth + self.oled_config.cut_depth / 2,
        )
        hole_down = self.engine.translate(
            hole_down, (0.0, 0.0, -self.oled_config.cut_depth / 4)
        )
        hole = self.engine.union([hole, hole_down])

        shape = self.engine.box(
            mount_ext_width, mount_ext_height, self.oled_config.depth
        )

        conn_hole_start = -mount_ext_height / 2.0 + self.oled_config.rim
        conn_hole_length = (
            self.oled_config.edge_overlap_end
            + self.oled_config.edge_overlap_connector
            + self.oled_config.edge_overlap_clearance
            + self.oled_config.thickness
        )
        conn_hole = self.engine.box(
            self.oled_config.width, conn_hole_length + 0.01, self.oled_config.depth
        )
        conn_hole = self.engine.translate(
            conn_hole,
            (
                0,
                conn_hole_start + conn_hole_length / 2,
                -self.oled_config.edge_overlap_thickness,
            ),
        )

        end_hole_length = (
            self.oled_config.edge_overlap_end + self.oled_config.edge_overlap_clearance
        )
        end_hole_start = mount_ext_height / 2.0 - self.oled_config.rim - end_hole_length
        end_hole = self.engine.box(
            self.oled_config.width, end_hole_length + 0.01, self.oled_config.depth
        )
        end_hole = self.engine.translate(
            end_hole,
            (
                0,
                end_hole_start + end_hole_length / 2,
                -self.oled_config.edge_overlap_thickness,
            ),
        )

        top_hole_start = (
            -mount_ext_height / 2.0
            + self.oled_config.rim
            + self.oled_config.edge_overlap_end
            + self.oled_config.edge_overlap_connector
        )
        top_hole_length = self.oled_config.height
        top_hole = self.engine.box(
            self.oled_config.width,
            top_hole_length,
            self.oled_config.edge_overlap_thickness
            + self.oled_config.thickness
            - self.oled_config.edge_chamfer,
        )
        top_hole = self.engine.translate(
            top_hole,
            (
                0,
                top_hole_start + top_hole_length / 2,
                (
                    self.oled_config.depth
                    - self.oled_config.edge_overlap_thickness
                    - self.oled_config.thickness
                    - self.oled_config.edge_chamfer
                )
                / 2.0,
            ),
        )

        top_chamfer_1 = self.engine.box(self.oled_config.width, top_hole_length, 0.01)
        top_chamfer_2 = self.engine.box(
            self.oled_config.width + 2 * self.oled_config.edge_chamfer,
            top_hole_length + 2 * self.oled_config.edge_chamfer,
            0.01,
        )
        top_chamfer_1 = self.engine.translate(
            top_chamfer_1, (0, 0, -self.oled_config.edge_chamfer - 0.05)
        )

        top_chamfer_1 = self.engine.hull_from_shapes([top_chamfer_1, top_chamfer_2])

        top_chamfer_1 = self.engine.translate(
            top_chamfer_1,
            (
                0,
                top_hole_start + top_hole_length / 2,
                self.oled_config.depth / 2.0 + 0.05,
            ),
        )

        top_hole = self.engine.union([top_hole, top_chamfer_1])

        shape = self.engine.difference(shape, [conn_hole, top_hole, end_hole])

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
        raise RuntimeError("SLIDING Oled Mount has no clip to render")
