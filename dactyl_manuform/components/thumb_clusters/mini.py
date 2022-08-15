#!/usr/bin/env python3
from __future__ import annotations

import typing as t

import numpy as np
from dactyl_manuform.interfaces.walls import ThumbClusterWallModel

from dactyl_manuform.types import Shape, Side, XY


class MiniThumbClusterWallModel(ThumbClusterWallModel):
    @property
    def screw_xy_positions_separable(self) -> t.Tuple[XY, ...]:
        return self.config.mini_separable_thumb_screw_xy_locations

    @property
    def screw_xy_positions(self) -> t.Tuple[XY, ...]:
        return self.config.mini_thumb_screw_xy_locations

    @property
    def mini_index_key(self) -> bool:
        return self.config.mini_index_key

    def place_tl(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (10, -23, 25))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-35, -16, -2))
        return shape

    def place_tr(self, shape: Shape) -> Shape:
        if self.mini_index_key:
            shape = self.engine.rotate(shape, (-25, 25, 0))
            shape = self.engine.translate(shape, self.thumb_origin)
            shape = self.engine.translate(shape, (-12.5, -10, 2))
        else:
            shape = self.engine.rotate(shape, (14, -15, 10))
            shape = self.engine.translate(shape, self.thumb_origin)
            shape = self.engine.translate(shape, (-15, -10, 5))

        return shape

    def place_ml(self, shape: Shape) -> Shape:
        raise RuntimeError("Minidox thumb cluster doesn't have ML key")

    def place_mr(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (10, -23, 25))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-23, -34, -6))
        return shape

    def place_bl(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (6, -32, 35))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-51, -25, -11.5))
        return shape

    def place_br(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (6, -34, 35))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-39, -43, -16))

        return shape

    def post_tr(self) -> Shape:
        return self.engine.translate(
            self.web_connectors.post(),
            (
                (self.properties.mount_width / 2) - self.post_adj,
                (self.properties.mount_height / 2) - self.post_adj,
                0,
            ),
        )

    def post_tl(self) -> Shape:
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -(self.properties.mount_width / 2) + self.post_adj,
                (self.properties.mount_height / 2) - self.post_adj,
                0,
            ),
        )

    def post_br(self) -> Shape:
        return self.engine.translate(
            self.web_connectors.post(),
            (
                (self.properties.mount_width / 2) - self.post_adj,
                -(self.properties.mount_height / 2) + self.post_adj,
                0,
            ),
        )

    def post_bl(self) -> Shape:
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -(self.properties.mount_width / 2) + self.post_adj,
                -(self.properties.mount_height / 2) + self.post_adj,
                0,
            ),
        )

    def layout_1x(self, shape: Shape, cap: bool = False) -> Shape:
        return self.engine.union(
            [
                self.place_mr(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_mr))
                ),
                self.place_br(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_br))
                ),
                self.place_tl(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_tl))
                ),
                self.place_bl(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_bl))
                ),
            ]
        )

    def layout_15x(self, shape: Shape, cap: bool = False, plate: bool = True) -> Shape:
        return self.engine.union(
            [self.place_tr(self.engine.rotate(shape, (0, 0, self.plate_rotation_tr)))]
        )

    def caps(self) -> Shape:
        t1 = self.layout_1x(self.key_caps.keycap(key_size=1.0))
        t15 = self.layout_15x(
            self.engine.rotate(
                self.key_caps.keycap(key_size=1.0), (0, 0, self.rad2deg(np.pi / 2))
            )
        )
        return t1.add(t15)

    def thumb_connectors(self) -> Shape:
        hulls = [
            # Top two
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.web_connectors.post_tr()),
                    self.place_tl(self.web_connectors.post_br()),
                    self.place_tr(self.post_tl()),
                    self.place_tr(self.post_bl()),
                ]
            ),
            # bottom two on the right
            self.engine.triangle_hulls(
                [
                    self.place_br(self.web_connectors.post_tr()),
                    self.place_br(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tl()),
                    self.place_mr(self.web_connectors.post_bl()),
                ]
            ),
            # bottom two on the left
            self.engine.triangle_hulls(
                [
                    self.place_mr(self.web_connectors.post_tr()),
                    self.place_mr(self.web_connectors.post_br()),
                    self.place_tr(self.post_br()),
                ]
            ),
            # between top and bottom row
            self.engine.triangle_hulls(
                [
                    self.place_br(self.web_connectors.post_tl()),
                    self.place_bl(self.web_connectors.post_bl()),
                    self.place_br(self.web_connectors.post_tr()),
                    self.place_bl(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tl()),
                    self.place_tl(self.web_connectors.post_bl()),
                    self.place_mr(self.web_connectors.post_tr()),
                    self.place_tl(self.web_connectors.post_br()),
                    self.place_tr(self.web_connectors.post_bl()),
                    self.place_mr(self.web_connectors.post_tr()),
                    self.place_tr(self.web_connectors.post_br()),
                ]
            ),
            # top two to the main keyboard, starting on the left
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.web_connectors.post_tl()),
                    self.place_bl(self.web_connectors.post_tr()),
                    self.place_tl(self.web_connectors.post_bl()),
                    self.place_bl(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tr()),
                    self.place_tl(self.web_connectors.post_bl()),
                    self.place_tl(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tr()),
                ]
            ),
            # top two to the main keyboard, starting on the left
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.web_connectors.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 0, self.properties.cornerrow
                    ),
                    self.place_tl(self.web_connectors.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 0, self.properties.cornerrow
                    ),
                    self.place_tr(self.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 1, self.properties.cornerrow
                    ),
                    self.place_tr(self.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 1, self.properties.cornerrow
                    ),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 2, self.properties.lastrow
                    ),
                    self.place_tr(self.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 2, self.properties.lastrow
                    ),
                    self.place_tr(self.post_br()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 2, self.properties.lastrow
                    ),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 3, self.properties.lastrow
                    ),
                ]
            ),
        ]

        return self.engine.union(hulls)

    def connection(self, side: Side = Side.RIGHT) -> Shape:
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        shape = self.engine.union(
            [
                self.engine.bottom_hull(
                    [
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate2(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate3(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate2(-0.3, 1),
                            )
                        ),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate3(-0.3, 1),
                            )
                        ),
                    ]
                )
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.engine.hull_from_shapes(
                    [
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate2(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate3(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate2(-0.3, 1),
                            )
                        ),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate3(-0.3, 1),
                            )
                        ),
                        self.place_tl(self.web_connectors.post_tl()),
                    ]
                ),
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.engine.hull_from_shapes(
                    [
                        self.placement.left_key_place(
                            self.web_connectors.post(),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate1(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate2(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate3(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.place_tl(self.web_connectors.post_tl()),
                    ]
                ),
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.engine.hull_from_shapes(
                    [
                        self.placement.left_key_place(
                            self.web_connectors.post(),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.left_key_place(
                            self.engine.translate(
                                self.web_connectors.post(), self.wall_locate1(-1, 0)
                            ),
                            self.properties.cornerrow,
                            -1,
                            low_corner=True,
                            side=side,
                        ),
                        self.placement.key_place(
                            self.web_connectors.post_bl(), 0, self.properties.cornerrow
                        ),
                        self.place_tl(self.web_connectors.post_tl()),
                    ]
                ),
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.engine.hull_from_shapes(
                    [
                        self.place_bl(self.web_connectors.post_tr()),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate1(-0.3, 1),
                            )
                        ),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate2(-0.3, 1),
                            )
                        ),
                        self.place_bl(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate3(-0.3, 1),
                            )
                        ),
                        self.place_tl(self.web_connectors.post_tl()),
                    ]
                ),
            ]
        )

        return shape

    def walls(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        # thumb, walls
        shape = self.engine.union(
            [
                self.wall_brace(
                    self.place_mr,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                    self.place_tr,
                    0,
                    -1,
                    self.post_br(),
                )
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_mr,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                    self.place_mr,
                    0,
                    -1,
                    self.web_connectors.post_bl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_br,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                    self.place_br,
                    0,
                    -1,
                    self.web_connectors.post_bl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_bl,
                    0,
                    1,
                    self.web_connectors.post_tr(),
                    self.place_bl,
                    0,
                    1,
                    self.web_connectors.post_tl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_br,
                    -1,
                    0,
                    self.web_connectors.post_tl(),
                    self.place_br,
                    -1,
                    0,
                    self.web_connectors.post_bl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_bl,
                    -1,
                    0,
                    self.web_connectors.post_tl(),
                    self.place_bl,
                    -1,
                    0,
                    self.web_connectors.post_bl(),
                ),
            ]
        )
        # thumb, corners
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_br,
                    -1,
                    0,
                    self.web_connectors.post_bl(),
                    self.place_br,
                    0,
                    -1,
                    self.web_connectors.post_bl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_bl,
                    -1,
                    0,
                    self.web_connectors.post_tl(),
                    self.place_bl,
                    0,
                    1,
                    self.web_connectors.post_tl(),
                ),
            ]
        )
        # thumb, tweeners
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_mr,
                    0,
                    -1,
                    self.web_connectors.post_bl(),
                    self.place_br,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_bl,
                    -1,
                    0,
                    self.web_connectors.post_bl(),
                    self.place_br,
                    -1,
                    0,
                    self.web_connectors.post_tl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_tr,
                    0,
                    -1,
                    self.post_br(),
                    (
                        lambda sh: self.placement.key_place(
                            sh, 3, self.properties.lastrow
                        )
                    ),
                    0,
                    -1,
                    self.web_connectors.post_bl(),
                ),
            ]
        )

        return shape

    def pcb_plate_cutouts(self, side: Side = Side.RIGHT) -> t.List[Shape]:
        shape = self.layout_1x(self.cutout(side=side))
        shape = self.engine.union([shape, self.layout_15x(self.cutout(side=side))])

        return shape

    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        shape = self.layout_1x(self.single_plate.render(side=side))
        shape = self.engine.union(
            [shape, self.layout_15x(self.single_plate.render(side=side))]
        )

        return shape
