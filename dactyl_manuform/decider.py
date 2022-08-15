#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.config import DactylManuformConfig, RenderConfiguration
from dactyl_manuform.types import (
    ColumnStyle,
    ControllerMount,
    KeyCapType,
    OledMount,
    PlateStyle,
    ScrewOffset,
    Side,
    ThumbStyle,
)


class DactylManuformComponentDecider:
    def __init__(self, config: DactylManuformConfig) -> None:
        self.config = config
        # TODO: Enable using actual overrides
        self.render_configuration = RenderConfiguration()

    @property
    def engine(self) -> str:
        if self.render_configuration.engine:
            return self.render_configuration.engine

        return self.config.engine

    @property
    def properties(self) -> str:
        if self.render_configuration.properties:
            return self.render_configuration.properties

        return "ModelProperties"

    @property
    def placement(self) -> str:
        if self.render_configuration.placement:
            return self.render_configuration.placement

        column_style = self.config.column_style
        if self.config.nrows > 5:
            column_style = self.config.column_style_gt5

        if column_style is ColumnStyle.FIXED:
            return "FixedKeyPlacementTransformer"

        if column_style is ColumnStyle.ORTHOGRAPHIC:
            return "OrthographicKeyPlacementTransformer"

        return "DefaultKeyPlacementTransformer"

    @property
    def single_plate(self) -> str:
        if self.render_configuration.single_plate:
            return self.render_configuration.single_plate

        if self.config.plate_style in [PlateStyle.NOTCH, PlateStyle.HS_NOTCH]:
            return "NotchSinglePlate"

        if self.config.plate_style in [PlateStyle.NUB, PlateStyle.HS_NUB]:
            return "NubSinglePlate"

        if self.config.plate_style in [PlateStyle.UNDERCUT, PlateStyle.HS_UNDERCUT]:
            return "UndercutSinglePlate"

        return "SquareHoleSinglePate"

    @property
    def key_holes(self) -> str:
        if self.render_configuration.key_holes:
            return self.render_configuration.key_holes

        return "DefaultKeyHolesModel"

    @property
    def connectors(self) -> str:
        if self.render_configuration.connectors:
            return self.render_configuration.connectors

        return "DefaultWebConnectorModel"

    @property
    def case_walls(self) -> str:
        if self.render_configuration.case_walls:
            return self.render_configuration.case_walls

        return "DefaultCaseModel"

    @property
    def back_wall(self) -> str:
        if self.render_configuration.back_wall:
            return self.render_configuration.back_wall

        return "DefaultBackWallModel"

    @property
    def front_wall(self) -> str:
        if self.render_configuration.front_wall:
            return self.render_configuration.front_wall

        return "DefaultFrontWallModel"

    @property
    def left_wall(self) -> str:
        if self.render_configuration.left_wall:
            return self.render_configuration.left_wall

        return "DefaultLeftWallModel"

    @property
    def right_wall(self) -> str:
        if self.render_configuration.right_wall:
            return self.render_configuration.right_wall

        return "DefaultRightWallModel"

    @property
    def screw_inserts(self) -> str:
        if self.render_configuration.screw_inserts:
            return self.render_configuration.screw_inserts

        if self.config.screws_offset is ScrewOffset.INSIDE:
            return "InsideScrewInsertModel"

        if self.config.screws_offset is ScrewOffset.OUTSIDE:
            return "OutsideScrewInsertModel"

        return "DefaultScrewInsertModel"

    @property
    def controller_mount(self) -> str:
        if self.render_configuration.controller_mount:
            return self.render_configuration.controller_mount

        if self.config.controller_mount_type is ControllerMount.USB_WALL:
            return "UsbWallControllerMountModel"

        if self.config.controller_mount_type is ControllerMount.RJ9_USB_WALL:
            return "UsbWallControllerMountModel"

        if self.config.controller_mount_type is ControllerMount.USB_TEENSY:
            return "TeensyControllerMountModel"

        if self.config.controller_mount_type is ControllerMount.RJ9_USB_TEENSY:
            return "RJ9TeensyControllerMountModel"

        if self.config.controller_mount_type is ControllerMount.EXTERNAL:
            return "ExternalControllerMountModel"

        if self.config.controller_mount_type is ControllerMount.PCB_MOUNT:
            return "PcbMountControllerMountModel"

        return "NoControllerMountModel"

    @property
    def plate_pcb_cutouts(self) -> str:
        if self.render_configuration.plate_pcb_cutouts:
            return self.render_configuration.plate_pcb_cutouts

        return "DefaultPlatePcbCutoutModel"

    @property
    def _left_thumb_style(self):
        if self.config.thumb_style in [
            ThumbStyle.TRACKBALL_CJ,
            ThumbStyle.TRACKBALL_ORBYL,
        ]:
            if self.config.ball_side in [Side.LEFT, Side.BOTH]:
                return self.config.thumb_style

            return self.config.other_thumb

        return self.config.thumb_style

    @property
    def _right_thumb_style(self) -> ThumbStyle:
        if self.config.thumb_style in [
            ThumbStyle.TRACKBALL_CJ,
            ThumbStyle.TRACKBALL_ORBYL,
        ]:
            if self.config.ball_side in [Side.RIGHT, Side.BOTH]:
                return self.config.thumb_style

            return self.config.other_thumb

        return self.config.thumb_style

    @property
    def left_thumb_cluster(self) -> str:
        if self.render_configuration.left_thumb_cluster:
            return self.render_configuration.left_thumb_cluster

        return self._thumb_cluster_model(style=self._left_thumb_style)

    @property
    def right_thumb_cluster(self) -> str:
        if self.render_configuration.right_thumb_cluster:
            return self.render_configuration.right_thumb_cluster

        return self._thumb_cluster_model(self._right_thumb_style)

    def _thumb_cluster_model(self, style: ThumbStyle) -> str:
        if style is ThumbStyle.CARBONFET:
            return "CarbonfetThumbClusterWallModel"

        if style is ThumbStyle.TRACKBALL_CJ:
            return "CJThumbClusterWallModel"

        if style is ThumbStyle.MINI:
            return "MiniThumbClusterWallModel"

        if style is ThumbStyle.MINIDOX:
            return "MinidoxThumbClusterWallModel"

        if style is ThumbStyle.TRACKBALL_ORBYL:
            return "OrbylThumbClusterWallModel"

        # Default cluster
        if self.config.default_1U_cluster:
            return "Default1UThumbClusterWallModel"

        return "DefaultThumbClusterWallModel"

    @property
    def thumb_cluster_properties(self) -> str:
        if self.render_configuration.thumb_cluster_properties:
            return self.render_configuration.thumb_cluster_properties

        return "ThumbClusterProperties"

    @property
    def oled_mount(self) -> str:
        if self.render_configuration.oled_mount:
            return self.render_configuration.oled_mount

        if self.config.oled_mount_type is OledMount.CLIP:
            return "ClipOledMountModel"

        if self.config.oled_mount_type is OledMount.SLIDING:
            return "SlidingOledMountModel"

        if self.config.oled_mount_type is OledMount.UNDERCUT:
            return "UndercutOledMountModel"

        return "NoOledMountModel"

    @property
    def key_caps(self) -> str:
        if self.render_configuration.key_caps:
            return self.render_configuration.key_caps

        if self.config.show_caps is KeyCapType.CHOC:
            return "ChocKeyCapModel"

        return "DefaultKeyCapModel"

    @property
    def base_plate(self) -> str:
        if self.render_configuration.base_plate:
            return self.render_configuration.base_plate

        return "DefaultBasePlateModel"

    @property
    def trackball_components(self) -> str:
        if self.render_configuration.trackball_components:
            return self.render_configuration.trackball_components

        if self.config.trackball_modular:
            return "ModularTrackballPartsComponent"

        return "DefaultTrackballPartsComponent"

    @property
    def model_builder(self) -> str:
        if self.render_configuration.model_builder:
            return self.render_configuration.model_builder

        return "DefaultDactylManuformBuilder"
