#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from logging import Logger

from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import BaseComponent
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.types import Shape, Side


class PcbCutoutModel(BaseComponent, ABC):
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

    @abstractmethod
    def cutout(self, side: Side = Side.RIGHT) -> Shape:
        ...

    @abstractmethod
    def render(self, side: Side = Side.RIGHT) -> t.List[Shape]:
        ...
