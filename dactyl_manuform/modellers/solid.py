#!/usr/bin/env python3
from __future__ import annotations

import logging
import typing as t
from pathlib import Path
from types import ModuleType

import solid as sl
from dactyl_manuform.interfaces.engine import Engine

from dactyl_manuform.types import RenderEngine, Shape, Shapes, XYZ


class SolidEngine(Engine):
    @property
    def kind(self) -> RenderEngine:
        return RenderEngine.SOLID

    @property
    def inner(self) -> ModuleType:
        return sl

    def box(self, width: float, height: float, depth: float) -> Shape:
        return sl.cube([width, height, depth], center=True)

    def cylinder(self, radius: float, height: float, segments: int = 100) -> Shape:
        return sl.cylinder(r=radius, h=height, segments=segments, center=True)

    def sphere(self, radius: float) -> Shape:
        return sl.sphere(radius)

    def cone(self, r1: float, r2: float, height: float) -> Shape:
        return sl.cylinder(r1=r1, r2=r2, h=height)

    def rotate(self, shape: t.Optional[Shape], angle: XYZ) -> t.Optional[Shape]:
        if shape is None:
            return None
        return sl.rotate(angle)(shape)

    def translate(self, shape: t.Optional[Shape], vector: XYZ) -> t.Optional[Shape]:
        if shape is None:
            return None
        return sl.translate(tuple(vector))(shape)

    def mirror(self, shape: Shape, plane: str) -> Shape:
        logging.debug("mirror()")
        planes = {
            "XY": [0, 0, 1],
            "YX": [0, 0, -1],
            "XZ": [0, 1, 0],
            "ZX": [0, -1, 0],
            "YZ": [1, 0, 0],
            "ZY": [-1, 0, 0],
        }
        return sl.mirror(planes[plane])(shape)

    def union(self, shapes: Shapes) -> Shape:
        logging.debug("union()")
        shape = None
        for item in shapes:
            if item is not None:
                if shape is None:
                    shape = item
                else:
                    shape += item
        return shape

    def add(self, shapes: Shapes) -> Shape:
        logging.debug("union()")
        shape = None
        for item in shapes:
            if item is not None:
                if shape is None:
                    shape = item
                else:
                    shape += item
        return shape

    def difference(self, shape: Shape, shapes: Shapes) -> Shape:
        logging.debug("difference()")
        for item in shapes:
            if item is not None:
                shape -= item
        return shape

    def intersect(self, shape1: Shape, shape2: t.Optional[Shape]) -> Shape:
        if shape2 is not None:
            return sl.intersection()(shape1, shape2)
        else:
            return shape1

    def hull_from_points(self, points: t.List[t.Any]) -> Shape:
        return sl.hull()(*points)

    def hull_from_shapes(
        self, shapes: Shapes, points: t.Optional[t.List[t.Any]] = None
    ) -> Shape:
        hs = []
        if points is not None:
            hs.extend(points)
        if shapes is not None:
            hs.extend(shapes)
        return sl.hull()(*hs)

    def tess_hull(
        self, shapes: Shapes, tolerance: float = 0.5, angular_tolerance: float = 1
    ) -> Shape:
        return sl.hull()(*shapes)

    def triangle_hulls(self, shapes: Shapes) -> Shape:
        logging.debug("triangle_hulls()")
        hulls = []
        for i in range(len(shapes) - 2):
            hulls.append(self.hull_from_shapes(shapes[i : (i + 3)]))

        return self.union(hulls)

    def bottom_hull(self, p: t.Any, height: float = 0.001) -> Shape:
        logging.debug("bottom_hull()")
        shape = None
        for item in p:  # TODO: item is not used - unnecessary loop?
            proj = sl.projection()(p)
            t_shape = sl.linear_extrude(
                height=height, twist=0, convexity=0, center=True
            )(proj)
            t_shape = sl.translate((0.0, 0.0, height / 2 - 10))(t_shape)
            if shape is None:
                shape = t_shape
            shape = sl.hull()(p, shape, t_shape)
        return shape

    def polyline(self, point_list: t.List[t.Any]) -> Shape:
        return sl.polygon(point_list)

    def extrude_poly(
        self,
        outer_poly: Shape,
        inner_polys: t.Optional[Shapes] = None,
        height: float = 1,
    ) -> Shape:
        if inner_polys is not None:
            return sl.linear_extrude(height=height, twist=0, convexity=0, center=True)(
                outer_poly, *inner_polys
            )
        else:
            return sl.linear_extrude(height=height, twist=0, convexity=0, center=True)(
                outer_poly
            )

    def import_file(self, fname: Path, convexity: int = 2) -> Shape:
        filename = fname.with_suffix(".stl")
        logging.info("IMPORTING FROM {}".format(filename))
        return sl.import_stl(str(filename), convexity=convexity)

    def export_file(self, shape: Shape, fname: Path) -> None:
        filename = str(fname.with_suffix(".scad"))
        logging.info("EXPORTING TO {}".format(filename))
        sl.scad_render_to_file(shape, filename)

    def export_dxf(self, shape: Shape, fname: Path) -> None:
        filename = str(fname.with_suffix(".dxf"))
        logging.info("NO DXF EXPORT FOR SOLID".format(filename))
        pass
