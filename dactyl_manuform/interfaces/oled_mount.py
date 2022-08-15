#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from logging import Logger

import numpy as np

from dactyl_manuform.config import DactylManuformConfig, OledMountConfiguration
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.interfaces.single_plate import SinglePlateComponent
from dactyl_manuform.types import OledMount, Shape, Side, XYZ


class OledMountComponent(AbstractComponentClass, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        single_plate: SinglePlateComponent,
        placement: KeyPlacementTransformer,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.single_plate = single_plate
        self.placement = placement

    @property
    @abstractmethod
    def oled_config(self) -> OledMountConfiguration:
        ...

    @property
    def trackball_in_wall(self) -> bool:
        return self.config.trackball_in_wall

    @property
    def trackball_side(self) -> Side:
        return self.config.ball_side

    @property
    def left_wall_x_offset(self) -> float:
        offset = self.config.left_wall_x_offset
        if self.config.oled_mount_type is not OledMount.NONE:
            offset = self.oled_config.left_wall_x_offset_override

        return offset

    def oled_position_rotation(self, side: Side = Side.RIGHT) -> t.Tuple[XYZ, XYZ]:
        trackball_in_wall = self.trackball_in_wall and side in [
            self.trackball_side,
            Side.BOTH,
        ]

        if trackball_in_wall:
            _left_wall_x_offset = self.config.tbiw_left_wall_x_offset_override
            _oled_center_row = self.config.tbiw_oled_center_row
            _oled_translation_offset = self.config.tbiw_oled_translation_offset
            _oled_rotation_offset = self.config.tbiw_oled_rotation_offset
        elif self.config.oled_center_row is not None:
            _oled_center_row = self.config.oled_center_row
            _oled_translation_offset = self.config.oled_translation_offset
            _oled_rotation_offset = self.config.oled_rotation_offset
            _left_wall_x_offset = self.left_wall_x_offset
        else:
            raise ValueError("oled_center_row must be set")

        base_pt1 = self.placement.key_position(
            list(
                np.array([-self.single_plate.mount_width / 2, 0.0, 0.0])
                + np.array([0.0, (self.single_plate.mount_height / 2), 0.0])
            ),
            0,
            _oled_center_row - 1,
        )
        base_pt2 = self.placement.key_position(
            list(
                np.array([-self.single_plate.mount_width / 2, 0.0, 0.0])
                + np.array([0.0, (self.single_plate.mount_height / 2), 0.0])
            ),
            0,
            _oled_center_row + 1,
        )
        base_pt0 = self.placement.key_position(
            list(
                np.array([-self.single_plate.mount_width / 2, 0.0, 0.0])
                + np.array([0.0, (self.single_plate.mount_height / 2), 0.0])
            ),
            0,
            _oled_center_row,
        )

        oled_mount_location_xyz: XYZ = (
            (np.array(base_pt1) + np.array(base_pt2)) / 2.0
            + np.array(((-_left_wall_x_offset / 2), 0.0, 0.0))
            + np.array(_oled_translation_offset)
        )
        oled_mount_location_xyz[2] = (oled_mount_location_xyz[2] + base_pt0[2]) / 2

        angle_x = np.arctan2(base_pt1[2] - base_pt2[2], base_pt1[1] - base_pt2[1])
        angle_z = np.arctan2(base_pt1[0] - base_pt2[0], base_pt1[1] - base_pt2[1])
        if trackball_in_wall:
            oled_mount_rotation_xyz: XYZ = (0.0, self.rad2deg(angle_x), -90) + np.array(
                _oled_rotation_offset
            )
        else:
            oled_mount_rotation_xyz = (
                self.rad2deg(angle_x),
                0,
                -self.rad2deg(angle_z),
            ) + np.array(_oled_rotation_offset)

        return oled_mount_location_xyz, oled_mount_rotation_xyz

    @abstractmethod
    def render_clip(self, side: Side = Side.RIGHT) -> Shape:
        ...

    @abstractmethod
    def render_frame(self, side: Side = Side.RIGHT) -> t.Tuple[Shape, Shape]:
        ...
