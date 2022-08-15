#!/usr/bin/env python3
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from logging import Logger

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.types import Shape, Side


class AbstractComponentClass(ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
    ) -> None:
        self.config = config
        self.engine = engine
        self.log = log

    @staticmethod
    def deg2rad(degrees: float) -> float:
        return degrees * math.pi / 180

    @staticmethod
    def rad2deg(rad: float) -> float:
        return rad * 180 / math.pi


class BaseComponent(AbstractComponentClass, ABC):
    @abstractmethod
    def render(self, side: Side = Side.RIGHT) -> Shape:
        raise NotImplementedError
