#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.key_caps import KeycapModel

from dactyl_manuform.types import Shape


class ChocKeyCapModel(KeycapModel):
    def keycap(self, key_size: float = 1) -> Shape:
        bl2 = 18.0 / 2
        bw2 = 17.5 / 2
        bt = 2
        pl2 = 15.0 / 2
        pw2 = 14.5 / 2
        pt = 1.5
        gap = 1.5

        k1 = self.engine.polyline(
            [(bw2, bl2), (bw2, -bl2), (-bw2, -bl2), (-bw2, bl2), (bw2, bl2)]
        )
        k1 = self.engine.extrude_poly(outer_poly=k1, height=0.1)
        k1 = self.engine.translate(k1, (0, 0, 0.05))
        k2 = self.engine.polyline(
            [(bw2, bl2), (bw2, -bl2), (-bw2, -bl2), (-bw2, bl2), (bw2, bl2)]
        )
        k2 = self.engine.extrude_poly(outer_poly=k2, height=0.1)
        k2 = self.engine.translate(k2, (0, 0, 0.05 + bt))
        k3 = self.engine.polyline(
            [(pw2, pl2), (pw2, -pl2), (-pw2, -pl2), (-pw2, pl2), (pw2, pl2)]
        )
        k3 = self.engine.extrude_poly(outer_poly=k3, height=0.1)
        k3 = self.engine.translate(k3, (0, 0, 0.05 + bt + pt))
        key_cap = self.engine.hull_from_shapes((k1, k2, k3))

        key_cap = self.engine.translate(
            key_cap, (0, 0, 2.8 + self.properties.plate_thickness)
        )

        if self.config.show_pcbs:
            key_cap = self.engine.add([key_cap, self.pcb])

        return key_cap
