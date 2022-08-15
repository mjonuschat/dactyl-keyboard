#!/usr/bin/env python3
from __future__ import annotations

from abc import abstractmethod

import numpy as np

from dactyl_manuform.components.properties import DactylManuformProperties
from dactyl_manuform.interfaces.base import AbstractComponentClass
from dactyl_manuform.interfaces.key_placement import KeyPlacementTransformer
from dactyl_manuform.interfaces.thumb_cluster import ThumbClusterProperties
from dactyl_manuform.interfaces.trackball_parts import TrackballPartsComponent
from dactyl_manuform.types import TrackballComponents, XYZ


class InWallTrackballComponent(AbstractComponentClass):
    def __init__(
        self,
        properties: DactylManuformProperties,
        thumb_properties: ThumbClusterProperties,
        placement: KeyPlacementTransformer,
        trackball_components: TrackballPartsComponent,
    ):
        super().__init__()

        self.properties = properties
        self.thumb_properties = thumb_properties
        self.placement = placement
        self.components = trackball_components

    @property
    def thumb_offsets(self) -> XYZ:
        return self.thumb_properties.offsets

    @property
    def thumb_origin(self) -> XYZ:
        return self.thumb_properties.origin

    @property
    @abstractmethod
    def trackball_position(self) -> XYZ:
        ...

    @property
    @abstractmethod
    def trackball_rotation(self) -> XYZ:
        ...

    def render(self) -> TrackballComponents:
        return self.components.generate(
            position=self.trackball_position, rotation=self.trackball_rotation
        )

    @property
    def base_pt1(self) -> XYZ:
        # TODO: Return type?
        base_pt = self.placement.key_position(
            list(
                np.array([-self.properties.mount_width / 2, 0, 0])
                + np.array([0, (self.properties.mount_height / 2), 0])
            ),
            0,
            self.properties.cornerrow - self.ball_center_row - 1,
        )

        return base_pt[0], base_pt[1], base_pt[2]

    @property
    def base_pt2(self) -> XYZ:
        base_pt = self.placement.key_position(
            list(
                np.array([-self.properties.mount_width / 2, 0, 0])
                + np.array([0, (self.properties.mount_height / 2), 0])
            ),
            0,
            self.properties.cornerrow - self.ball_center_row + 1,
        )

        return base_pt[0], base_pt[1], base_pt[2]

    @property
    def trackball_position(self) -> XYZ:
        base_pt1 = self.base_pt1
        base_pt2 = self.base_pt2

        return (
            (np.array(base_pt1) + np.array(base_pt2)) / 2.0
            + np.array(((-self.left_wall_x_offset / 2), 0, 0))
            + np.array(self.translational_offset)
        )

    @property
    def trackball_rotation(self) -> XYZ:
        base_pt1 = self.base_pt1
        base_pt2 = self.base_pt2

        angle_x = np.arctan2(base_pt1[2] - base_pt2[2], base_pt1[1] - base_pt2[1])
        angle_z = np.arctan2(base_pt1[0] - base_pt2[0], base_pt1[1] - base_pt2[1])

        return XYZ(
            self.rad2deg(angle_x),
            0,
            self.rad2deg(angle_z),
        ) + np.array(self.rotation_offset)

    @property
    def ball_center_row(self) -> float:
        return self.config.tbiw_ball_center_row

    @property
    def translational_offset(self) -> XYZ:
        return self.config.tbiw_translational_offset

    @property
    def rotation_offset(self) -> XYZ:
        return self.config.tbiw_rotation_offset

    @property
    def left_wall_x_offset(self) -> float:
        return self.config.tbiw_left_wall_x_offset_override
