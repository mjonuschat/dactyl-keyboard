#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from logging import Logger

import numpy as np
from dactyl_manuform.components.properties import DactylManuformProperties

from dactyl_manuform.config import DactylManuformConfig, OledMountConfiguration
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.interfaces.connector import ConnectorComponent
from dactyl_manuform.interfaces.engine import Engine
from dactyl_manuform.interfaces.key_caps import KeycapModel
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.interfaces.plate_pcb_cutout import PcbCutoutModel
from dactyl_manuform.interfaces.single_plate import SinglePlateComponent
from dactyl_manuform.interfaces.thumb_cluster import ThumbClusterProperties
from dactyl_manuform.interfaces.trackball_parts import TrackballPartsComponent
from dactyl_manuform.types import (
    OledMount,
    Shape,
    ShiftValues,
    Side,
    TrackballComponents,
    XY,
    XYZ,
)


class AbstractWallComponent(AbstractComponentClass, ABC):
    def __init__(
        self,
        config: DactylManuformConfig,
        engine: Engine,
        log: Logger,
        properties: DactylManuformProperties,
        connectors: ConnectorComponent,
        placement: KeyPlacementTransformer,
    ) -> None:
        super().__init__(config=config, engine=engine, log=log)

        self.properties = properties
        self.connectors = connectors
        self.placement = placement

    def wall_locate1(self, dx: float, dy: float) -> XYZ:
        self.log.debug("wall_locate1()")
        return dx * self.config.wall_thickness, dy * self.config.wall_thickness, -1.0

    def wall_locate2(self, dx: float, dy: float) -> XYZ:
        self.log.debug("wall_locate2()")
        return (
            dx * self.config.wall_x_offset,
            dy * self.config.wall_y_offset,
            -self.config.wall_z_offset,
        )

    def wall_locate3(self, dx: float, dy: float, back: bool = False) -> XYZ:
        self.log.debug("wall_locate3()")
        if back:
            return (
                dx * (self.config.wall_x_offset + self.config.wall_base_x_thickness),
                dy * (self.config.wall_y_offset + self.config.wall_base_back_thickness),
                -self.config.wall_z_offset,
            )
        else:
            return (
                dx * (self.config.wall_x_offset + self.config.wall_base_x_thickness),
                dy * (self.config.wall_y_offset + self.config.wall_base_y_thickness),
                -self.config.wall_z_offset,
            )

    def wall_brace(
        self,
        place1: t.Callable[..., Shape],
        dx1: float,
        dy1: float,
        post1: Shape,
        place2: t.Callable[..., Shape],
        dx2: float,
        dy2: float,
        post2: Shape,
        back: bool = False,
        skeleton: bool = False,
        skel_bottom: bool = False,
    ):
        self.log.debug("wall_brace()")
        hulls = [place1(post1)]

        if not skeleton:
            hulls.append(
                place1(self.engine.translate(post1, self.wall_locate1(dx1, dy1)))
            )
            hulls.append(
                place1(self.engine.translate(post1, self.wall_locate2(dx1, dy1)))
            )
        if not skeleton or skel_bottom:
            hulls.append(
                place1(self.engine.translate(post1, self.wall_locate3(dx1, dy1, back)))
            )

        hulls.append(place2(post2))
        if not skeleton:
            hulls.append(
                place2(self.engine.translate(post2, self.wall_locate1(dx2, dy2)))
            )
            hulls.append(
                place2(self.engine.translate(post2, self.wall_locate2(dx2, dy2)))
            )

        if not skeleton or skel_bottom:
            hulls.append(
                place2(self.engine.translate(post2, self.wall_locate3(dx2, dy2, back)))
            )

        shape1 = self.engine.hull_from_shapes(hulls)

        hulls = []
        if not skeleton:
            hulls.append(
                place1(self.engine.translate(post1, self.wall_locate2(dx1, dy1)))
            )
        if not skeleton or skel_bottom:
            hulls.append(
                place1(self.engine.translate(post1, self.wall_locate3(dx1, dy1, back)))
            )
        if not skeleton:
            hulls.append(
                place2(self.engine.translate(post2, self.wall_locate2(dx2, dy2)))
            )
        if not skeleton or skel_bottom:
            hulls.append(
                place2(self.engine.translate(post2, self.wall_locate3(dx2, dy2, back)))
            )

        if len(hulls) > 0:
            shape2 = self.engine.bottom_hull(hulls)
            shape1 = self.engine.union([shape1, shape2])

        return shape1

    def key_wall_brace(
        self,
        x1: int,
        y1: int,
        dx1: float,
        dy1: float,
        post1: Shape,
        x2: int,
        y2: int,
        dx2: float,
        dy2: float,
        post2: Shape,
        back: bool = False,
        skeleton: bool = False,
        skel_bottom: bool = False,
    ):
        self.log.debug("key_wall_brace()")
        return self.wall_brace(
            (lambda shape: self.placement.key_place(shape, x1, y1)),
            dx1,
            dy1,
            post1,
            (lambda shape: self.placement.key_place(shape, x2, y2)),
            dx2,
            dy2,
            post2,
            back,
            skeleton=skeleton,
            skel_bottom=False,
        )


class WallModel(AbstractWallComponent, ABC):
    @abstractmethod
    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        ...


class BackWallModel(WallModel, ABC):
    ...


class FrontWallModel(WallModel, ABC):
    ...


class LeftWallModel(WallModel, ABC):
    ...


class RightWallModel(WallModel, ABC):
    ...


class ScrewInsertModel(WallModel, ABC):
    @property
    def oled_config(self) -> t.Optional[OledMountConfiguration]:
        if self.config.oled_mount_type is OledMount.NONE:
            return

        return OledMountConfiguration.parse_obj(
            self.config.oled_configurations[self.config.oled_mount_type]
        )

    @property
    def left_wall_lower_y_offset(self) -> float:
        offset = self.config.left_wall_lower_y_offset
        if oled_config := self.oled_config:
            offset = oled_config.left_wall_lower_y_offset

        return offset

    @property
    def outer_radius(self) -> float:
        return self.config.screw_insert_outer_radius

    @property
    def bottom_radius(self) -> float:
        return self.config.screw_insert_bottom_radius

    @property
    def top_radius(self) -> float:
        return self.config.screw_insert_top_radius

    @property
    def height(self) -> float:
        return self.config.screw_insert_height

    @abstractmethod
    def shift(self, column: int, row: int) -> ShiftValues:
        ...

    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        raise RuntimeError("Calling render() on a screw insert is not supported.")

    def shape(self, bottom_radius: float, top_radius: float, height: float) -> Shape:
        self.log.debug("screw_insert_shape()")
        if bottom_radius == top_radius:
            base = self.engine.cylinder(radius=bottom_radius, height=height)
        else:
            base = self.engine.translate(
                self.engine.cone(r1=bottom_radius, r2=top_radius, height=height),
                (0, 0, -height / 2),
            )

        shape = self.engine.union(
            (
                base,
                self.engine.translate(
                    self.engine.sphere(top_radius), (0, 0, height / 2)
                ),
            )
        )
        return shape

    def insert(
        self,
        column: int,
        row: int,
        bottom_radius: float,
        top_radius: float,
        height: float,
        side: Side = Side.RIGHT,
    ):
        shift = self.shift(column=column, row=row)

        if shift.up:
            position = self.placement.key_position(
                list(
                    np.array(self.wall_locate2(0, 1))
                    + np.array(
                        [
                            0,
                            (self.properties.mount_height / 2) + shift.up_adjust,
                            0,
                        ]
                    )
                ),
                column,
                row,
            )
        elif shift.down:
            position = self.placement.key_position(
                list(
                    np.array(self.wall_locate2(0, -1))
                    - np.array(
                        [
                            0,
                            (self.properties.mount_height / 2) + shift.down_adjust,
                            0,
                        ]
                    )
                ),
                column,
                row,
            )
        elif shift.left:
            position = list(
                np.array(self.placement.left_key_position(row, 0, side=side))
                + np.array(self.wall_locate3(-1, 0))
                + np.array((shift.left_adjust, 0, 0))
            )
        else:
            position = self.placement.key_position(
                list(
                    np.array(self.wall_locate2(1, 0))
                    + np.array([(self.properties.mount_height / 2), 0, 0])
                    + np.array((shift.right_adjust, 0, 0))
                ),
                column,
                row,
            )

        shape = self.shape(bottom_radius, top_radius, height)
        shape = self.engine.translate(shape, (position[0], position[1], height / 2))

        return shape

    def outers(self, offset: float = 0.0, side: Side = Side.RIGHT) -> Shape:
        return self.all_shapes(
            bottom_radius=self.outer_radius,
            top_radius=self.outer_radius,
            height=self.height + 1.5,
            offset=offset,
            side=side,
        )

    def holes(self, side: Side = Side.RIGHT) -> Shape:
        return self.all_shapes(
            bottom_radius=self.bottom_radius,
            top_radius=self.top_radius,
            height=self.height + 0.02,
            offset=-0.01,
            side=side,
        )

    def screw_holes(self, side: Side = Side.RIGHT) -> Shape:
        return self.all_shapes(bottom_radius=1.7, top_radius=1.7, height=350, side=side)

    def all_shapes(
        self,
        bottom_radius: float,
        top_radius: float,
        height: float,
        offset: float = 0.0,
        side: Side = Side.RIGHT,
    ) -> Shape:
        self.log.debug("screw_insert_all_shapes()")

        shape = (
            self.engine.translate(
                self.insert(0, 0, bottom_radius, top_radius, height, side=side),
                (0, 0, offset),
            ),
            self.engine.translate(
                self.insert(
                    0,
                    self.properties.cornerrow,
                    bottom_radius,
                    top_radius,
                    height,
                    side=side,
                ),
                (0, self.left_wall_lower_y_offset, offset),
            ),
            self.engine.translate(
                self.insert(
                    3,
                    self.properties.lastrow,
                    bottom_radius,
                    top_radius,
                    height,
                    side=side,
                ),
                (0, 0, offset),
            ),
            self.engine.translate(
                self.insert(3, 0, bottom_radius, top_radius, height, side=side),
                (0, 0, offset),
            ),
            self.engine.translate(
                self.insert(
                    self.properties.lastcol,
                    0,
                    bottom_radius,
                    top_radius,
                    height,
                    side=side,
                ),
                (0, 0, offset),
            ),
            self.engine.translate(
                self.insert(
                    self.properties.lastcol,
                    self.properties.cornerrow,
                    bottom_radius,
                    top_radius,
                    height,
                    side=side,
                ),
                (0, 0, offset),
            ),
        )

        return shape
