#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from logging import Logger

import numpy as np
from dactyl_manuform.components.properties import DactylManuformProperties
from dactyl_manuform.config import DactylManuformConfig, OledMountConfiguration
from dactyl_manuform.interfaces.base import BaseTransformer
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.types import ColumnStyle, OledMount, Shape, Side, XYZ


class KeyPlacementTransformer(BaseTransformer, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        properties: DactylManuformProperties,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.properties = properties

    @property
    def oled_config(self) -> t.Optional[OledMountConfiguration]:
        if self.config.oled_mount_type is OledMount.NONE:
            return

        return OledMountConfiguration.parse_obj(
            self.config.oled_configurations[self.config.oled_mount_type]
        )

    @property
    def left_wall_x_offset(self) -> float:
        if oled_config := self.oled_config:
            return oled_config.left_wall_x_offset_override

        return self.config.left_wall_x_offset

    @property
    def left_wall_z_offset(self) -> float:
        if oled_config := self.oled_config:
            return oled_config.left_wall_z_offset_override

        return self.config.left_wall_z_offset

    @property
    def left_wall_lower_y_offset(self) -> float:
        if oled_config := self.oled_config:
            return oled_config.left_wall_lower_y_offset

        return self.config.left_wall_lower_y_offset

    @property
    def left_wall_lower_z_offset(self) -> float:
        if oled_config := self.oled_config:
            return oled_config.left_wall_lower_z_offset

        return self.config.left_wall_lower_z_offset

    @property
    def column_style(self) -> ColumnStyle:
        return self.properties.column_style

    @property
    def tenting_angle(self) -> float:
        return self.config.tenting_angle

    def column_angle(self, column: int) -> float:
        return self.properties.row_curvature * (self.properties.centercol - column)

    def column_offset(self, column: int) -> XYZ:
        return self.config.column_offsets[column]

    def translate_place(self, shape: Shape, vector: XYZ) -> Shape:
        return self.engine.translate(shape, vector)

    def rotate_place_x(self, shape: Shape, angle: float) -> Shape:
        return self.engine.rotate(shape, (self.rad2deg(angle), 0.0, 0.0))

    def rotate_place_y(self, shape: Shape, angle: float) -> Shape:
        return self.engine.rotate(shape, (0.0, self.rad2deg(angle), 0.0))

    @property
    def left_wall_lower_x_offset(self) -> float:
        return self.config.left_wall_lower_x_offset

    def translate_position(self, shape: Shape, vector: XYZ) -> Shape:
        self.log.debug("translate_position()")
        vals = []
        for i in range(len(shape)):
            vals.append(shape[i] + vector[i])
        return vals

    def rotate_position_x(self, shape: Shape, angle: float) -> Shape:
        self.log.debug("rotate_position_x()")
        t_matrix = np.array(
            [
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)],
            ]
        )
        return np.matmul(t_matrix, shape)

    def rotate_position_y(self, shape: Shape, angle: float) -> Shape:
        self.log.debug("rotate_position_y()")
        t_matrix = np.array(
            [
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)],
            ]
        )
        return np.matmul(t_matrix, shape)

    def finalize_geometry(
        self,
        shape: Shape,
        translate_fn: t.Callable[[Shape, XYZ], Shape],
        rotate_y_fn: t.Callable[[Shape, float], Shape],
    ) -> Shape:

        shape = rotate_y_fn(shape, self.tenting_angle)
        shape = translate_fn(shape, (0.0, 0.0, self.properties.keyboard_z_offset))

        return shape

    def key_place(self, shape: Shape, column: int, row: int) -> Shape:
        self.log.debug("key_place()")
        return self.apply(
            shape=shape,
            column=column,
            row=row,
            translate_fn=self.translate_place,
            rotate_x_fn=self.rotate_place_x,
            rotate_y_fn=self.rotate_place_y,
        )

    def key_position(
        self,
        position: Shape,
        column: int,
        row: int,
    ) -> Shape:
        self.log.debug("key_position()")
        return self.apply(
            shape=position,
            column=column,
            row=row,
            translate_fn=self.translate_position,
            rotate_x_fn=self.rotate_position_x,
            rotate_y_fn=self.rotate_position_y,
        )

    def left_key_place(
        self,
        shape: Shape,
        row: int,
        direction: int,
        low_corner: bool = False,
        side: Side = Side.RIGHT,
    ) -> Shape:
        self.log.debug("left_key_place()")
        pos = self.left_key_position(
            row=row,
            direction=direction,
            low_corner=low_corner,
            side=side,
        )

        return self.engine.translate(shape, pos)

    @abstractmethod
    def left_key_position(
        self,
        row: int,
        direction: int,
        low_corner: bool = False,
        side: Side = Side.RIGHT,
    ) -> np.ndarray:
        ...

    @abstractmethod
    def apply(
        self,
        shape: Shape,
        column: int,
        row: int,
        translate_fn: t.Callable[[Shape, XYZ], Shape],
        rotate_x_fn: t.Callable[[Shape, float], Shape],
        rotate_y_fn: t.Callable[[Shape, float], Shape],
    ) -> Shape:
        pass
