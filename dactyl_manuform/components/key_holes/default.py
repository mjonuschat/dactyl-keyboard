#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.key_holes import KeyHolesModel

from dactyl_manuform.types import Shape, Side


class DefaultKeyHolesModel(KeyHolesModel):
    def render(self, side: Side = Side.RIGHT) -> Shape:
        self.log.debug("Rendering key holes")
        holes = []
        for column in range(self.properties.columns):
            for row in range(self.properties.rows):
                if (
                    self.properties.reduced_inner_columns
                    <= column
                    < (self.properties.columns - self.properties.reduced_outer_columns)
                ) or (not row == self.properties.lastrow):
                    holes.append(
                        self.placement.key_place(
                            self.single_plate.render(side=side), column, row
                        )
                    )

        shape = self.engine.union(holes)

        return shape
