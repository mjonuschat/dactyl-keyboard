#!/usr/bin/env python3
from __future__ import annotations

from abc import ABC, abstractmethod
from functools import wraps
from logging import Logger
from pathlib import Path

from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.types import Shape


def debug_export(name: str):
    def export_decorator(fn):
        @wraps(fn)
        def export_wrapper(self, *args, **kwargs):
            shape = fn(self, *args, **kwargs)
            if self.debug_exports:
                debug_path = self.save_path / "debug"
                debug_path.mkdir(mode=0o775, parents=True, exist_ok=True)

                self.engine.export_file(shape=shape, fname=(debug_path / name))

            return shape

        return export_wrapper

    return export_decorator


class DactylManuformBuilder(ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        properties: DactylManuformProperties,
        engine: Engine,
        log: Logger,
        save_path: Path,
    ):
        self.log = log
        self.engine = engine
        self.properties = properties
        self.config = config
        self.save_path = save_path

    def export_file(self, shape: Shape, name: str) -> None:
        self.engine.export_file(
            shape=shape,
            fname=self.save_path / f"{self.config.config_name}_{name}",
        )

    def export_dxf(self, shape: Shape, name: str) -> None:
        self.engine.export_dxf(
            shape=shape,
            fname=self.save_path / f"{self.config.config_name}_{name}",
        )

    @abstractmethod
    def render(self) -> None:
        ...
