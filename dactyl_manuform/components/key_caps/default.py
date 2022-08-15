#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.key_caps import KeycapModel

from dactyl_manuform.types import Shape


class DefaultKeyCapModel(KeycapModel):
    def keycap(self, key_size: float = 1) -> Shape:
        bl2 = 18.5 / 2
        bw2 = 18.5 / 2
        m = 17 / 2
        pl2 = 6
        pw2 = 6

        if key_size == 1.5:
            bl2 = self.config.sa_length / 2
            bw2 = 27.94 / 2
            m = 0
            pl2 = 6
            pw2 = 11

        if key_size == 2:
            bl2 = self.config.sa_length
            bw2 = self.config.sa_length / 2
            m = 0
            pl2 = 16
            pw2 = 6

        k1 = self.engine.polyline(
            [(bw2, bl2), (bw2, -bl2), (-bw2, -bl2), (-bw2, bl2), (bw2, bl2)]
        )
        k1 = self.engine.extrude_poly(outer_poly=k1, height=0.1)
        k1 = self.engine.translate(k1, (0, 0, 0.05))
        k2 = self.engine.polyline(
            [(pw2, pl2), (pw2, -pl2), (-pw2, -pl2), (-pw2, pl2), (pw2, pl2)]
        )
        k2 = self.engine.extrude_poly(outer_poly=k2, height=0.1)
        k2 = self.engine.translate(k2, (0, 0, 12.0))
        if m > 0:
            m1 = self.engine.polyline([(m, m), (m, -m), (-m, -m), (-m, m), (m, m)])
            m1 = self.engine.extrude_poly(outer_poly=m1, height=0.1)
            m1 = self.engine.translate(m1, (0, 0, 6.0))
            key_cap = self.engine.hull_from_shapes((k1, k2, m1))
        else:
            key_cap = self.engine.hull_from_shapes((k1, k2))

        key_cap = self.engine.translate(
            key_cap, (0, 0, 5 + self.properties.plate_thickness)
        )

        if self.config.show_pcbs:
            key_cap = self.engine.add([key_cap, self.pcb])

        return key_cap
