#!/usr/bin/env python3
from __future__ import annotations

import typing as t

import numpy as np

from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.types import Shape, Side, XYZ


class DefaultKeyPlacementTransformer(KeyPlacementTransformer):
    def left_key_base_position(self, row: int, direction: int) -> np.ndarray:
        return np.array(
            self.key_position(
                [
                    -self.properties.mount_width * 0.5,
                    direction * self.properties.mount_height * 0.5,
                    0,
                ],
                0,
                row,
            )
        )

    def left_key_position_tbiw(
        self,
        row: int,
        direction: int,
        low_corner: bool = False,
        side: Side = Side.RIGHT,
    ) -> t.Optional[np.ndarray]:
        self.log.debug("left_key_position_tbiw()")

        if not self.properties.trackball_in_wall:
            return

        if side not in [self.properties.trackball_side, Side.BOTH]:
            return

        pos = self.left_key_base_position(row=row, direction=direction)

        x_offset = 0.0
        y_offset = 0.0
        z_offset = 0.0

        if low_corner:
            x_offset = self.config.tbiw_left_wall_lower_x_offset
            y_offset = self.config.tbiw_left_wall_lower_y_offset
            z_offset = self.config.tbiw_left_wall_lower_z_offset

        return np.array(
            pos
            - np.array(
                [
                    self.config.tbiw_left_wall_x_offset_override - x_offset,
                    -y_offset,
                    self.config.tbiw_left_wall_z_offset_override + z_offset,
                ]
            )
        )

    def left_key_position(
        self,
        row: int,
        direction: int,
        low_corner: bool = False,
        side: Side = Side.RIGHT,
    ) -> np.ndarray:
        self.log.debug("left_key_position()")

        tbiw_position = self.left_key_position_tbiw(row, direction, low_corner, side)
        if tbiw_position is not None:
            return tbiw_position

        pos = np.array(
            self.key_position(
                [
                    -self.properties.mount_width * 0.5,
                    direction * self.properties.mount_height * 0.5,
                    0,
                ],
                0,
                row,
            )
        )

        x_offset = 0.0
        y_offset = 0.0
        z_offset = 0.0

        if low_corner:
            x_offset = self.left_wall_lower_x_offset
            y_offset = self.left_wall_lower_y_offset
            z_offset = self.left_wall_lower_z_offset

        return np.array(
            pos
            - np.array(
                [
                    self.left_wall_x_offset - x_offset,
                    -y_offset,
                    self.left_wall_z_offset + z_offset,
                ]
            )
        )

    def apply(
        self,
        shape: Shape,
        column: int,
        row: int,
        translate_fn: t.Callable[[Shape, XYZ], Shape],
        rotate_x_fn: t.Callable[[Shape, float], Shape],
        rotate_y_fn: t.Callable[[Shape, float], Shape],
    ) -> Shape:
        self.log.debug("apply_key_geometry()")
        shape = translate_fn(shape, (0, 0, -self.properties.row_radius))
        shape = rotate_x_fn(
            shape, self.properties.column_curvature * (self.properties.centerrow - row)
        )
        shape = translate_fn(shape, (0, 0, self.properties.row_radius))
        shape = translate_fn(shape, (0, 0, -self.properties.column_radius))
        shape = rotate_y_fn(shape, self.column_angle(column))
        shape = translate_fn(shape, (0, 0, self.properties.column_radius))
        shape = translate_fn(shape, self.column_offset(column))

        return self.finalize_geometry(
            shape=shape, translate_fn=translate_fn, rotate_y_fn=rotate_y_fn
        )
