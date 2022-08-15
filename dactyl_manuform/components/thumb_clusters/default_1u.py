#!/usr/bin/env python3
from __future__ import annotations

import typing as t

from dactyl_manuform.components.thumb_clusters.default import (
    DefaultThumbClusterWallModel,
)

from dactyl_manuform.types import Shape


class Default1UThumbClusterWallModel(DefaultThumbClusterWallModel):
    @property
    def double_plate_height(self) -> float:
        height = 0.7 * self.config.sa_double_length

        return (height - self.properties.mount_height) / 3

    def layout_1x(self, shape: Shape, cap: bool = False) -> Shape:
        self.log.debug("thumb_1x_layout()")

        shape_list = self.layout_1x_shapes(shape)

        if cap:
            shape_list += [
                self.place_tr(
                    self.engine.rotate(
                        self.engine.rotate(shape, (0, 0, 90)),
                        (0, 0, self.plate_rotation_tr),
                    )
                ),
                self.place_tl(
                    self.engine.rotate(
                        self.engine.rotate(shape, (0, 0, 90)),
                        (0, 0, self.plate_rotation_tl),
                    )
                ),
            ]
            return self.engine.add(shape_list)

        shape_list.append(
            self.place_tr(
                self.engine.rotate(
                    self.engine.rotate(shape, (0, 0, 90)),
                    (0, 0, self.plate_rotation_tr),
                )
            )
        )
        return self.engine.union(shape_list)

    def layout_15x(self, shape: Shape, cap: bool = False, plate: bool = True) -> Shape:
        self.log.debug("thumb_15x_layout()")
        if plate and cap:
            return self.layout_15x_with_plate_and_cap(shape=shape)

        if plate:
            return self.engine.union(
                [
                    self.place_tl(
                        self.engine.rotate(shape, (0, 0, self.plate_rotation_tl))
                    ),
                ]
            )

        if cap:
            shape = self.engine.rotate(shape, (0, 0, 90))
            return self.engine.add([self.place_tl(shape), self.place_tr(shape)])

        return self.engine.union([self.place_tl(shape)])

    def wall_start(self) -> Shape:
        return self.engine.union(
            [
                self.wall_brace(
                    self.place_mr,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                    self.place_tr,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                )
            ]
        )

    def wall_end(self, shape: Shape) -> Shape:
        return self.engine.union(
            [
                shape,
                self.wall_brace(
                    self.place_tr,
                    0,
                    -1,
                    self.web_connectors.post_br(),
                    (
                        lambda sh: self.placement.key_place(
                            sh, 3, self.properties.lastrow
                        )
                    ),
                    0,
                    -1,
                    self.web_connectors.post_bl(),
                ),
            ]
        )

    def caps(self) -> Shape:
        return self.layout_1x(self.key_caps.keycap(key_size=1.0), cap=True)

    def connector_hulls(self) -> t.List[Shape]:
        # Get the default thumb cluster connectors
        hulls = super().connector_hulls()

        # Replace the top two
        hulls[0] = self.engine.triangle_hulls(
            [
                self.place_tl(self.post_tr()),
                self.place_tl(self.post_br()),
                self.place_tr(self.web_connectors.post_tl()),
                self.place_tr(self.web_connectors.post_bl()),
            ]
        )

        # Replace the top two to the main keyboard
        hulls[5] = self.engine.triangle_hulls(
            [
                self.place_tl(self.post_tl()),
                self.place_ml(self.web_connectors.post_tr()),
                self.place_tl(self.post_bl()),
                self.place_ml(self.web_connectors.post_br()),
                self.place_tl(self.post_br()),
                self.place_mr(self.web_connectors.post_tr()),
                self.place_tr(self.web_connectors.post_bl()),
                self.place_mr(self.web_connectors.post_br()),
                self.place_tr(self.web_connectors.post_br()),
            ]
        )

        hulls[6] = self.engine.triangle_hulls(
            [
                self.place_tl(self.post_tl()),
                self.placement.key_place(
                    self.web_connectors.post_bl(), 0, self.properties.cornerrow
                ),
                self.place_tl(self.post_tr()),
                self.placement.key_place(
                    self.web_connectors.post_br(), 0, self.properties.cornerrow
                ),
                self.place_tr(self.web_connectors.post_tl()),
                self.placement.key_place(
                    self.web_connectors.post_bl(), 1, self.properties.cornerrow
                ),
                self.place_tr(self.web_connectors.post_tr()),
                self.placement.key_place(
                    self.web_connectors.post_br(), 1, self.properties.cornerrow
                ),
                self.placement.key_place(
                    self.web_connectors.post_bl(), 2, self.properties.lastrow
                ),
                self.place_tr(self.web_connectors.post_tr()),
                self.placement.key_place(
                    self.web_connectors.post_bl(), 2, self.properties.lastrow
                ),
                self.place_tr(self.web_connectors.post_br()),
                self.placement.key_place(
                    self.web_connectors.post_br(), 2, self.properties.lastrow
                ),
                self.placement.key_place(
                    self.web_connectors.post_bl(), 3, self.properties.lastrow
                ),
            ]
        )

        return hulls
