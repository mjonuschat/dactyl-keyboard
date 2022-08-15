#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.walls import LeftWallModel

from dactyl_manuform.types import Shape, Side


class DefaultLeftWallModel(LeftWallModel):
    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.log.debug("left_wall()")

        shape = self.engine.union(
            [
                self.wall_brace(
                    (lambda sh: self.placement.key_place(sh, 0, 0)),
                    0,
                    1,
                    self.connectors.post_tl(),
                    (lambda sh: self.placement.left_key_place(sh, 0, 1, side=side)),
                    0,
                    1,
                    self.connectors.post(),
                )
            ]
        )

        shape = self.engine.union(
            [
                shape,
                self.wall_brace(
                    (lambda sh: self.placement.left_key_place(sh, 0, 1, side=side)),
                    0,
                    1,
                    self.connectors.post(),
                    (lambda sh: self.placement.left_key_place(sh, 0, 1, side=side)),
                    -1,
                    0,
                    self.connectors.post(),
                    skeleton=skeleton,
                ),
            ]
        )

        corner = self.properties.lastrow
        if self.properties.reduced_inner_columns > 0:
            corner = self.properties.cornerrow

        for i in range(corner + 1):
            y = i
            low = y == corner
            temp_shape1 = self.wall_brace(
                (lambda sh: self.placement.left_key_place(sh, y, 1, side=side)),
                -1,
                0,
                self.connectors.post(),
                (
                    lambda sh: self.placement.left_key_place(
                        sh, y, -1, low_corner=low, side=side
                    )
                ),
                -1,
                0,
                self.connectors.post(),
                skeleton=skeleton and (y < corner),
            )
            shape = self.engine.union([shape, temp_shape1])

            temp_shape2 = self.engine.hull_from_shapes(
                (
                    self.placement.key_place(self.connectors.post_tl(), 0, y),
                    self.placement.key_place(self.connectors.post_bl(), 0, y),
                    self.placement.left_key_place(
                        self.connectors.post(), y, 1, side=side
                    ),
                    self.placement.left_key_place(
                        self.connectors.post(), y, -1, low_corner=low, side=side
                    ),
                )
            )

            shape = self.engine.union([shape, temp_shape2])

        for i in range(corner):
            y = i + 1
            low = y == corner
            temp_shape1 = self.wall_brace(
                (lambda sh: self.placement.left_key_place(sh, y - 1, -1, side=side)),
                -1,
                0,
                self.connectors.post(),
                (lambda sh: self.placement.left_key_place(sh, y, 1, side=side)),
                -1,
                0,
                self.connectors.post(),
                skeleton=skeleton and (y < corner),
            )
            shape = self.engine.union([shape, temp_shape1])

            temp_shape2 = self.engine.hull_from_shapes(
                (
                    self.placement.key_place(self.connectors.post_tl(), 0, y),
                    self.placement.key_place(self.connectors.post_bl(), 0, y - 1),
                    self.placement.left_key_place(
                        self.connectors.post(), y, 1, side=side
                    ),
                    self.placement.left_key_place(
                        self.connectors.post(), y - 1, -1, side=side
                    ),
                )
            )

            shape = self.engine.union([shape, temp_shape2])

        return shape
