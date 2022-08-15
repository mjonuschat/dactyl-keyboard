#!/usr/bin/env python3
from __future__ import annotations

import logging
import typing as t
from importlib.util import find_spec
from pathlib import Path

import pinject

from dactyl_manuform.builders.base import DactylManuformBuilder
from dactyl_manuform.components.properties import DactylManuformProperties
from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.decider import DactylManuformComponentDecider
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.types import RenderEngine

try:
    from dactyl_manuform.modellers.cadquery import CadQueryEngine
except ModuleNotFoundError:
    # TODO: Warning message
    pass

try:
    from dactyl_manuform.modellers.solid import SolidEngine
except ModuleNotFoundError:
    # TODO: Warning Message
    pass


ComponentList = t.Dict[
    str, t.Type[t.Union[AbstractComponentClass, DactylManuformBuilder]]
]


class DactylManuformBindingSpec(pinject.BindingSpec):
    __MODULES: ComponentList = {}

    def __init__(self, config: DactylManuformConfig):
        super().__init__()
        self.config = config
        self.decider = DactylManuformComponentDecider(config=self.config)

        self._import_components()

    def __import(self, directory: str) -> ComponentList:
        root = Path(__file__).parent
        models = {}
        for f in (root / directory).rglob("*.py"):
            py = ".".join([str(p) for p in f.with_suffix("").relative_to(root).parts])
            mod = __import__(".".join([__package__, py]), fromlist=[py])
            classes = [
                getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)
            ]
            for cls in classes:
                models[cls.__name__] = cls

        return models

    def _import_components(self) -> ComponentList:
        if not self.__MODULES:
            components = self.__import("components")
            builders = self.__import("builders")
            transformers = self.__import("transformers")
            modules = {**components, **builders, **transformers}
            self.__MODULES = modules
            return modules

        return self.__MODULES

    @property
    def model_builder(self) -> t.Type[DactylManuformBuilder]:
        klass_name = self.decider.model_builder
        klass = self.__MODULES[klass_name]

        return klass

    def build_component(
        self, name: str, *args, **kwargs
    ) -> t.Union[AbstractComponentClass, DactylManuformBuilder]:
        return self.__MODULES[name](*args, **kwargs)

    def configure(self, bind):
        bind("properties", to_class=DactylManuformProperties)

    def provide_config(self) -> DactylManuformConfig:
        return self.config.copy(deep=True)

    def provide_log(self) -> logging.Logger:
        return logging.getLogger()

    def provide_engine(self):
        engine = self.decider.engine
        if engine == RenderEngine.SOLID:
            return SolidEngine()

        if engine == RenderEngine.CADQUERY:
            return CadQueryEngine()

        return self.build_component(self.decider.engine)

    def provide_case_wall(
        self,
        config,
        engine,
        log,
        back_wall,
        front_wall,
        left_wall,
        right_wall,
    ):
        return self.build_component(
            self.decider.case_walls,
            config=config,
            engine=engine,
            log=log,
            back_wall=back_wall,
            front_wall=front_wall,
            left_wall=left_wall,
            right_wall=right_wall,
        )

    def provide_connectors(self, config, engine, log, properties, placement):
        return self.build_component(
            self.decider.connectors,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
        )

    def provide_screw_inserts(
        self, config, engine, log, properties, placement, connectors
    ):
        return self.build_component(
            self.decider.screw_inserts,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            connectors=connectors,
            placement=placement,
        )

    def provide_key_holes(
        self, config, engine, log, properties, single_plate, placement
    ):
        return self.build_component(
            self.decider.key_holes,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            single_plate=single_plate,
            placement=placement,
        )

    def provide_controller_mount(
        self, config, engine, log, properties, placement, connectors
    ):
        return self.build_component(
            self.decider.controller_mount,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            connectors=connectors,
            placement=placement,
        )

    def provide_oled_mount(self, config, engine, log, single_plate, placement):
        return self.build_component(
            self.decider.oled_mount,
            config=config,
            engine=engine,
            log=log,
            single_plate=single_plate,
            placement=placement,
        )

    def provide_plate_pcb_cutouts(self, config, engine, log, properties, placement):
        return self.build_component(
            self.decider.plate_pcb_cutouts,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
        )

    def provide_left_thumb_cluster(
        self,
        config,
        engine,
        log,
        properties,
        placement,
        thumb_properties,
        connectors,
        single_plate,
        key_caps,
        plate_pcb_cutouts,
        screw_inserts,
        trackball_components,
    ):
        return self.build_component(
            self.decider.left_thumb_cluster,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
            thumb_properties=thumb_properties,
            connectors=connectors,
            single_plate=single_plate,
            key_caps=key_caps,
            plate_pcb_cutouts=plate_pcb_cutouts,
            screw_inserts=screw_inserts,
            trackball_components=trackball_components,
        )

    def provide_right_thumb_cluster(
        self,
        config,
        engine,
        log,
        properties,
        placement,
        thumb_properties,
        connectors,
        single_plate,
        key_caps,
        plate_pcb_cutouts,
        screw_inserts,
        trackball_components,
    ):
        return self.build_component(
            self.decider.right_thumb_cluster,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
            thumb_properties=thumb_properties,
            connectors=connectors,
            single_plate=single_plate,
            key_caps=key_caps,
            plate_pcb_cutouts=plate_pcb_cutouts,
            screw_inserts=screw_inserts,
            trackball_components=trackball_components,
        )

    def provide_thumb_properties(
        self,
        config,
        engine,
        log,
        properties,
        placement,
    ):
        return self.build_component(
            self.decider.thumb_cluster_properties,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
        )

    def provide_key_caps(
        self,
        config,
        engine,
        log,
        properties,
        single_plate,
        placement,
        plate_pcb_cutouts,
    ):
        return self.build_component(
            self.decider.key_caps,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
            single_plate=single_plate,
            plate_pcb_cutouts=plate_pcb_cutouts,
        )

    def provide_base_plate(
        self,
        config,
        engine,
        log,
        properties,
        left_thumb_cluster,
        right_thumb_cluster,
        case_wall,
        screw_inserts,
    ):
        return self.build_component(
            self.decider.base_plate,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            left_thumb_cluster=left_thumb_cluster,
            right_thumb_cluster=right_thumb_cluster,
            case_wall=case_wall,
            screw_inserts=screw_inserts,
        )

    def provide_single_plate(self, config, engine, log, parts_path):
        return self.build_component(
            self.decider.single_plate,
            config=config,
            engine=engine,
            log=log,
            parts_path=parts_path,
        )

    def provide_back_wall(self, config, engine, log, properties, connectors, placement):
        return self.build_component(
            self.decider.back_wall,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            connectors=connectors,
            placement=placement,
        )

    def provide_front_wall(
        self, config, engine, log, properties, connectors, placement
    ):
        return self.build_component(
            self.decider.front_wall,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            connectors=connectors,
            placement=placement,
        )

    def provide_left_wall(self, config, engine, log, properties, connectors, placement):
        return self.build_component(
            self.decider.left_wall,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            connectors=connectors,
            placement=placement,
        )

    def provide_right_wall(
        self, config, engine, log, properties, connectors, placement
    ):
        return self.build_component(
            self.decider.right_wall,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            connectors=connectors,
            placement=placement,
        )

    def provide_placement(self, config, engine, log, properties):
        return self.build_component(
            self.decider.placement,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
        )

    def provide_trackball_components(
        self, config, engine, log, properties, placement, parts_path
    ):
        return self.build_component(
            self.decider.trackball_components,
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            placement=placement,
            parts_path=parts_path,
        )

    def provide_model_builder(self):
        return self.build_component(self.decider.model_builder)

    def provide_save_path(self, config: DactylManuformConfig) -> Path:
        path = Path(__file__).parent  # src dir
        path = path.parent  # project root

        path = path / "things"

        if config.save_dir:
            path = path / config.save_dir

        path.mkdir(mode=0o775, parents=True, exist_ok=True)

        return path

    # TODO: Relocate the parts directory
    def provide_parts_path(self) -> Path:
        spec = find_spec("src").submodule_search_locations or []
        if path := next(iter(spec), None):
            return Path(path) / "parts"

        # Best guess...
        return Path(__file__).parent.parent / "src" / "parts"
