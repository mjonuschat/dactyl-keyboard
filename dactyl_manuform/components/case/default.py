#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.case import CaseModel

from dactyl_manuform.types import Shape, Side


class DefaultCaseModel(CaseModel):
    def render(self, side: Side = Side.RIGHT) -> Shape:
        self.log.info("case_walls()")
        return self.engine.union(
            [
                self.back_wall.render(side=side, skeleton=self.skeleton),
                self.left_wall.render(side=side, skeleton=self.skeleton),
                self.right_wall.render(side=side, skeleton=self.skeleton),
                self.front_wall.render(side=side, skeleton=self.skeleton),
                # thumb_walls(side=side),
                # thumb_connection(side=side),
            ]
        )
