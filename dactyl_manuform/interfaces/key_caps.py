#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger

from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import BaseComponent
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.interfaces.plate_pcb_cutout import PcbCutoutModel
from dactyl_manuform.interfaces.single_plate import SinglePlateComponent
from dactyl_manuform.types import Shape


class KeycapModel(BaseComponent, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        properties: DactylManuformProperties,
        single_plate: SinglePlateComponent,
        placement: KeyPlacementTransformer,
        plate_pcb_cutouts: PcbCutoutModel,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.properties = properties
        self.single_plate = single_plate
        self.placement = placement
        self.plate_cutout = plate_pcb_cutouts

    @property
    def pcb_width(self) -> float:
        return self.config.pcb_width

    @property
    def pcb_height(self) -> float:
        return self.config.pcb_height

    @property
    def pcb_thickness(self) -> float:
        return self.config.pcb_thickness

    @property
    def pcb_hole_diameter(self) -> float:
        return self.config.pcb_hole_diameter

    @property
    def pcb_hole_pattern_width(self) -> float:
        return self.config.pcb_hole_pattern_width

    @property
    def pcb_hole_pattern_height(self) -> float:
        return self.config.pcb_hole_pattern_height

    @property
    def pcb(self) -> Shape:
        shape = self.engine.box(self.pcb_width, self.pcb_height, self.pcb_thickness)
        shape = self.engine.translate(shape, (0, 0, -self.pcb_thickness / 2))
        hole = self.engine.cylinder(
            self.pcb_hole_diameter / 2, self.pcb_thickness + 0.2
        )
        hole = self.engine.translate(hole, (0, 0, -(self.pcb_thickness + 0.1) / 2))
        holes = [
            self.engine.translate(
                hole,
                (self.pcb_hole_pattern_width / 2, self.pcb_hole_pattern_height / 2, 0),
            ),
            self.engine.translate(
                hole,
                (-self.pcb_hole_pattern_width / 2, self.pcb_hole_pattern_height / 2, 0),
            ),
            self.engine.translate(
                hole,
                (
                    -self.pcb_hole_pattern_width / 2,
                    -self.pcb_hole_pattern_height / 2,
                    0,
                ),
            ),
            self.engine.translate(
                hole,
                (self.pcb_hole_pattern_width / 2, -self.pcb_hole_pattern_height / 2, 0),
            ),
        ]
        shape = self.engine.difference(shape, holes)

        return shape

    @abstractmethod
    def keycap(self, key_size: float = 1) -> Shape:
        ...

    def render(self, key_size: float = 1) -> Shape:
        caps = None
        for column in range(self.properties.columns):
            for row in range(self.properties.rows):
                if (
                    self.properties.reduced_inner_columns
                    <= column
                    < (self.properties.columns - self.properties.reduced_outer_columns)
                ) or (not row == self.properties.lastrow):
                    if caps is None:
                        caps = self.placement.key_place(
                            self.keycap(key_size=key_size), column, row
                        )
                    else:
                        caps = self.engine.add(
                            [
                                caps,
                                self.placement.key_place(
                                    self.keycap(key_size=key_size), column, row
                                ),
                            ]
                        )

        return caps
