#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.walls import FrontWallModel

from dactyl_manuform.types import Shape, Side


class DefaultFrontWallModel(FrontWallModel):
    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.log.debug("front_wall()")
        shape = None

        corner = self.properties.cornerrow
        offset_col = 99

        if self.properties.reduced_outer_columns > 0:
            offset_col = self.properties.columns - self.properties.reduced_outer_columns

        for i in range(self.properties.columns - 3):
            x = i + 3
            self.log.debug(f"col {x}")
            if x < (offset_col - 1):
                self.log.debug("pre-offset")
                if x > 3:
                    shape = self.engine.union(
                        [
                            shape,
                            self.key_wall_brace(
                                x - 1,
                                self.properties.lastrow,
                                0,
                                -1,
                                self.connectors.post_br(),
                                x,
                                self.properties.lastrow,
                                0,
                                -1,
                                self.connectors.post_bl(),
                            ),
                        ]
                    )
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.lastrow,
                            0,
                            -1,
                            self.connectors.post_bl(),
                            x,
                            self.properties.lastrow,
                            0,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )
            elif x < offset_col:
                self.log.debug("offset setup")
                if x > 3:
                    shape = self.engine.union(
                        [
                            shape,
                            self.key_wall_brace(
                                x - 1,
                                self.properties.lastrow,
                                0,
                                -1,
                                self.connectors.post_br(),
                                x,
                                self.properties.lastrow,
                                0,
                                -1,
                                self.connectors.post_bl(),
                            ),
                        ]
                    )
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.lastrow,
                            0,
                            -1,
                            self.connectors.post_bl(),
                            x,
                            self.properties.lastrow,
                            0.5,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )

            elif x == offset_col:
                self.log.debug("offset")
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x - 1,
                            self.properties.lastrow,
                            0.5,
                            -1,
                            self.connectors.post_br(),
                            x,
                            self.properties.cornerrow,
                            0.5,
                            -1,
                            self.connectors.post_bl(),
                        ),
                    ]
                )
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.cornerrow,
                            0.5,
                            -1,
                            self.connectors.post_bl(),
                            x,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )

            elif x == (offset_col + 1):
                self.log.debug("offset completion")
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_bl(),
                            x - 1,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_bl(),
                            x,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )

            else:
                self.log.debug("post offset")
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_bl(),
                            x - 1,
                            corner,
                            0,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )
                shape = self.engine.union(
                    [
                        shape,
                        self.key_wall_brace(
                            x,
                            self.properties.cornerrow,
                            0,
                            -1,
                            self.connectors.post_bl(),
                            x,
                            corner,
                            0,
                            -1,
                            self.connectors.post_br(),
                        ),
                    ]
                )

        return shape
