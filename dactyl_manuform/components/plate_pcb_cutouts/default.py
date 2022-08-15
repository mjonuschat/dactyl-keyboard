#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.interfaces.plate_pcb_cutout import PcbCutoutModel

from dactyl_manuform.types import Shape, Side, XYZ


class DefaultPlatePcbCutoutModel(PcbCutoutModel):
    @property
    def pcb_size(self) -> XYZ:
        return self.config.plate_pcb_size

    @property
    def pcb_offset(self) -> XYZ:
        return self.config.plate_pcb_offset

    def cutout(self, side: Side = Side.RIGHT) -> Shape:
        shape = self.engine.box(*self.pcb_size)
        shape = self.engine.translate(shape, (0, 0, -self.pcb_size[2] / 2))
        shape = self.engine.translate(shape, self.pcb_offset)

        if side is Side.LEFT:
            shape = self.engine.mirror(shape, "YZ")

        return shape

    def render(self, side: Side = Side.RIGHT) -> t.List[Shape]:
        self.log.debug("place_pcb_cutouts()")

        cutouts = []
        for column in range(self.properties.columns):
            for row in range(self.properties.rows):
                if (
                    self.properties.reduced_inner_columns
                    <= column
                    < (self.properties.columns - self.properties.reduced_outer_columns)
                ) or (not row == self.properties.lastrow):
                    cutouts.append(
                        self.placement.key_place(self.cutout(side=side), column, row)
                    )

        return cutouts
