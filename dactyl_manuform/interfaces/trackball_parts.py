#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger
from pathlib import Path

from dactyl_manuform.components.properties import DactylManuformProperties
from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.types import Shape, TrackballComponents, XYZ


class TrackballPartsComponent(AbstractComponentClass, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        properties: DactylManuformProperties,
        placement: KeyPlacementTransformer,
        parts_path: Path,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.properties = properties
        self.placement = placement
        self.parts_path = parts_path

    @property
    def socket_rotation_offset(self) -> XYZ:
        return self.config.tb_socket_rotation_offset

    @property
    def socket_translation_offset(self) -> XYZ:
        return self.config.tb_socket_translation_offset

    @property
    def trackball_hole_diameter(self) -> float:
        return self.config.trackball_hole_diameter

    @property
    def trackball_hole_height(self) -> float:
        return self.config.trackball_hole_height

    @property
    def trackball_ball_diameter(self) -> float:
        return self.config.ball_diameter

    @abstractmethod
    def precut_shape(self) -> Shape:
        ...

    def precut(self, rotation: XYZ, position: XYZ) -> Shape:
        precut = self.precut_shape()

        precut = self.engine.rotate(precut, self.socket_rotation_offset)
        precut = self.engine.translate(precut, self.socket_translation_offset)
        precut = self.engine.rotate(precut, rotation)
        precut = self.engine.translate(precut, position)

        return precut

    @abstractmethod
    def socket_shape(self) -> Shape:
        ...

    def socket(self, position: XYZ, rotation: XYZ) -> Shape:
        socket = self.socket_shape()

        socket = self.engine.rotate(socket, self.socket_rotation_offset)
        socket = self.engine.translate(socket, self.socket_translation_offset)
        socket = self.engine.rotate(socket, rotation)
        socket = self.engine.translate(socket, position)

        return socket

    @abstractmethod
    def cutout_shape(self) -> Shape:
        ...

    def cutout(self, position: XYZ, rotation: XYZ) -> Shape:
        cutout = self.cutout_shape()

        cutout = self.engine.rotate(cutout, self.socket_rotation_offset)
        cutout = self.engine.translate(cutout, self.socket_translation_offset)

        cutout = self.engine.rotate(cutout, rotation)
        cutout = self.engine.translate(cutout, position)

        return cutout

    @abstractmethod
    def sensor_shape(self, position: XYZ, rotation: XYZ) -> Shape:
        ...

    def sensor(self, position: XYZ, rotation: XYZ) -> Shape:
        sensor = self.sensor_shape(position=position, rotation=rotation)

        # Small adjustment due to line to line surface / minute numerical error issues
        # Creates small overlap to assist engines in union function later
        sensor = self.engine.rotate(sensor, self.socket_rotation_offset)
        sensor = self.engine.translate(sensor, self.socket_translation_offset)

        sensor = self.engine.translate(sensor, (0, 0, 0.001))
        sensor = self.engine.rotate(sensor, rotation)
        sensor = self.engine.translate(sensor, position)

        return sensor

    def ball_shape(self) -> Shape:
        shape = self.engine.sphere(self.trackball_ball_diameter / 2)

        return shape

    def ball(self, position: XYZ, rotation: XYZ) -> Shape:
        ball = self.ball_shape()

        ball = self.engine.rotate(ball, self.socket_rotation_offset)
        ball = self.engine.translate(ball, self.socket_translation_offset)
        ball = self.engine.rotate(ball, rotation)
        ball = self.engine.translate(ball, position)

        return ball

    def generate(self, position: XYZ, rotation: XYZ) -> TrackballComponents:
        return TrackballComponents(
            precut=self.precut(position=position, rotation=rotation),
            shape=self.socket(position=position, rotation=rotation),
            cutout=self.cutout(position=position, rotation=rotation),
            sensor=self.sensor(position=position, rotation=rotation),
            ball=self.ball(position=position, rotation=rotation),
        )
