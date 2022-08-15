#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.interfaces.walls import ThumbClusterWallModel

from dactyl_manuform.types import Shape, Side, TrackballComponents, XY, XYZ


class OrbylThumbClusterWallModel(ThumbClusterWallModel):
    @property
    def has_trackball(self) -> bool:
        return True

    @property
    def trackball_position(self) -> XYZ:
        position = self.thumb_origin

        # Changes size based on key diameter around ball, shifting off of the top left cluster key.
        shift = [
            -0.9 * self.key_diameter / 2 + 27 - 42,
            -0.1 * self.key_diameter / 2 + 3 - 25,
            -5,
        ]

        return (
            position[0] + shift[0] + self.translation_offset[0],
            position[1] + shift[1] + self.translation_offset[1],
            position[2] + shift[2] + self.translation_offset[2],
        )

    @property
    def trackball_rotation(self) -> XYZ:
        rotation = (
            10.0 + self.rotation_offset[0],
            -15.0 + self.rotation_offset[1],
            5.0 + self.rotation_offset[2],
        )

        return rotation

    @property
    def screw_xy_positions_separable(self) -> t.Tuple[XY, ...]:
        return self.config.orbyl_separable_thumb_screw_xy_locations

    @property
    def screw_xy_positions(self) -> t.Tuple[XY, ...]:
        return self.config.orbyl_thumb_screw_xy_locations

    @property
    def ball_diameter(self) -> float:
        return self.config.ball_diameter

    @property
    def ball_wall_thickness(self) -> float:
        return self.config.ball_wall_thickness

    @property
    def ball_gap(self) -> float:
        return self.config.ball_gap

    @property
    def key_height(self):
        return self.config.tbjs_Uheight

    @property
    def key_width(self):
        return self.config.tbjs_Uwidth

    @property
    def key_diameter(self) -> float:
        return self.config.tbjs_key_diameter

    @property
    def key_translation_offsets(self) -> t.Tuple[XYZ, XYZ, XYZ, XYZ]:
        return self.config.tbjs_key_translation_offsets

    @property
    def key_rotation_offsets(self) -> t.Tuple[XYZ, XYZ, XYZ, XYZ]:
        return self.config.tbjs_key_rotation_offsets

    @property
    def rotation_offset(self) -> XYZ:
        return self.config.tbjs_rotation_offset

    @property
    def translation_offset(self) -> XYZ:
        return self.config.tbjs_translation_offset

    @property
    def trackball_post_radius(self) -> float:
        return self.ball_diameter / 2 + self.ball_wall_thickness + self.ball_gap

    @property
    def thumb_position(self) -> XYZ:
        # Changes size based on key diameter around ball, shifting off of the top left cluster key.
        shift = [
            -0.9 * self.key_diameter / 2 + 27 - 42,
            -0.1 * self.key_diameter / 2 + 3 - 25,
            -5,
        ]

        return (
            self.thumb_origin[0] + shift[0] + self.translation_offset[0],
            self.thumb_origin[1] + shift[1] + self.translation_offset[1],
            self.thumb_origin[2] + shift[2] + self.translation_offset[2],
        )

    @property
    def thumb_rotation(self):
        rotation = (
            10 + self.rotation_offset[0],
            -15 + self.rotation_offset[1],
            5 + self.rotation_offset[2],
        )

        return rotation

    def place_tl(self, shape: Shape) -> Shape:
        self.log.debug("thumb_tr_place()")
        # Modifying to make a "ring" of keys
        shape = self.engine.rotate(shape, (0, 0, 0))
        t_off = self.key_translation_offsets[0]
        shape = self.engine.rotate(shape, self.key_rotation_offsets[0])
        shape = self.engine.translate(
            shape, (t_off[0], t_off[1] + self.key_diameter / 2, t_off[2])
        )
        shape = self.engine.rotate(shape, (0, 0, -80))
        shape = self.place(shape)

        return shape

    def place_tr(self, shape: Shape) -> Shape:
        raise RuntimeError("Orbyl trackball thumb cluster doesn't have TR key")

    def place_ml(self, shape: Shape) -> Shape:
        raise RuntimeError("Orbyl trackball thumb cluster doesn't have ML key")

    def place_mr(self, shape: Shape) -> Shape:
        self.log.debug("thumb_mr_place()")
        shape = self.engine.rotate(shape, (0, 0, 0))
        shape = self.engine.rotate(shape, self.key_rotation_offsets[1])
        t_off = self.key_translation_offsets[1]
        shape = self.engine.translate(
            shape, (t_off[0], t_off[1] + self.key_diameter / 2, t_off[2])
        )
        shape = self.engine.rotate(shape, (0, 0, -130))
        shape = self.place(shape)

        return shape

    def place_bl(self, shape: Shape) -> Shape:
        self.log.debug("thumb_bl_place()")
        shape = self.engine.rotate(shape, (0, 0, 180))
        shape = self.engine.rotate(shape, self.key_rotation_offsets[3])
        t_off = self.key_translation_offsets[3]
        shape = self.engine.translate(
            shape, (t_off[0], t_off[1] + self.key_diameter / 2, t_off[2])
        )
        shape = self.engine.rotate(shape, (0, 0, -230))
        shape = self.place(shape)

        return shape

    def place_br(self, shape: Shape) -> Shape:
        self.log.debug("thumb_br_place()")

        shape = self.engine.rotate(shape, (0, 0, 180))
        shape = self.engine.rotate(shape, self.key_rotation_offsets[2])
        t_off = self.key_translation_offsets[2]
        shape = self.engine.translate(
            shape, (t_off[0], t_off[1] + self.key_diameter / 2, t_off[2])
        )
        shape = self.engine.rotate(shape, (0, 0, -180))
        shape = self.place(shape)

        return shape

    def place(self, shape: Shape) -> Shape:
        shape = self.engine.rotate(shape, self.thumb_rotation)
        shape = self.engine.translate(shape, self.thumb_position)

        return shape

    def post_tr(self) -> Shape:
        self.log.debug("thumb_post_tr()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                (self.properties.mount_width / 2)
                + self.properties.adjustable_plate_size(self.key_width)
                - self.post_adj,
                (
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.key_height)
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
                -(self.properties.mount_width / 2)
                - self.properties.adjustable_plate_size(self.key_width)
                + self.post_adj,
                (
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.key_height)
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
                (self.properties.mount_width / 2)
                + self.properties.adjustable_plate_size(self.key_width)
                - self.post_adj,
                -(
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.key_height)
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
                -(self.properties.mount_width / 2)
                - self.properties.adjustable_plate_size(self.key_width)
                + self.post_adj,
                -(
                    (self.properties.mount_height / 2)
                    + self.properties.adjustable_plate_size(self.key_height)
                )
                + self.post_adj,
                0,
            ),
        )

    def trackball_post_r(self) -> Shape:
        self.log.debug("tbjs_post_r()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                1.0 * (self.trackball_post_radius - self.post_adj),
                0.0 * (self.trackball_post_radius - self.post_adj),
                0,
            ),
        )

    def trackball_post_tr(self) -> Shape:
        self.log.debug("tbjs_post_tr()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                0.5 * (self.trackball_post_radius - self.post_adj),
                0.866 * (self.trackball_post_radius - self.post_adj),
                0,
            ),
        )

    def trackball_post_tl(self) -> Shape:
        self.log.debug("tbjs_post_tl()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -0.5 * (self.trackball_post_radius - self.post_adj),
                0.866 * (self.trackball_post_radius - self.post_adj),
                0,
            ),
        )

    def trackball_post_l(self) -> Shape:
        self.log.debug("tbjs_post_l()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -1.0 * (self.trackball_post_radius - self.post_adj),
                0.0 * (self.trackball_post_radius - self.post_adj),
                0,
            ),
        )

    def trackball_post_bl(self) -> Shape:
        self.log.debug("tbjs_post_bl()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                -0.5 * (self.trackball_post_radius - self.post_adj),
                -0.866 * (self.trackball_post_radius - self.post_adj),
                0,
            ),
        )

    def trackball_post_br(self) -> Shape:
        self.log.debug("tbjs_post_br()")
        return self.engine.translate(
            self.web_connectors.post(),
            (
                0.5 * (self.trackball_post_radius - self.post_adj),
                -0.866 * (self.trackball_post_radius - self.post_adj),
                0,
            ),
        )

    def layout_1x(self, shape: Shape, cap: bool = False) -> Shape:
        return self.engine.union(
            [
                self.place_tl(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_tr))
                ),
                self.place_mr(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_mr))
                ),
                self.place_bl(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_bl))
                ),
                self.place_br(
                    self.engine.rotate(shape, (0, 0, self.plate_rotation_br))
                ),
            ]
        )

    def layout_15x(self, shape: Shape, cap: bool = False, plate: bool = True) -> Shape:
        raise RuntimeError("Orbyl Trackball thumb cluster doesn't use layout_15x()")

    def layout_fx(self, shape: Shape) -> Shape:
        return [
            self.place_tl(self.engine.rotate(shape, (0, 0, self.plate_rotation_tr))),
            self.place_mr(self.engine.rotate(shape, (0, 0, self.plate_rotation_mr))),
            self.place_bl(self.engine.rotate(shape, (0, 0, self.plate_rotation_bl))),
            self.place_br(self.engine.rotate(shape, (0, 0, self.plate_rotation_br))),
        ]

    def caps(self) -> Shape:
        return self.layout_1x(self.key_caps.keycap(key_size=1.0))

    def thumb_connectors(self) -> Shape:
        self.log.info("thumb_connectors()")
        hulls = [
            # bottom 2 to tb
            self.engine.triangle_hulls(
                [
                    self.place(self.trackball_post_l()),
                    self.place_bl(self.post_tl()),
                    self.place(self.trackball_post_bl()),
                    self.place_bl(self.post_tr()),
                    self.place_br(self.post_tl()),
                    self.place(self.trackball_post_bl()),
                    self.place_br(self.post_tr()),
                    self.place(self.trackball_post_br()),
                    self.place_br(self.post_tr()),
                    self.place(self.trackball_post_br()),
                    self.place_mr(self.post_br()),
                    self.place(self.trackball_post_r()),
                    self.place_mr(self.post_bl()),
                    self.place_tl(self.post_br()),
                    self.place(self.trackball_post_r()),
                    self.place_tl(self.post_bl()),
                    self.place(self.trackball_post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 0, self.properties.cornerrow
                    ),
                    self.place(self.trackball_post_tl()),
                ]
            ),
            # bottom left
            self.engine.triangle_hulls(
                [
                    self.place_bl(self.post_tr()),
                    self.place_br(self.post_tl()),
                    self.place_bl(self.post_br()),
                    self.place_br(self.post_bl()),
                ]
            ),
            # bottom right
            self.engine.triangle_hulls(
                [
                    self.place_br(self.post_tr()),
                    self.place_mr(self.post_br()),
                    self.place_br(self.post_br()),
                    self.place_mr(self.post_tr()),
                ]
            ),
            # top right
            self.engine.triangle_hulls(
                [
                    self.place_mr(self.post_bl()),
                    self.place_tl(self.post_br()),
                    self.place_mr(self.post_tl()),
                    self.place_tl(self.post_tr()),
                ]
            ),
        ]

        return self.engine.union(hulls)

    def connection(self, side: Side = Side.RIGHT) -> Shape:
        # clunky bit on the top left thumb connection  (normal connectors don't work well)
        hulls = [
            self.engine.triangle_hulls(
                [
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 0, self.properties.cornerrow
                    ),
                    self.placement.left_key_place(
                        self.web_connectors.post(),
                        self.properties.cornerrow,
                        -1,
                        side=side,
                        low_corner=True,
                    ),
                    self.place(self.trackball_post_tl()),
                ]
            ),
            self.engine.triangle_hulls(
                [
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 0, self.properties.cornerrow
                    ),
                    self.place_tl(self.post_bl()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 0, self.properties.cornerrow
                    ),
                    self.place_tl(self.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 1, self.properties.cornerrow
                    ),
                    self.place_tl(self.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 1, self.properties.cornerrow
                    ),
                    self.place_tl(self.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 2, self.properties.lastrow
                    ),
                    self.place_tl(self.post_tr()),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 2, self.properties.lastrow
                    ),
                    self.place_mr(self.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 2, self.properties.lastrow
                    ),
                    self.placement.key_place(
                        self.web_connectors.post_bl(), 3, self.properties.lastrow
                    ),
                    self.place_mr(self.post_tr()),
                    self.place_mr(self.post_tl()),
                    self.placement.key_place(
                        self.web_connectors.post_br(), 2, self.properties.lastrow
                    ),
                ]
            ),
        ]

        shape = self.engine.union(hulls)
        return shape

    def walls(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.log.info("thumb_walls()")
        # thumb, walls
        shape = self.wall_brace(
            self.place_mr,
            0.5,
            1,
            self.post_tr(),
            (lambda sh: self.placement.key_place(sh, 3, self.properties.lastrow)),
            0,
            -1,
            self.web_connectors.post_bl(),
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_mr,
                    0.5,
                    1,
                    self.post_tr(),
                    self.place_br,
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
                    self.place_br,
                    0,
                    -1,
                    self.post_br(),
                    self.place_br,
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
                    self.place_br,
                    0,
                    -1,
                    self.post_bl(),
                    self.place_bl,
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
                    self.place_bl,
                    0,
                    -1,
                    self.post_br(),
                    self.place_bl,
                    -1,
                    -1,
                    self.post_bl(),
                ),
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place,
                    -1.5,
                    0,
                    self.trackball_post_tl(),
                    (
                        lambda sh: self.placement.left_key_place(
                            sh,
                            self.properties.cornerrow,
                            -1,
                            side=self.properties.trackball_side,
                            low_corner=True,
                        )
                    ),
                    -1,
                    0,
                    self.web_connectors.post(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place,
                    -1.5,
                    0,
                    self.trackball_post_tl(),
                    self.place,
                    -1,
                    0,
                    self.trackball_post_l(),
                ),
            ]
        )
        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place,
                    -1,
                    0,
                    self.trackball_post_l(),
                    self.place_bl,
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
                    self.place_bl,
                    -1,
                    0,
                    self.post_tl(),
                    self.place_bl,
                    -1,
                    -1,
                    self.post_bl(),
                ),
            ]
        )

        return shape

    def pcb_plate_cutouts(self, side: Side = Side.RIGHT) -> t.List[Shape]:
        return self.layout_1x(self.cutout(side=side))

    def trackball_components(self) -> TrackballComponents:
        return self.components.generate(
            position=self.trackball_position, rotation=self.trackball_rotation
        )

    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        shape = self.layout_1x(self.single_plate.render(side=side))
        shape = self.engine.union(
            [
                shape,
                *self.layout_fx(
                    self.adjustable_square_plate(
                        key_width=self.key_width, key_height=self.key_height
                    )
                ),
            ]
        )
        return shape
