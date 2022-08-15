#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.walls import BackWallModel

from dactyl_manuform.types import Shape, Side


class DefaultBackWallModel(BackWallModel):
    def render(self, side: Side = Side.RIGHT, skeleton: bool = False) -> Shape:
        self.log.debug("back_wall()")

        x = 0
        shape = None
        shape = self.engine.union(
            [
                shape,
                self.key_wall_brace(
                    x,
                    0,
                    0,
                    1,
                    self.connectors.post_tl(),
                    x,
                    0,
                    0,
                    1,
                    self.connectors.post_tr(),
                    back=True,
                ),
            ]
        )
        for i in range(self.properties.columns - 1):
            x = i + 1
            shape = self.engine.union(
                [
                    shape,
                    self.key_wall_brace(
                        x,
                        0,
                        0,
                        1,
                        self.connectors.post_tl(),
                        x,
                        0,
                        0,
                        1,
                        self.connectors.post_tr(),
                        back=True,
                    ),
                ]
            )

            skelly = skeleton and not x == 1
            shape = self.engine.union(
                [
                    shape,
                    self.key_wall_brace(
                        x,
                        0,
                        0,
                        1,
                        self.connectors.post_tl(),
                        x - 1,
                        0,
                        0,
                        1,
                        self.connectors.post_tr(),
                        back=True,
                        skeleton=skelly,
                        skel_bottom=True,
                    ),
                ]
            )

        shape = self.engine.union(
            [
                shape,
                self.key_wall_brace(
                    self.properties.lastcol,
                    0,
                    0,
                    1,
                    self.connectors.post_tr(),
                    self.properties.lastcol,
                    0,
                    1,
                    0,
                    self.connectors.post_tr(),
                    back=True,
                    skeleton=skeleton,
                    skel_bottom=True,
                ),
            ]
        )
        if not skeleton:
            shape = self.engine.union(
                [
                    shape,
                    self.key_wall_brace(
                        self.properties.lastcol,
                        0,
                        0,
                        1,
                        self.connectors.post_tr(),
                        self.properties.lastcol,
                        0,
                        1,
                        0,
                        self.connectors.post_tr(),
                    ),
                ]
            )
        return shape
