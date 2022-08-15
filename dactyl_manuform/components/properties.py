#!/usr/bin/env python3
from __future__ import annotations

import numpy as np

from dactyl_manuform.config import DactylManuformConfig
from dactyl_manuform.interfaces.single_plate import SinglePlateComponent
from dactyl_manuform.types import Side, Symmetry, ThumbStyle


class DactylManuformProperties:
    def __init__(
        self,
        config: DactylManuformConfig,
        single_plate: SinglePlateComponent,
    ) -> None:
        super().__init__()
        self.config = config
        self.single_plate = single_plate

    @property
    def columns(self) -> int:
        return self.config.ncols

    @property
    def rows(self) -> int:
        return self.config.nrows

    @property
    def keyboard_z_offset(self) -> float:
        return self.config.keyboard_z_offset

    @property
    def column_style(self):
        if self.rows > 5:
            return self.config.column_style_gt5

        return self.config.column_style

    @property
    def column_curvature(self) -> float:
        return self.config.alpha

    @property
    def row_curvature(self) -> float:
        return self.config.beta

    @property
    def plate_thickness(self):
        return self.config.plate_thickness

    @property
    def cap_top_height(self) -> float:
        return self.plate_thickness + self.config.sa_profile_key_height

    @property
    def row_radius(self) -> float:
        height = (self.mount_height + self.config.extra_height) / 2
        return height / np.sin(self.column_curvature / 2) + self.cap_top_height

    @property
    def column_radius(self) -> float:
        width = (self.mount_width + self.config.extra_width) / 2
        return width / np.sin(self.row_curvature / 2) + self.cap_top_height

    @property
    def centerrow(self) -> int:
        return self.rows - self.config.centerrow_offset

    @property
    def centercol(self) -> int:
        return self.config.centercol

    @property
    def lastrow(self) -> int:
        return self.config.nrows - 1

    @property
    def lastcol(self) -> int:
        return self.config.ncols - 1

    @property
    def cornerrow(self) -> int:
        if self.config.reduced_outer_cols > 0 or self.config.reduced_inner_cols > 0:
            return self.lastrow - 1

        return self.lastrow

    @property
    def reduced_inner_columns(self) -> int:
        return self.config.reduced_inner_cols

    @property
    def reduced_outer_columns(self) -> int:
        return self.config.reduced_outer_cols

    @property
    def mount_width(self) -> float:
        return self.single_plate.mount_width

    @property
    def mount_height(self) -> float:
        return self.single_plate.mount_height

    @property
    def mount_thickness(self) -> float:
        return self.single_plate.mount_thickness

    @property
    def trackball_side(self) -> Side:
        return self.config.ball_side

    @property
    def trackball_in_wall(self) -> bool:
        return self.config.trackball_in_wall

    @property
    def thumb_style(self) -> ThumbStyle:
        return self.config.thumb_style

    @property
    def minidox_key_size(self) -> float:
        return self.config.minidox_Usize

    @property
    def symmetry(self):
        if self.single_plate.hotswappable:
            return Symmetry.ASYMMETRIC

        has_trackball = self.config.thumb_style in [
            ThumbStyle.TRACKBALL_CJ,
            ThumbStyle.TRACKBALL_ORBYL,
        ]
        has_trackball = self.config.trackball_in_wall or has_trackball

        if has_trackball and self.config.ball_side is not Side.BOTH:
            return Symmetry.ASYMMETRIC

        return Symmetry.SYMMETRIC

    def adjustable_plate_size(self, key_size: float = 1.5) -> float:
        return (key_size * self.config.sa_length - self.mount_height) / 2

    def key_dimension(self, key_size: float = 1.5) -> float:
        return key_size * self.config.sa_length

    # TODO: This should move into the thumb cluster rendering - they know if they have a TB
    def has_trackball(self, side: Side = Side.RIGHT) -> bool:
        return self.thumb_style in [
            ThumbStyle.TRACKBALL_CJ,
            ThumbStyle.TRACKBALL_ORBYL,
        ] and self.trackball_side in [Side.BOTH, side]
