#!/usr/bin/env python3
from __future__ import annotations

import typing as t

import numpy as np
from dactyl_manuform.interfaces.walls import ThumbClusterWallModel

from dactyl_manuform.types import Shape, Side, TrackballComponents, XY, XYZ


class CJThumbClusterWallModel(ThumbClusterWallModel):
    @property
    def has_trackball(self) -> bool:
        return True

    @property
    def trackball_position(self) -> XYZ:
        return np.array([-15, -60, -12]) + self.thumb_origin

    @property
    def trackball_rotation(self) -> XYZ:
        return 0.0, 0.0, 0.0

    @property
    def screw_xy_positions_separable(self) -> t.Tuple[XY, ...]:
        return self.config.tbcj_separable_thumb_screw_xy_locations

    @property
    def screw_xy_positions(self) -> t.Tuple[XY, ...]:
        return self.config.tbcj_thumb_screw_xy_locations

    @property
    def trackball_outer_diameter(self) -> float:
        return self.config.tbcj_outer_diameter

    @property
    def trackball_inner_diameter(self) -> float:
        return self.config.tbcj_inner_diameter

    @property
    def trackball_holder(self) -> Shape:
        center = self.engine.box(
            self.post_size, self.post_size, self.trackball_thickness
        )

        shape = []
        for i in range(8):
            shape_ = self.engine.hull_from_shapes(
                [
                    center,
                    self.trackball_edge_post(i),
                    self.trackball_edge_post(i + 1),
                ]
            )
            shape.append(shape_)

        shape = self.engine.union(shape)

        shape = self.engine.difference(
            shape,
            [
                self.engine.cylinder(
                    self.trackball_inner_diameter / 2, self.trackball_thickness + 0.1
                )
            ],
        )

        return shape

    def trackball_edge_post(self, i) -> Shape:
        shape = self.engine.box(
            self.post_size, self.post_size, self.trackball_thickness
        )
        shape = self.oct_corner(i, self.trackball_outer_diameter, shape)
        return shape

    def trackball_web_post(self, i: int):
        shape = self.engine.box(
            self.post_size, self.post_size, self.trackball_thickness
        )
        shape = self.oct_corner(i, self.trackball_outer_diameter, shape)
        return shape

    def oct_corner(self, i, diameter, shape) -> Shape:
        radius = diameter / 2
        i = (i + 1) % 8

        r = radius
        m = radius * np.tan(np.pi / 8)

        points_x = [m, r, r, m, -m, -r, -r, -m]
        points_y = [r, m, -m, -r, -r, -m, m, r]

        return self.engine.translate(shape, (points_x[i], points_y[i], 0))

    @property
    def trackball_thickness(self) -> float:
        return self.config.tbcj_thickness

    @property
    def post_size(self) -> float:
        return self.config.post_size

    def post_tl(self) -> Shape:
        raise RuntimeError("CJ Trackball thumb cluster doesn't use post_tl()")

    def post_tr(self) -> Shape:
        raise RuntimeError("CJ Trackball thumb cluster doesn't use post_tr()")

    def post_bl(self) -> Shape:
        raise RuntimeError("CJ Trackball thumb cluster doesn't use post_bl()")

    def post_br(self) -> Shape:
        raise RuntimeError("CJ Trackball thumb cluster doesn't use post_br()")

    def place_tl(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (7.5, -18, 10))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-32.5, -14.5, -2.5))
        return shape

    def place_tr(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (10, -15, 10))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-12, -16, 3))
        return shape

    def place_ml(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (6, -34, 40))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-51, -25, -12))
        return shape

    def place_mr(self, shape: Shape) -> Shape:
        raise RuntimeError("CJ trackball thumb cluster doesn't have MR key")

    def place_bl(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, (-4, -35, 52))
        shape = self.engine.translate(shape, self.thumb_origin)
        shape = self.engine.translate(shape, (-56.3, -43.3, -23.5))
        return shape

    def place_br(self, shape: Shape) -> Shape:
        raise RuntimeError("CJ trackball thumb cluster doesn't have BR key")

    def place(self, shape: Shape) -> Shape:
        location = np.array([-15, -60, -12]) + self.thumb_origin
        shape = self.engine.translate(shape, location)
        shape = self.engine.rotate(shape, (0, 0, 0))
        return shape

    def layout_1x(self, shape: Shape, cap: bool = False) -> Shape:
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
                self.place_bl(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_bl))
                ),
            ]
        )

    def layout_15x(self, shape: Shape, cap: bool = False, plate: bool = True) -> Shape:
        raise RuntimeError("CJ Trackball thumb cluster doesn't use layout_15x()")

    def caps(self) -> Shape:
        return self.layout_1x(self.key_caps.keycap(key_size=1.0))

    def thumb_connectors(self) -> Shape:
        hulls = [
            # Top two
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.web_connectors.post_tr()),
                    self.place_tl(self.web_connectors.post_br()),
                    self.place_tr(self.web_connectors.post_tl()),
                    self.place_tr(self.web_connectors.post_bl()),
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
            self.engine.triangle_hulls(
                [
                    self.place_tl(self.web_connectors.post_tl()),
                    self.place_ml(self.web_connectors.post_tr()),
                    self.place_tl(self.web_connectors.post_bl()),
                    self.place_ml(self.web_connectors.post_br()),
                    self.place_tl(self.web_connectors.post_br()),
                    self.place_tr(self.web_connectors.post_bl()),
                    self.place_tr(self.web_connectors.post_br()),
                ]
            ),
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
                    self.place_tr(self.web_connectors.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 1, self.properties.cornerrow
                    ),
                    self.place_tr(self.web_connectors.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 1, self.properties.cornerrow
                    ),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 2, self.properties.lastrow
                    ),
                    self.place_tr(self.web_connectors.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 2, self.properties.lastrow
                    ),
                    self.place_tr(self.web_connectors.post_br()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 2, self.properties.lastrow
                    ),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 3, self.properties.lastrow
                    ),
                ]
            ),
            self.engine.triangle_hulls(
                [
                    self.place(self.trackball_web_post(4)),
                    self.place_bl(self.web_connectors.post_bl()),
                    self.place(self.trackball_web_post(5)),
                    self.place_bl(self.web_connectors.post_br()),
                    self.place(self.trackball_web_post(6)),
                ]
            ),
            self.engine.triangle_hulls(
                [
                    self.place_bl(self.web_connectors.post_br()),
                    self.place(self.trackball_web_post(6)),
                    self.place_ml(self.web_connectors.post_bl()),
                ]
            ),
            self.engine.triangle_hulls(
                [
                    self.place_ml(self.web_connectors.post_bl()),
                    self.place(self.trackball_web_post(6)),
                    self.place_ml(self.web_connectors.post_br()),
                    self.place_tr(self.web_connectors.post_bl()),
                ]
            ),
            self.engine.triangle_hulls(
                [
                    self.place(self.trackball_web_post(6)),
                    self.place_tr(self.web_connectors.post_bl()),
                    self.place(self.trackball_web_post(7)),
                    self.place_tr(self.web_connectors.post_br()),
                    self.place(self.trackball_web_post(0)),
                    self.place_tr(self.web_connectors.post_br()),
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
                        self.place_tl(self.web_connectors.post_tl()),
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
                        self.place_tl(self.web_connectors.post_tl()),
                    ]
                ),
            ]
        )

        return shape

    def walls(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.side = side
        shape = self.engine.union(
            [
                self.wall_brace(
                    self.place_ml,
                    -0.3,
                    1,
                    self.web_connectors.post_tr(),
                    self.place_ml,
                    0,
                    1,
                    self.web_connectors.post_tl(),
                )
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

        points = [
            (self.place_bl, -1, 0, self.web_connectors.post_bl()),
            (self.place, 0, -1, self.trackball_web_post(4)),
            (self.place, 0, -1, self.trackball_web_post(3)),
            (self.place, 0, -1, self.trackball_web_post(2)),
            (self.place, 1, -1, self.trackball_web_post(1)),
            (self.place, 1, 0, self.trackball_web_post(0)),
            (
                (lambda sh: self.placement.key_place(sh, 3, self.properties.lastrow)),
                0,
                -1,
                self.web_connectors.post_bl(),
            ),
        ]
        for i, _ in enumerate(points[:-1]):
            (pa, dxa, dya, sa) = points[i]
            (pb, dxb, dyb, sb) = points[i + 1]

            shape = self.engine.union(
                [shape, self.wall_brace(pa, dxa, dya, sa, pb, dxb, dyb, sb)]
            )

        return shape

    def pcb_plate_cutouts(self, side: Side = Side.RIGHT) -> t.List[Shape]:
        return self.layout_1x(self.cutout(side=side))

    def trackball_components(self) -> TrackballComponents:
        return self.components.generate(
            position=self.trackball_position, rotation=self.trackball_rotation
        )

    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        t = self.layout_1x(self.single_plate.render(side=side))
        tb = self.place(self.trackball_holder)

        return self.engine.union([t, tb])
