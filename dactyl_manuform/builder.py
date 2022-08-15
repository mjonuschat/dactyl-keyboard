#!/usr/bin/env python3
from __future__ import annotations

import typing as t

import pinject

from dactyl_manuform.builders.base import DactylManuformBuilder
from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.di import DactylManuformBindingSpec


class DactylManuformBuilderFactory:
    def __init__(self, config: t.Dict[str, t.Any]) -> None:
        self.config = DactylManuformConfig.parse_obj(obj=config)

        spec = DactylManuformBindingSpec(config=self.config)
        self.__model_builder_cls = spec.model_builder

        self.container = pinject.new_object_graph(binding_specs=[spec])

    def __model_builder(self) -> DactylManuformBuilder:
        return self.container.provide(self.__model_builder_cls)

    def render(self) -> None:
        builder = self.__model_builder()
        builder.render()
