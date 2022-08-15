#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.walls import RightWallModel

from dactyl_manuform.types import Shape, Side


class DefaultRightWallModel(RightWallModel):
    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.log.debug("right_wall()")
        y = 0

        shape = None

        corner = self.properties.lastrow
        if self.properties.reduced_outer_columns > 0:
            corner = self.properties.cornerrow

        shape = self.engine.union(
            [
                shape,
                self.key_wall_brace(
                    self.properties.lastcol,
                    y,
                    1,
                    0,
                    self.connectors.post_tr(),
                    self.properties.lastcol,
                    y,
                    1,
                    0,
                    self.connectors.post_br(),
                    skeleton=skeleton,
                ),
            ]
        )

        for i in range(corner):
            y = i + 1
            shape = self.engine.union(
                [
                    shape,
                    self.key_wall_brace(
                        self.properties.lastcol,
                        y - 1,
                        1,
                        0,
                        self.connectors.post_br(),
                        self.properties.lastcol,
                        y,
                        1,
                        0,
                        self.connectors.post_tr(),
                        skeleton=skeleton,
                    ),
                ]
            )

            shape = self.engine.union(
                [
                    shape,
                    self.key_wall_brace(
                        self.properties.lastcol,
                        y,
                        1,
                        0,
                        self.connectors.post_tr(),
                        self.properties.lastcol,
                        y,
                        1,
                        0,
                        self.connectors.post_br(),
                        skeleton=skeleton,
                    ),
                ]
            )
            # STRANGE PARTIAL OFFSET

        shape = self.engine.union(
            [
                shape,
                self.key_wall_brace(
                    self.properties.lastcol,
                    corner,
                    0,
                    -1,
                    self.connectors.post_br(),
                    self.properties.lastcol,
                    corner,
                    1,
                    0,
                    self.connectors.post_br(),
                    skeleton=skeleton,
                ),
            ]
        )

        return shape
