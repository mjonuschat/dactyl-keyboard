#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.walls import ScrewInsertModel

from dactyl_manuform.types import ShiftValues


class DefaultScrewInsertModel(ScrewInsertModel):
    def shift(self, column: int, row: int) -> ShiftValues:
        right = column == self.properties.lastcol
        left = column == 0
        up = (not (right or left)) and (row == 0)
        down = (not (right or left)) and (row >= self.properties.lastrow)

        return ShiftValues(
            up=up,
            down=down,
            left=left,
            right=right,
            left_adjust=0.0,
            right_adjust=0.0,
            down_adjust=0.0,
            up_adjust=0.0,
        )
