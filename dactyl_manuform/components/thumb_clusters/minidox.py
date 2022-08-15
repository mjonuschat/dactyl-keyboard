#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.interfaces.walls import ThumbClusterWallModel

from dactyl_manuform.types import Shape, Side, XY


class MinidoxThumbClusterWallModel(ThumbClusterWallModel):
    @property
    def screw_xy_positions_separable(self) -> t.Tuple[XY, ...]:
        return self.adjust_xy_positions(
            self.config.minidox_separable_thumb_screw_xy_locations
        )

    @property
    def screw_xy_positions(self) -> t.Tuple[XY, ...]:
        return self.adjust_xy_positions(self.config.minidox_thumb_screw_xy_locations)

    def adjust_xy_positions(self, positions: t.Tuple[XY, ...]) -> t.Tuple[XY, ...]:
        first, *other = positions
        first = (
            first[0],
            first[1] + -0.4 * (self.minidox_key_size - 1) * self.config.sa_length,
        )
        return first, *other

    @property
    def minidox_key_size(self) -> float:
        return self.config.minidox_Usize

    def place_tl(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (10, -23, 25))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-35, -16, -2))
        return shape

    def place_tr(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (14, -15, 10))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-15, -10, 5))
        return shape

    def place_ml(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (6, -34, 40))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-53, -26, -12))
        return shape

    def place_mr(self, shape: Shape) -> Shape:
        raise RuntimeError("Minidox thumb cluster doesn't have MR key")

    def place_bl(self, shape: Shape) -> Shape:
        raise RuntimeError("Minidox thumb cluster doesn't have BL key")

    def place_br(self, shape: Shape) -> Shape:
        raise RuntimeError("Minidox thumb cluster doesn't have BR key")

    def post_tr(self) -> Shape:
        self.log.debug("thumb_post_tr()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                (self.properties.mount_width / 2) - self.post_adj,
                (
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.minidox_key_size)
                )
                - self.post_adj,
                0,
            ),
        )

    def post_tl(self) -> Shape:
        self.log.debug("thumb_post_tl()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -(self.properties.mount_width / 2) + self.post_adj,
                (
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.minidox_key_size)
                )
                - self.post_adj,
                0,
            ),
        )

    def post_br(self) -> Shape:
        self.log.debug("thumb_post_br()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                (self.properties.mount_width / 2) - self.post_adj,
                -(
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.minidox_key_size)
                )
                + self.post_adj,
                0,
            ),
        )

    def post_bl(self) -> Shape:
        self.log.debug("thumb_post_bl()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -(self.properties.mount_width / 2) + self.post_adj,
                -(
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.minidox_key_size)
                )
                + self.post_adj,
                0,
            ),
        )

    def layout_fx(self, shape: Shape) -> Shape:
        return self.engine.union(
            [
                self.place_tr(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_tr))
                ),
                self.place_tl(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_tl))
                ),
                self.place_ml(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_ml))
                ),
            ]
        )

    def layout_1x(self, shape: Shape, cap: bool = False) -> Shape:
        raise RuntimeError("Minidox thumb cluster uses a variable key size")

    def layout_15x(self, shape: Shape, cap: bool = False, plate: bool = True) -> Shape:
        raise RuntimeError("Minidox thumb cluster uses a variable key size")

    def caps(self) -> Shape:
        return self.layout_fx(self.key_caps.keycap(key_size=1.0))

    def thumb_connectors(self) -> Shape:
        hulls = [
            # Top two
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.post_tr()),
                    self.place_tl(self.post_br()),
                    self.place_tr(self.post_tl()),
                    self.place_tr(self.post_bl()),
                ]
            ),
            # bottom two on the right
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.post_tl()),
                    self.place_tl(self.post_bl()),
                    self.place_ml(self.post_tr()),
                    self.place_ml(self.post_br()),
                ]
            ),
            # top two to the main keyboard, starting on the left
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 0, self.properties.cornerrow
                    ),
                    self.place_tl(self.post_tr()),
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
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate2(-0.3, 1)
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate3(-0.3, 1)
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
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate2(-0.3, 1)
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate3(-0.3, 1)
                            )
                        ),
                        self.place_tl(self.post_tl()),
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
                        self.place_tl(self.post_tl()),
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
                        self.place_tl(self.post_tl()),
                    ]
                ),
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.engine.hull_from_shapes(
                    [
                        self.place_ml(self.post_tr()),
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate1(0, 1)
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate2(0, 1)
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.post_tr(), self.wall_locate3(0, 1)
                            )
                        ),
                        self.place_tl(self.post_tl()),
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
                    self.place_tr,
                    0,
                    -1,
                    self.post_br(),
                    self.place_tr,
                    0,
                    -1,
                    self.post_bl(),
                )
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_tr,
                    0,
                    -1,
                    self.post_bl(),
                    self.place_tl,
                    0,
                    -1,
                    self.post_br(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_tl,
                    0,
                    -1,
                    self.post_br(),
                    self.place_tl,
                    0,
                    -1,
                    self.post_bl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_tl,
                    0,
                    -1,
                    self.post_bl(),
                    self.place_ml,
                    -1,
                    -1,
                    self.post_br(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_ml,
                    -1,
                    -1,
                    self.post_br(),
                    self.place_ml,
                    0,
                    -1,
                    self.post_bl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_ml,
                    0,
                    -1,
                    self.post_bl(),
                    self.place_ml,
                    -1,
                    0,
                    self.post_bl(),
                ),
            ]
        )
        # thumb, corners
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_ml,
                    -1,
                    0,
                    self.post_bl(),
                    self.place_ml,
                    -1,
                    0,
                    self.post_tl(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_ml,
                    -1,
                    0,
                    self.post_tl(),
                    self.place_ml,
                    0,
                    1,
                    self.post_tl(),
                ),
            ]
        )
        # thumb, tweeners
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_ml,
                    0,
                    1,
                    self.post_tr(),
                    self.place_ml,
                    0,
                    1,
                    self.post_tl(),
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
        shape = self.layout_fx(self.cutout(side=side))
        shape = self.engine.union([shape, self.layout_fx(self.cutout())])

        return shape

    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        shape = self.layout_fx(
            self.engine.rotate(self.single_plate.render(side=side), (0.0, 0.0, -90))
        )
        shape = self.engine.union(
            [shape, self.layout_fx(self.adjustable_plate(self.minidox_key_size))]
        )

        return shape
