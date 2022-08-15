#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from logging import Logger
from pathlib import Path

from dactyl_manuform.builders.base import DactylManuformBuilder, debug_export
from dactyl_manuform.components.properties import DactylManuformProperties
from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.base_plate import BasePlateModel
from dactyl_manuform.interfaces.case import CaseModel
from dactyl_manuform.interfaces.connector import ConnectorComponent
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_caps import KeycapModel
from dactyl_manuform.interfaces.key_holes import KeyHolesModel
from dactyl_manuform.interfaces.oled_mount import OledMountComponent
from dactyl_manuform.interfaces.plate_pcb_cutout import PcbCutoutModel
from dactyl_manuform.interfaces.walls import (
    ControllerMountModel,
    ScrewInsertModel,
    ThumbClusterWallModel,
)
from dactyl_manuform.types import OledMount, Shape, Side, Symmetry


class DefaultDactylManuformBuilder(DactylManuformBuilder):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        save_path: Path,
        properties: DactylManuformProperties,
        key_holes: KeyHolesModel,
        connectors: ConnectorComponent,
        case_wall: CaseModel,
        screw_inserts: ScrewInsertModel,
        controller_mount: ControllerMountModel,
        oled_mount: OledMountComponent,
        plate_pcb_cutouts: PcbCutoutModel,
        left_thumb_cluster: ThumbClusterWallModel,
        right_thumb_cluster: ThumbClusterWallModel,
        key_caps: KeycapModel,
        base_plate: BasePlateModel,
    ):
        super().__init__(
            config=config,
            engine=engine,
            log=log,
            properties=properties,
            save_path=save_path,
        )

        self.base_plate = base_plate
        self.caps = key_caps
        self.right_thumb_cluster = right_thumb_cluster
        self.left_thumb_cluster = left_thumb_cluster
        self.plate_pcb_cutouts = plate_pcb_cutouts
        self.oled_mount = oled_mount
        self.controller_mount = controller_mount
        self.screw_inserts = screw_inserts
        self.case_wall = case_wall
        self.connectors = connectors
        self.key_holes = key_holes

        # TODO: Make configurable
        self.debug_exports: bool = False
        self._current_side: Side = Side.RIGHT

    @property
    def side(self) -> Side:
        return self._current_side

    @side.setter
    def side(self, side: Side) -> None:
        self._current_side = side

    @property
    def thumb_cluster(self) -> ThumbClusterWallModel:
        if self.side is Side.RIGHT:
            return self.right_thumb_cluster
        return self.left_thumb_cluster

    @debug_export(name="debug_key_plates")
    def create_key_plates(self, side: Side = Side.RIGHT) -> Shape:
        return self.engine.union([self.key_holes.render(side=side)])

    @debug_export(name="debug_connector_shape")
    def add_connectors(self, shape: Shape, side: Side = Side.RIGHT) -> Shape:
        connector_shape = self.connectors.render()
        return self.engine.union([shape, connector_shape])

    @debug_export(name="debug_walls_shape")
    def add_walls(self, shape: Shape, side: Side = Side.RIGHT) -> Shape:
        s2 = self.engine.union([self.case_wall.render(side=side)])
        s2 = self.engine.union([s2, *self.screw_inserts.outers(side=side)])
        s2 = self.controller_mount.apply(shape=s2)
        s2 = self.engine.difference(
            s2,
            [self.engine.union(self.screw_inserts.holes(side=side))],
        )

        return self.engine.union([shape, s2])

    def add_oled_mount(self, shape: Shape, side: Side = Side.RIGHT) -> Shape:
        hole, frame = self.oled_mount.render_frame(side=side)
        shape = self.engine.difference(shape, [hole])
        return self.engine.union([shape, frame])

    def add_trackball(self, shape: Shape, side: Side = Side.RIGHT) -> Shape:
        if not self.thumb_cluster.has_trackball:
            return shape

        trackball_components = self.thumb_cluster.trackball_components()
        shape = self.engine.difference(shape, [trackball_components.precut])
        shape = self.engine.union([shape, trackball_components.shape])
        shape = self.engine.difference(shape, [trackball_components.cutout])
        shape = self.engine.union([shape, trackball_components.sensor])

        if self.config.show_caps:
            shape = self.engine.add([shape, trackball_components.ball])

        return shape

    def add_trackball_in_wall_step1(
        self, shape: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        if not self.properties.trackball_in_wall:
            return shape

        if side in [Side.BOTH, self.properties.trackball_side]:
            self.add_trackball(shape=shape, side=side)

        return shape

    def add_pcb_plate_cutouts(self, shape: Shape, side: Side = Side.RIGHT) -> Shape:
        if self.config.plate_pcb_clear:
            shape = self.engine.difference(
                shape, [self.plate_pcb_cutouts.render(side=side)]
            )

        return shape

    @debug_export("debug_thumb_shape")
    def create_thumb_cluster(self, side: Side = Side.RIGHT) -> Shape:
        return self.thumb_cluster.render(side=side)

    @debug_export("debug_thumb_connector_shape")
    def create_thumb_connectors(self, side: Side = Side.RIGHT) -> Shape:
        return self.thumb_cluster.thumb_connectors()

    def create_thumb_walls(self, side: Side = Side.RIGHT) -> Shape:
        # TODO: Remove skeletal param
        shape = self.thumb_cluster.walls(side=side, skeleton=self.config.skeletal)
        shape = self.engine.union([shape, *self.thumb_cluster.outers(side=side)])

        return shape

    def create_main_shape(self, side: Side = Side.RIGHT) -> Shape:
        shape = self.create_key_plates(side=side)
        shape = self.add_connectors(shape=shape, side=side)
        shape = self.add_walls(shape=shape, side=side)
        shape = self.add_oled_mount(shape=shape, side=side)
        shape = self.add_trackball_in_wall_step1(shape=shape, side=side)
        shape = self.add_pcb_plate_cutouts(shape=shape, side=side)

        return self.engine.difference(shape, [self.block])

    @debug_export("debug_thumb_test_TODO-side_shape")
    def create_thumb_section_walls(self, side: Side = Side.RIGHT) -> Shape:
        thumb_shape = self.create_thumb_cluster(side=side)
        thumb_connector_shape = self.create_thumb_connectors()
        thumb_wall_shape = self.create_thumb_walls(side=side)
        thumb_connection_shape = self.thumb_cluster.connection(side=side)

        return self.engine.union(
            [
                thumb_shape,
                thumb_connector_shape,
                thumb_wall_shape,
                thumb_connection_shape,
            ]
        )

    def add_thumb_cluster_screw_holes(
        self, shape: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        return self.engine.difference(
            shape,
            [self.engine.union(self.thumb_cluster.holes(side=side))],
        )

    @debug_export(name="debug_thumb_test_1_shape")
    def add_trackball_precut(
        self, shape: Shape, precut: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        return self.engine.difference(shape, [precut])

    @debug_export(name="debug_thumb_test_2_shape")
    def add_trackball_shape(
        self, shape: Shape, trackball: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        return self.engine.union([shape, trackball])

    @debug_export(name="debug_thumb_test_3_shape")
    def add_trackball_cutout(
        self, shape: Shape, cutout: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        return self.engine.difference(shape, [cutout])

    @debug_export(name="debug_thumb_test_4_shape")
    def add_trackball_sensor(
        self, shape: Shape, sensor: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        return self.engine.union([shape, sensor])

    def add_thumb_cluster_trackball(
        self, shape: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        if not self.properties.has_trackball(side=side):
            return shape

        self.log.info("Has Trackball")
        trackball_components = self.thumb_cluster.trackball_components()

        shape = self.add_trackball_precut(
            shape=shape, precut=trackball_components.precut, side=side
        )
        shape = self.add_trackball_shape(
            shape=shape, trackball=trackball_components.shape, side=side
        )
        shape = self.add_trackball_cutout(
            shape=shape, cutout=trackball_components.cutout, side=side
        )
        shape = self.add_trackball_sensor(
            shape=shape, sensor=trackball_components.sensor, side=side
        )

        return shape

    def add_thumb_cluster_pcb_plate_cutouts(
        self, shape: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        if self.config.plate_pcb_clear:
            shape = self.engine.difference(
                shape, [self.thumb_cluster.pcb_plate_cutouts(side=side)]
            )

        return shape

    @debug_export(name="debug_thumb_test_5_shape")
    def create_thumb_section(self, side: Side = Side.RIGHT) -> Shape:
        shape = self.create_thumb_section_walls(side=side)
        shape = self.add_thumb_cluster_screw_holes(shape=shape, side=side)
        shape = self.add_thumb_cluster_trackball(shape=shape, side=side)
        shape = self.add_thumb_cluster_pcb_plate_cutouts(shape=shape, side=side)

        return self.engine.difference(shape, [self.block])

    @property
    def block(self) -> Shape:
        block = self.engine.box(350, 350, 40)
        block = self.engine.translate(block, (0, 0, -20))

        return block

    @debug_export(name="debug_thumb_test_6_shape")
    def join_main_shape_with_thumb_section(
        self, main_shape: Shape, thumb_section: Shape
    ) -> Shape:
        return self.engine.union([main_shape, thumb_section])

    def assemble_main_case_separable_thumb(
        self, main_shape: Shape, thumb_section: Shape, side: Side = Side.RIGHT
    ) -> t.Tuple[Shape, Shape]:
        thumb_section = self.engine.difference(thumb_section, [main_shape])
        if self.config.show_caps:
            thumb_section = self.engine.add([thumb_section, self.thumb_cluster.caps()])

            if self.properties.has_trackball(side=side):
                trackball_components = self.thumb_cluster.trackball_components()
                main_shape = self.engine.add([thumb_section, trackball_components.ball])

        return main_shape, thumb_section

    def assemble_main_case_combined(
        self, main_shape: Shape, thumb_section: Shape, side: Side = Side.RIGHT
    ) -> t.Tuple[Shape, Shape]:
        main_shape = self.join_main_shape_with_thumb_section(
            main_shape=main_shape, thumb_section=thumb_section
        )

        if self.config.show_caps:
            main_shape = self.engine.add([main_shape, self.thumb_cluster.caps()])
            if self.properties.has_trackball(side=side):
                trackball_components = self.thumb_cluster.trackball_components()
                main_shape = self.engine.add([main_shape, trackball_components.ball])

        if (
            self.config.trackball_in_wall
            and (side in [self.properties.trackball_side, Side.BOTH])
            and not self.config.separable_thumb
        ):
            main_shape = self.add_trackball(shape=main_shape, side=side)

        return main_shape, thumb_section

    def assemble_main_case(
        self, main_shape: Shape, thumb_section: Shape, side: Side = Side.RIGHT
    ) -> Shape:
        if self.config.separable_thumb:
            main_shape, thumb_section = self.assemble_main_case_separable_thumb(
                main_shape=main_shape, thumb_section=thumb_section, side=side
            )
        else:
            main_shape, thumb_section = self.assemble_main_case_combined(
                main_shape=main_shape, thumb_section=thumb_section, side=side
            )

        if self.config.show_caps:
            main_shape = self.engine.add([main_shape, self.caps.render()])

        if side is Side.LEFT:
            main_shape = self.engine.mirror(main_shape, "YZ")
            thumb_section = self.engine.mirror(thumb_section, "YZ")

        return main_shape, thumb_section

    def model_side(self, side: Side = Side.RIGHT) -> t.Tuple[Shape, Shape]:
        main_shape = self.create_main_shape(side=side)
        thumb_section = self.create_thumb_section(side=side)

        return self.assemble_main_case(
            main_shape=main_shape, thumb_section=thumb_section, side=side
        )

    def export_oled_mount_frame(self) -> None:
        if self.config.oled_mount_type is OledMount.UNDERCUT:
            self.export_file(
                shape=self.oled_mount.render_frame()[1], name="oled_undercut_test"
            )

        if self.config.oled_mount_type is OledMount.SLIDING:
            self.export_file(
                shape=self.oled_mount.render_frame()[1], name="oled_sliding_test"
            )

        if self.config.oled_mount_type is OledMount.CLIP:
            oled_mount_frame = self.oled_mount.render_frame()
            oled_clip = self.oled_mount.render_clip()
            self.export_file(shape=oled_clip, name="oled_clip")
            self.export_file(shape=oled_mount_frame[1], name="oled_clip_test")
            self.export_file(
                shape=self.engine.union([oled_mount_frame[1], oled_clip]),
                name="oled_clip_assy_test",
            )

    def render(self) -> None:
        print(
            f"Building Dacty Manuform {self.properties.rows}x{self.properties.columns}"
        )
        print(
            f"Thumb Cluster(s): {self.config.thumb_style} / {self.config.other_thumb}"
        )
        print(f"Rendering using {self.engine.kind} to {self.save_path}")
        mod_r, tmb_r = self.model_side(side=Side.RIGHT)
        self.export_file(shape=mod_r, name="right")
        self.export_file(shape=tmb_r, name="thumb_right")

        base = self.base_plate.render(side=Side.RIGHT)
        self.export_file(shape=base, name="right_plate")
        self.export_dxf(shape=base, name="right_plate")

        if self.properties.symmetry is Symmetry.ASYMMETRIC:
            mod_l, tmb_l = self.model_side(side=Side.LEFT)
            self.export_file(shape=mod_l, name="left")
            self.export_file(shape=tmb_l, name="thumb_left")

            base_l = self.engine.mirror(self.base_plate.render(side=Side.LEFT), "YZ")
            self.export_file(shape=base_l, name="left_plate")
            self.export_dxf(shape=base_l, name="left_plate")
        else:
            self.export_file(shape=self.engine.mirror(mod_r, "YZ"), name="left")

            base_l = self.engine.mirror(base, "YZ")
            self.export_file(shape=base_l, name="left_plate")
            self.export_dxf(shape=base_l, name="left_plate")

        self.export_oled_mount_frame()
        print("\n\n\n")
