#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.single_plate import SinglePlateComponent

from dactyl_manuform.types import Shape, Side


class SquareCutoutSinglePlate(SinglePlateComponent):
    @property
    def keyswitch_width(self) -> float:
        return self.config.hole_keyswitch_width

    @property
    def keyswitch_height(self) -> float:
        return self.config.hole_keyswitch_height

    def render_base_plate(self, side: Side) -> Shape:
        tb_border = (self.mount_height - self.keyswitch_height) / 2
        top_wall = self.engine.box(self.mount_width, tb_border, self.plate_thickness)
        top_wall = self.engine.translate(
            top_wall,
            (
                0,
                (tb_border / 2) + (self.keyswitch_height / 2),
                self.plate_thickness / 2,
            ),
        )

        lr_border = (self.mount_width - self.keyswitch_width) / 2
        left_wall = self.engine.box(lr_border, self.mount_height, self.plate_thickness)
        left_wall = self.engine.translate(
            left_wall,
            ((lr_border / 2) + (self.keyswitch_width / 2), 0, self.plate_thickness / 2),
        )

        side_nub = self.engine.cylinder(radius=1, height=2.75)
        side_nub = self.engine.rotate(side_nub, (90, 0, 0))
        side_nub = self.engine.translate(side_nub, (self.keyswitch_width / 2, 0, 1))

        nub_cube = self.engine.box(1.5, 2.75, self.plate_thickness)
        nub_cube = self.engine.translate(
            nub_cube,
            ((1.5 / 2) + (self.keyswitch_width / 2), 0, self.plate_thickness / 2),
        )

        side_nub2 = self.engine.tess_hull(shapes=(side_nub, nub_cube))
        side_nub2 = self.engine.union([side_nub2, side_nub, nub_cube])

        plate_half1 = self.engine.union([top_wall, left_wall, side_nub2])
        plate_half2 = plate_half1
        plate_half2 = self.engine.mirror(plate_half2, "XZ")
        plate_half2 = self.engine.mirror(plate_half2, "YZ")

        return self.engine.union([plate_half1, plate_half2])
