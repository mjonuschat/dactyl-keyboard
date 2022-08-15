#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.transformers.key_placement.default import (
    DefaultKeyPlacementTransformer,
)
from dactyl_manuform.types import Shape, XYZ


class FixedKeyPlacementTransformer(DefaultKeyPlacementTransformer):
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

        shape = rotate_y_fn(shape, self.fixed_angles(column))
        shape = translate_fn(shape, (self.fixed_x(column), 0, self.fixed_z(column)))
        shape = translate_fn(
            shape, (0, 0, -(self.properties.row_radius + self.fixed_z(column)))
        )
        shape = rotate_x_fn(
            shape, self.properties.column_curvature * (self.properties.centerrow - row)
        )
        shape = translate_fn(
            shape, (0, 0, self.properties.row_radius + self.fixed_z(column))
        )
        shape = rotate_y_fn(shape, self.config.fixed_tenting)
        shape = translate_fn(shape, (0, self.column_offset(column)[1], 0))

        return self.finalize_geometry(
            shape=shape, translate_fn=translate_fn, rotate_y_fn=rotate_y_fn
        )
