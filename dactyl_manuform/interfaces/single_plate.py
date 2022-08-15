#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import BaseComponent
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.types import Shape, Side


class SinglePlateComponent(BaseComponent, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        parts_path: Path,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)
        self.parts_path = parts_path

    @property
    @abstractmethod
    def keyswitch_height(self) -> float:
        ...

    @property
    @abstractmethod
    def keyswitch_width(self) -> float:
        ...

    @property
    def hotswappable(self) -> bool:
        return self.config.plate_style.startswith("HS_")

    @property
    def plate_file(self) -> t.Optional[Path]:
        if self.hotswappable:
            return self.parts_path / "hot_swap_plate"

        # TODO: Handle this properly
        return None

    @property
    def mount_width(self) -> float:
        return self.keyswitch_width + 2 * self.config.plate_rim

    @property
    def mount_height(self) -> float:
        return self.keyswitch_height + 2 * self.config.plate_rim

    @property
    def mount_thickness(self) -> float:
        return self.plate_thickness

    @property
    def plate_thickness(self) -> float:
        return self.config.plate_thickness

    @property
    def plate_offset(self) -> float:
        return self.config.plate_offset

    @property
    def plate_holes(self) -> bool:
        return self.config.plate_holes

    @property
    def plate_hole_width(self) -> float:
        return self.config.plate_holes_width

    @property
    def plate_hole_height(self) -> float:
        return self.config.plate_holes_height

    @property
    def plate_hole_depth(self) -> float:
        return self.config.plate_holes_depth

    @property
    def plate_hole_diameter(self) -> float:
        return self.config.plate_holes_diameter

    @property
    def plate_hole_radius(self) -> float:
        return self.plate_hole_diameter / 2.0

    @property
    def plate_hole_x_offset(self) -> float:
        return self.config.plate_holes_xy_offset[0]

    @property
    def plate_hole_y_offset(self) -> float:
        return self.config.plate_holes_xy_offset[1]

    @property
    def clip_undercut(self) -> float:
        return self.config.clip_undercut

    @property
    def clip_thickness(self) -> float:
        return self.config.clip_thickness

    @property
    def undercut_transition(self) -> float:
        return self.config.undercut_transition

    def render_base_plate(self, side: Side) -> Shape:
        """
        Renders a square hole for non-nub designs.
        """
        plate = self.engine.box(
            self.mount_width, self.mount_height, self.mount_thickness
        )
        plate = self.engine.translate(plate, (0.0, 0.0, self.mount_thickness / 2.0))

        shape_cut = self.engine.box(
            self.keyswitch_width, self.keyswitch_height, self.mount_thickness * 2 + 0.02
        )
        shape_cut = self.engine.translate(
            shape_cut, (0.0, 0.0, self.mount_thickness - 0.01)
        )

        plate = self.engine.difference(plate, [shape_cut])

        return plate

    def render_undercut(self, plate: Shape, side: Side) -> Shape:
        return plate

    def render_plate_file(self, plate: Shape, side: Side) -> Shape:
        if plate_file := self.plate_file:
            socket = self.engine.import_file(plate_file)
            socket = self.engine.translate(
                socket, (0.0, 0.0, self.plate_thickness + self.plate_offset)
            )

            plate = self.engine.union([plate, socket])

        return plate

    def render_plate_holes(self, plate: Shape, side: Side) -> Shape:
        if self.plate_holes:
            half_width = self.plate_hole_width / 2.0
            half_height = self.plate_hole_height / 2.0

            # TODO: Extract into a property / extract correction factor
            half_depth = self.plate_hole_depth / 2 - 0.01
            height = self.plate_hole_depth + 0.01

            holes = [
                self.engine.translate(
                    self.engine.cylinder(
                        radius=self.plate_hole_radius,
                        height=height,
                    ),
                    (
                        self.plate_hole_x_offset + half_width,
                        self.plate_hole_y_offset + half_height,
                        half_depth,
                    ),
                ),
                self.engine.translate(
                    self.engine.cylinder(
                        radius=self.plate_hole_radius,
                        height=height,
                    ),
                    (
                        self.plate_hole_x_offset - half_width,
                        self.plate_hole_y_offset + half_height,
                        half_depth,
                    ),
                ),
                self.engine.translate(
                    self.engine.cylinder(
                        radius=self.plate_hole_radius,
                        height=height,
                    ),
                    (
                        self.plate_hole_x_offset - half_width,
                        self.plate_hole_y_offset - half_height,
                        half_depth,
                    ),
                ),
                self.engine.translate(
                    self.engine.cylinder(
                        radius=self.plate_hole_radius,
                        height=height,
                    ),
                    (
                        self.plate_hole_x_offset + half_width,
                        self.plate_hole_y_offset - half_height,
                        half_depth,
                    ),
                ),
            ]

            plate = self.engine.difference(plate, holes)

        return plate

    def mirror_plate(self, plate: Shape, side: Side):
        if side is Side.LEFT:
            plate = self.engine.mirror(plate, "YZ")

        return plate

    def render(self, side: Side = Side.RIGHT) -> Shape:
        plate = self.render_base_plate(side=side)
        plate = self.render_undercut(plate=plate, side=side)
        plate = self.render_plate_file(plate=plate, side=side)
        plate = self.render_plate_holes(plate=plate, side=side)
        plate = self.mirror_plate(plate=plate, side=side)

        return plate
