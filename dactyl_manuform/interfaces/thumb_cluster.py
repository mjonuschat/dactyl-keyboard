#!/usr/bin/env python3
from __future__ import annotations

from logging import Logger

from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.types import ThumbStyle, XYZ


class ThumbClusterProperties(AbstractComponentClass):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        properties: DactylManuformProperties,
        placement: KeyPlacementTransformer,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.properties = properties
        self.placement = placement

    @property
    def offsets(self) -> XYZ:
        return self.config.thumb_offsets

    @property
    def origin(self) -> XYZ:
        corner = self.properties.lastrow
        if self.properties.reduced_inner_columns > 0:
            corner = self.properties.cornerrow

        origin = self.placement.key_position(
            [self.properties.mount_width / 2, -(self.properties.mount_height / 2), 0.0],
            1,
            corner,
        )

        for i in range(len(origin)):
            origin[i] = origin[i] + self.offsets[i]

        if self.properties.thumb_style is ThumbStyle.MINIDOX:
            origin[1] = (
                origin[1]
                - 0.4 * (self.properties.minidox_key_size - 1) * self.config.sa_length
            )

        return origin[0], origin[1], origin[2]
