#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger

from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.types import Shape


class ConnectorComponent(AbstractComponentClass, ABC):
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
    def post_size(self) -> float:
        return self.config.post_size

    @property
    def post_adj(self) -> float:
        return self.config.post_adj

    @property
    def thickness(self) -> float:
        return self.config.web_thickness

    @abstractmethod
    def post(self) -> Shape:
        ...

    @abstractmethod
    def post_tr(self) -> Shape:
        ...

    @abstractmethod
    def post_tl(self) -> Shape:
        ...

    @abstractmethod
    def post_br(self) -> Shape:
        ...

    @abstractmethod
    def post_bl(self) -> Shape:
        ...

    @abstractmethod
    def render(self) -> Shape:
        ...
