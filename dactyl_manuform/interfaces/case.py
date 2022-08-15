#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC
from logging import Logger

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base import BaseComponent
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.walls import (
    BackWallModel,
    FrontWallModel,
    LeftWallModel,
    RightWallModel,
)


class CaseModel(BaseComponent, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        back_wall: BackWallModel,
        front_wall: FrontWallModel,
        left_wall: LeftWallModel,
        right_wall: RightWallModel,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.back_wall = back_wall
        self.front_wall = front_wall
        self.left_wall = left_wall
        self.right_wall = right_wall

    @property
    def skeleton(self) -> bool:
        return self.config.skeletal
