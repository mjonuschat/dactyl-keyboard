#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from logging import Logger

from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import BaseComponent
from dactyl_manuform.interfaces.case import CaseModel
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.walls import ScrewInsertModel, ThumbClusterWallModel
from dactyl_manuform.types import RenderEngine, Shape, Side


class BasePlateModel(BaseComponent, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        properties: DactylManuformProperties,
        left_thumb_cluster: ThumbClusterWallModel,
        right_thumb_cluster: ThumbClusterWallModel,
        case_wall: CaseModel,
        screw_inserts: ScrewInsertModel,
    ):
        super().__init__(config=config, engine=engine, log=log)

        self.properties = properties
        self.left_thumb_cluster = left_thumb_cluster
        self.right_thumb_cluster = right_thumb_cluster
        self.case_wall = case_wall
        self.screw_inserts = screw_inserts

    def thumb_cluster(self, side: Side) -> ThumbClusterWallModel:
        if side is Side.RIGHT:
            return self.right_thumb_cluster
        return self.left_thumb_cluster

    @abstractmethod
    def render_cadquery(self, side: Side = Side.RIGHT) -> Shape:
        ...

    @abstractmethod
    def render_solid(self, side: Side = Side.RIGHT) -> Shape:
        ...

    def render(self, side: Side = Side.RIGHT) -> Shape:
        if self.engine.kind is RenderEngine.CADQUERY:
            return self.render_cadquery(side=side)

        return self.render_solid(side=side)
