#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC

from dactyl_manuform.interfaces.walls import ControllerMountModel

from dactyl_manuform.types import Shape


class TeensyHolderMixin(ControllerMountModel, ABC):
    # TODO: Move these to the config?
    @property
    def teensy_width(self) -> float:
        return 20.0

    @property
    def teensy_height(self) -> float:
        return 12.0

    @property
    def teensy_length(self) -> float:
        return 33.0

    @property
    def teensy2_length(self) -> float:
        return 53.0

    @property
    def teensy_pcb_thickness(self) -> float:
        return 2.0

    @property
    def teensy_offset_height(self) -> float:
        return 5.0

    @property
    def teensy_holder_top_length(self) -> float:
        return 18.0

    @property
    def teensy_holder_width(self) -> float:
        return 7.0 + self.teensy_pcb_thickness

    @property
    def teensy_holder_height(self) -> float:
        return 6.0 + self.teensy_width

    def teensy_holder(self) -> Shape:
        self.log.debug("teensy_holder()")

        teensy_top_xy = self.placement.key_position(
            self.wall_locate3(-1, 0), 0, self.properties.centerrow - 1
        )
        teensy_bot_xy = self.placement.key_position(
            self.wall_locate3(-1, 0), 0, self.properties.centerrow + 1
        )

        teensy_holder_length = teensy_top_xy[1] - teensy_bot_xy[1]
        teensy_holder_offset = -teensy_holder_length / 2
        teensy_holder_top_offset = (
            self.teensy_holder_top_length / 2
        ) - teensy_holder_length

        s1 = self.engine.box(3, teensy_holder_length, 6 + self.teensy_width)
        s1 = self.engine.translate(s1, (1.5, teensy_holder_offset, 0))

        s2 = self.engine.box(self.teensy_pcb_thickness, teensy_holder_length, 3)
        s2 = self.engine.translate(
            s2,
            (
                (self.teensy_pcb_thickness / 2) + 3,
                teensy_holder_offset,
                -1.5 - (self.teensy_width / 2),
            ),
        )

        s3 = self.engine.box(
            self.teensy_pcb_thickness, self.teensy_holder_top_length, 3
        )
        s3 = self.engine.translate(
            s3,
            (
                (self.teensy_pcb_thickness / 2) + 3,
                teensy_holder_top_offset,
                1.5 + (self.teensy_width / 2),
            ),
        )

        s4 = self.engine.box(4, self.teensy_holder_top_length, 4)
        s4 = self.engine.translate(
            s4,
            (
                self.teensy_pcb_thickness + 5,
                teensy_holder_top_offset,
                1 + (self.teensy_width / 2),
            ),
        )

        shape = self.engine.union((s1, s2, s3, s4))

        shape = self.engine.translate(shape, (-self.teensy_holder_width, 0, 0))
        shape = self.engine.translate(shape, (-1.4, 0, 0))
        shape = self.engine.translate(
            shape, (teensy_top_xy[0], teensy_top_xy[1] - 1, (6 + self.teensy_width) / 2)
        )

        return shape
