#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.single_plate import SinglePlateComponent

from dactyl_manuform.types import RenderEngine, Shape, Side


class NotchSinglePlate(SinglePlateComponent):
    @property
    def keyswitch_width(self) -> float:
        return self.config.undercut_keyswitch_width

    @property
    def keyswitch_height(self) -> float:
        return self.config.undercut_keyswitch_height

    @property
    def notch_width(self) -> float:
        return self.config.notch_width

    def render_undercut(self, plate: Shape, side: Side) -> Shape:
        undercut = self.engine.box(
            self.notch_width,
            self.keyswitch_height + 2 * self.clip_undercut,
            self.mount_thickness,
        )
        undercut = self.engine.union(
            [
                undercut,
                self.engine.box(
                    self.keyswitch_width + 2 * self.clip_undercut,
                    self.notch_width,
                    self.mount_thickness,
                ),
            ]
        )

        undercut = self.engine.translate(
            undercut, (0.0, 0.0, -self.clip_thickness + self.mount_thickness / 2.0)
        )

        if self.engine.kind is RenderEngine.CADQUERY and self.undercut_transition > 0:
            undercut = undercut.faces("+Z").chamfer(
                self.undercut_transition, self.clip_undercut
            )

        return self.engine.difference(plate, [undercut])
