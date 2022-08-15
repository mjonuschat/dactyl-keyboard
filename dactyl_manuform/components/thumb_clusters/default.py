#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.interfaces.walls import ThumbClusterWallModel

from dactyl_manuform.types import Shape, Side, XY


class DefaultThumbClusterWallModel(ThumbClusterWallModel):
    @property
    def screw_xy_positions_separable(self) -> t.Tuple[XY, ...]:
        return self.config.default_separable_thumb_screw_xy_locations

    @property
    def screw_xy_positions(self) -> t.Tuple[XY, ...]:
        return self.config.default_thumb_screw_xy_locations

    @property
    def double_plate_height(self) -> float:
        height = 0.95 * self.config.sa_double_length

        return (height - self.properties.mount_height) / 3

    def place_tl(self, shape: Shape) -> Shape:
        self.log.debug("thumb_tl_place()")
        shape = self.engine.rotate(shape, (7.5, -18, 10))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-32.5, -14.5, -2.5))
        return shape

    def place_tr(self, shape: Shape) -> Shape:
        self.log.debug("thumb_tr_place()")
        shape = self.engine.rotate(shape, (10, -15, 10))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-12, -16, 3))
        return shape

    def place_ml(self, shape: Shape) -> Shape:
        self.log.debug("thumb_ml_place()")
        shape = self.engine.rotate(shape, (6, -34, 40))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-51, -25, -12))
        return shape

    def place_mr(self, shape: Shape) -> Shape:
        self.log.debug("thumb_mr_place()")
        shape = self.engine.rotate(shape, (-6, -34, 48))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-29, -40, -13))
        return shape

    def place_bl(self, shape: Shape) -> Shape:
        self.log.debug("thumb_bl_place()")
        shape = self.engine.rotate(shape, (-4, -35, 52))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-56.3, -43.3, -23.5))
        return shape

    def place_br(self, shape: Shape) -> Shape:
        self.log.debug("thumb_br_place()")
        shape = self.engine.rotate(shape, (-16, -33, 54))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-37.8, -55.3, -25.3))
        return shape

    def post_tr(self) -> Shape:
        self.log.debug("thumb_post_tr()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                (self.properties.mount_width / 2) - self.post_adj,
                ((self.properties.mount_height / 2) + self.double_plate_height)
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
                ((self.properties.mount_height / 2) + self.double_plate_height)
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
                -((self.properties.mount_height / 2) + self.double_plate_height)
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
                -((self.properties.mount_height / 2) + self.double_plate_height)
                + self.post_adj,
                0,
            ),
        )

    def layout_1x_shapes(self, shape: Shape) -> t.List[Shape]:
        return [
            self.place_mr(self.engine.rotate(shape, (0, 0, self.plate_rotation_mr))),
            self.place_ml(self.engine.rotate(shape, (0, 0, self.plate_rotation_ml))),
            self.place_br(self.engine.rotate(shape, (0, 0, self.plate_rotation_br))),
            self.place_bl(self.engine.rotate(shape, (0, 0, self.plate_rotation_bl))),
        ]

    def layout_1x(self, shape: Shape, cap: bool = False) -> Shape:
        self.log.debug("thumb_1x_layout()")

        shape_list = self.layout_1x_shapes(shape)

        if cap:
            return self.engine.add(shape_list)

        return self.engine.union(shape_list)

    def layout_15x_with_plate_and_cap(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (0, 0, 90))
        cap_list = [
            self.place_tl(self.engine.rotate(shape, (0, 0, self.plate_rotation_tl))),
            self.place_tr(self.engine.rotate(shape, (0, 0, self.plate_rotation_tr))),
        ]
        return self.engine.add(cap_list)

    def layout_15x(self, shape: Shape, cap: bool = False, plate: bool = True) -> Shape:
        self.log.debug("thumb_15x_layout()")
        if plate and cap:
            return self.layout_15x_with_plate_and_cap(shape=shape)

        if plate:
            return self.engine.add(
                [
                    self.place_tl(
                        self.engine.rotate(shape, (0, 0, self.plate_rotation_tl))
                    ),
                    self.place_tr(
                        self.engine.rotate(shape, (0, 0, self.plate_rotation_tr))
                    ),
                ]
            )

        if cap:
            shape = self.engine.rotate(shape, (0, 0, 90))
            return self.engine.add([self.place_tl(shape), self.place_tr(shape)])

        return self.engine.union([self.place_tl(shape), self.place_tr(shape)])

    def wall_start(self) -> Shape:
        return self.engine.union(
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

    def wall_end(self, shape: Shape) -> Shape:
        return self.engine.union(
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

    def walls_base(self, shape: Shape) -> Shape:
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
                    self.place_ml,
                    -0.3,
                    1,
                    self.web_connectors.post_tr(),
                    self.place_ml,
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

        return shape

    def corners(self, shape: Shape) -> Shape:
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

        return shape

    def tweeners(self, shape: Shape) -> Shape:
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
                    self.place_ml,
                    0,
                    1,
                    self.web_connectors.post_tl(),
                    self.place_bl,
                    0,
                    1,
                    self.web_connectors.post_tr(),
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

        return shape

    def caps(self) -> Shape:
        t1 = self.layout_1x(self.key_caps.keycap(key_size=1.0), cap=True)
        t1.add(self.layout_15x(self.key_caps.keycap(key_size=1.5), cap=True))
        return t1

    def connector_hulls(self) -> t.List[Shape]:
        self.log.info("thumb_connectors()")
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
                    self.place_br(self.web_connectors.post_tr()),
                    self.place_br(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tl()),
                    self.place_mr(self.web_connectors.post_bl()),
                ]
            ),
            # bottom two on the left
            self.engine.triangle_hulls(
                [
                    self.place_br(self.web_connectors.post_tr()),
                    self.place_br(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tl()),
                    self.place_mr(self.web_connectors.post_bl()),
                ]
            ),
            # centers of the bottom four
            self.engine.triangle_hulls(
                [
                    self.place_bl(self.web_connectors.post_tr()),
                    self.place_bl(self.web_connectors.post_br()),
                    self.place_ml(self.web_connectors.post_tl()),
                    self.place_ml(self.web_connectors.post_bl()),
                ]
            ),
            # top two to the middle two, starting on the left
            self.engine.triangle_hulls(
                [
                    self.place_br(self.web_connectors.post_tl()),
                    self.place_bl(self.web_connectors.post_bl()),
                    self.place_br(self.web_connectors.post_tr()),
                    self.place_bl(self.web_connectors.post_br()),
                    self.place_mr(self.web_connectors.post_tl()),
                    self.place_ml(self.web_connectors.post_bl()),
                    self.place_mr(self.web_connectors.post_tr()),
                    self.place_ml(self.web_connectors.post_br()),
                ]
            ),
            # top two to the main keyboard, starting on the left
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.post_tl()),
                    self.place_ml(self.web_connectors.post_tr()),
                    self.place_tl(self.post_bl()),
                    self.place_ml(self.web_connectors.post_br()),
                    self.place_tl(self.post_br()),
                    self.place_mr(self.web_connectors.post_tr()),
                    self.place_tr(self.post_bl()),
                    self.place_mr(self.web_connectors.post_br()),
                    self.place_tr(self.post_br()),
                ]
            ),
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
                        self.web_connectors.post_tl(), 2, self.properties.lastrow
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

        return hulls

    def thumb_connectors(self) -> Shape:
        hulls = self.connector_hulls()

        return self.engine.union(hulls)

    def connection(self, side: Side = Side.RIGHT) -> Shape:
        self.log.info("thumb_connection()")
        shape = None
        shape = self.engine.union(
            [
                shape,
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
                                self.web_connectors.post_tr(),
                                self.wall_locate2(-0.3, 1),
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate3(-0.3, 1),
                            )
                        ),
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
                                self.web_connectors.post_tr(),
                                self.wall_locate2(-0.3, 1),
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate3(-0.3, 1),
                            )
                        ),
                        self.place_tl(self.post_tl()),
                    ]
                ),
            ]
        )  # )

        shape = self.engine.union(
            [
                shape,
                self.engine.hull_from_shapes(
                    [
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
                        self.place_ml(self.web_connectors.post_tr()),
                        self.place_ml(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate1(-0.3, 1),
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate2(-0.3, 1),
                            )
                        ),
                        self.place_ml(
                            self.engine.translate(
                                self.web_connectors.post_tr(),
                                self.wall_locate3(-0.3, 1),
                            )
                        ),
                        self.place_tl(self.post_tl()),
                    ]
                ),
            ]
        )

        return shape

    def walls(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        shape = self.wall_start()
        shape = self.walls_base(shape=shape)
        shape = self.corners(shape=shape)
        shape = self.tweeners(shape=shape)
        shape = self.wall_end(shape=shape)

        return shape

    def pcb_plate_cutouts(self, side: Side = Side.RIGHT) -> t.List[Shape]:
        shape = self.layout_1x(self.cutout(side=side))
        shape = self.engine.union([shape, self.layout_15x(self.cutout(side=side))])
        return shape

    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.log.info("thumb()")

        shape = self.layout_1x(
            self.engine.rotate(self.single_plate.render(side=side), (0, 0, -90))
        )
        shape = self.engine.union(
            [
                shape,
                self.layout_15x(
                    self.engine.rotate(self.single_plate.render(side=side), (0, 0, -90))
                ),
            ]
        )
        shape = self.engine.union(
            [shape, self.layout_15x(self.double_plate, plate=False)]
        )

        return shape
