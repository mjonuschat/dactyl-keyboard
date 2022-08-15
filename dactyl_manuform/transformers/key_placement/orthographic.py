#!/usr/bin/env python3
from __future__ import annotations

import typing as t

import numpy as np
from dactyl_manuform.transformers.key_placement.default import (
    DefaultKeyPlacementTransformer,
)

from dactyl_manuform.types import Shape, XYZ


class OrthographicKeyPlacementTransformer(DefaultKeyPlacementTransformer):
    def fixed_angles(self, column: int) -> float:
        return self.config.fixed_angles[column]

    def fixed_x(self, column: int) -> float:
        return self.config.fixed_x[column]

    def fixed_z(self, column: int) -> float:
        return self.config.fixed_z[column]

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

        column_x_delta = -1 - self.properties.column_radius * np.sin(
            self.properties.row_curvature
        )
        column_z_delta = self.properties.column_radius * (
            1 - np.cos(self.column_angle(column))
        )

        shape = translate_fn(shape, (0, 0, -self.properties.row_radius))
        shape = rotate_x_fn(
            shape, self.properties.column_curvature * (self.properties.centerrow - row)
        )
        shape = translate_fn(shape, (0, 0, self.properties.row_radius))
        shape = rotate_y_fn(shape, self.column_angle(column))
        shape = translate_fn(
            shape,
            (-(column - self.properties.centercol) * column_x_delta, 0, column_z_delta),
        )
        shape = translate_fn(shape, self.column_offset(column))

        return self.finalize_geometry(
            shape=shape, translate_fn=translate_fn, rotate_y_fn=rotate_y_fn
        )
