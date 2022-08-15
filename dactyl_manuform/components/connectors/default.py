#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.connector import ConnectorComponent

from dactyl_manuform.types import Shape


class DefaultWebConnectorModel(ConnectorComponent):
    def post(self) -> Shape:
        self.log.debug("web_post()")
        post = self.engine.box(self.post_size, self.post_size, self.thickness)
        post = self.engine.translate(
            post, (0, 0, self.config.plate_thickness - (self.thickness / 2))
        )
        return post

    def divide(self, wide: bool = False) -> float:
        if wide:
            return 1.2
        return 2.0

    def post_tr(self, wide: bool = False) -> Shape:
        web_divide = self.divide(wide)

        return self.engine.translate(
            self.post(),
            (
                (self.properties.mount_width / web_divide) - self.post_adj,
                (self.properties.mount_height / 2) - self.post_adj,
                0.0,
            ),
        )

    def post_tl(self, wide: bool = False) -> Shape:
        web_divide = self.divide(wide)
        return self.engine.translate(
            self.post(),
            (
                -(self.properties.mount_width / web_divide) + self.post_adj,
                (self.properties.mount_height / 2) - self.post_adj,
                0.0,
            ),
        )

    def post_bl(self, wide: bool = False) -> Shape:
        web_divide = self.divide(wide)

        return self.engine.translate(
            self.post(),
            (
                -(self.properties.mount_width / web_divide) + self.post_adj,
                -(self.properties.mount_height / 2) + self.post_adj,
                0.0,
            ),
        )

    def post_br(self, wide: bool = False) -> Shape:
        web_divide = self.divide(wide)

        return self.engine.translate(
            self.post(),
            (
                (self.properties.mount_width / web_divide) - self.post_adj,
                -(self.properties.mount_height / 2) + self.post_adj,
                0.0,
            ),
        )

    def render(self) -> Shape:
        self.log.debug("connectors()")
        hulls = []
        for column in range(self.properties.columns - 1):
            iterrows = self.properties.lastrow
            if (
                self.properties.reduced_inner_columns
                <= column
                < (self.properties.columns - self.properties.reduced_outer_columns - 1)
            ):
                iterrows = self.properties.lastrow + 1

            for row in range(iterrows):  # need to consider last_row?
                # for row in range(nrows):  # need to consider last_row?
                places = [
                    self.placement.key_place(self.post_tl(), column + 1, row),
                    self.placement.key_place(self.post_tr(), column, row),
                    self.placement.key_place(self.post_bl(), column + 1, row),
                    self.placement.key_place(self.post_br(), column, row),
                ]
                hulls.append(self.engine.triangle_hulls(places))

        for column in range(self.properties.columns):
            iterrows = self.properties.cornerrow
            if (
                self.properties.reduced_inner_columns
                <= column
                < (self.properties.columns - self.properties.reduced_outer_columns)
            ):
                iterrows = self.properties.lastrow

            for row in range(iterrows):
                places = [
                    self.placement.key_place(self.post_bl(), column, row),
                    self.placement.key_place(self.post_br(), column, row),
                    self.placement.key_place(self.post_tl(), column, row + 1),
                    self.placement.key_place(self.post_tr(), column, row + 1),
                ]
                hulls.append(self.engine.triangle_hulls(places))

        for column in range(self.properties.columns - 1):
            iterrows = self.properties.cornerrow
            if (
                self.properties.reduced_inner_columns
                <= column
                < (self.properties.columns - self.properties.reduced_outer_columns - 1)
            ):
                iterrows = self.properties.lastrow

            for row in range(iterrows):
                places = [
                    self.placement.key_place(self.post_br(), column, row),
                    self.placement.key_place(self.post_tr(), column, row + 1),
                    self.placement.key_place(self.post_bl(), column + 1, row),
                    self.placement.key_place(self.post_tl(), column + 1, row + 1),
                ]
                hulls.append(self.engine.triangle_hulls(places))

            if column == (self.properties.reduced_inner_columns - 1):
                places = [
                    self.placement.key_place(self.post_bl(), column + 1, iterrows),
                    self.placement.key_place(self.post_br(), column, iterrows),
                    self.placement.key_place(self.post_tl(), column + 1, iterrows + 1),
                    self.placement.key_place(self.post_bl(), column + 1, iterrows + 1),
                ]
                hulls.append(self.engine.triangle_hulls(places))
            if column == (
                self.properties.columns - self.properties.reduced_outer_columns - 1
            ):
                places = [
                    self.placement.key_place(self.post_br(), column, iterrows),
                    self.placement.key_place(self.post_bl(), column + 1, iterrows),
                    self.placement.key_place(self.post_tr(), column, iterrows + 1),
                    self.placement.key_place(self.post_br(), column, iterrows + 1),
                ]
                hulls.append(self.engine.triangle_hulls(places))

        return self.engine.union(hulls)
