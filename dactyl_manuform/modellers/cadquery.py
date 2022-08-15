#!/usr/bin/env python3
from __future__ import annotations

import logging
import typing as t
from pathlib import Path
from types import ModuleType

import cadquery as cq
import numpy as np
from dactyl_manuform.interfaces.engine import Engine

from dactyl_manuform.types import RenderEngine, Shape, Shapes, XYZ
from scipy.spatial import ConvexHull as sphull


class CadQueryEngine(Engine):
    @property
    def kind(self) -> RenderEngine:
        return RenderEngine.CADQUERY

    @property
    def inner(self) -> ModuleType:
        return cq

    def box(self, width: float, height: float, depth: float) -> Shape:
        return cq.Workplane("XY").box(width, height, depth)

    def cylinder(self, radius: float, height: float, segments: int = 100) -> Shape:
        shape = cq.Workplane("XY").union(
            cq.Solid.makeCylinder(radius=radius, height=height)
        )
        shape = self.translate(shape, (0, 0, -height / 2))
        return shape

    def sphere(self, radius: float) -> Shape:
        return cq.Workplane("XY").union(cq.Solid.makeSphere(radius))

    def cone(self, r1: float, r2: float, height: float) -> Shape:
        return cq.Workplane("XY").union(
            cq.Solid.makeCone(radius1=r1, radius2=r2, height=height)
        )

    def rotate(self, shape: t.Optional[Shape], angle: XYZ) -> t.Optional[Shape]:
        if shape is None:
            return None
        origin = (0, 0, 0)
        shape = shape.rotate(
            axisStartPoint=origin, axisEndPoint=(1, 0, 0), angleDegrees=angle[0]
        )
        shape = shape.rotate(
            axisStartPoint=origin, axisEndPoint=(0, 1, 0), angleDegrees=angle[1]
        )
        shape = shape.rotate(
            axisStartPoint=origin, axisEndPoint=(0, 0, 1), angleDegrees=angle[2]
        )
        return shape

    def translate(self, shape: t.Optional[Shape], vector: XYZ) -> t.Optional[Shape]:
        if shape is None:
            return None

        return shape.translate(tuple(vector))

    def mirror(self, shape: Shape, plane: str) -> Shape:
        logging.debug("mirror()")
        return shape.mirror(mirrorPlane=plane)

    def union(self, shapes: Shapes) -> Shape:
        logging.debug("union()")
        shape = None
        for item in shapes:
            if item is not None:
                if shape is None:
                    shape = item
                else:
                    shape = shape.union(item)
        return shape

    def add(self, shapes: Shapes) -> Shape:
        logging.debug("union()")
        shape = None
        for item in shapes:
            if item is not None:
                if shape is None:
                    shape = item
                else:
                    shape = shape.add(item)
        return shape

    def difference(self, shape: Shape, shapes: Shapes) -> Shape:
        logging.debug("difference()")
        for item in shapes:
            if item is not None:
                shape = shape.cut(item)
        return shape

    def intersect(self, shape1: Shape, shape2: t.Optional[Shape]) -> Shape:
        if shape2 is not None:
            return shape1.intersect(shape2)
        else:
            return shape1

    def _face_from_points(
        self, points: t.List[t.Any]  # TODO: Real input type(s)
    ) -> Shape:
        # logging.debug()('face_from_points()')
        edges = []
        num_pnts = len(points)
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % num_pnts]
            edges.append(
                cq.Edge.makeLine(
                    cq.Vector(p1[0], p1[1], p1[2]),
                    cq.Vector(p2[0], p2[1], p2[2]),
                )
            )

        face = cq.Face.makeFromWires(cq.Wire.assembleEdges(edges))

        return face

    def hull_from_points(self, points: t.List[t.Any]) -> Shape:
        # logging.debug()('hull_from_points()')
        hull_calc = sphull(points)
        n_faces = len(hull_calc.simplices)

        faces = []
        for i in range(n_faces):
            face_items = hull_calc.simplices[i]
            fpnts = []
            for item in face_items:
                fpnts.append(points[item])
            faces.append(self._face_from_points(fpnts))

        shape = cq.Solid.makeSolid(cq.Shell.makeShell(faces))
        shape = cq.Workplane("XY").union(shape)
        return shape

    def hull_from_shapes(
        self, shapes: Shapes, points: t.Optional[t.List[t.Any]] = None
    ) -> Shape:
        # logging.debug()('hull_from_shapes()')
        vertices = []
        for shape in shapes:
            verts = shape.vertices()
            for vert in verts.objects:
                vertices.append(np.array(vert.toTuple()))
        if points is not None:
            for point in points:
                vertices.append(np.array(point))

        shape = self.hull_from_points(vertices)
        return shape

    def tess_hull(
        self, shapes: Shapes, tolerance: float = 0.5, angular_tolerance: float = 1
    ) -> Shape:
        # logging.debug()('hull_from_shapes()')
        vertices = []
        solids = []
        for wp in shapes:
            for item in wp.solids().objects:
                solids.append(item)

        for shape in solids:
            verts = shape.tessellate(tolerance, angular_tolerance)[0]
            for vert in verts:
                vertices.append(np.array(vert.toTuple()))

        shape = self.hull_from_points(vertices)
        return shape

    def triangle_hulls(self, shapes: Shapes) -> Shape:
        logging.debug("triangle_hulls()")
        hulls = [cq.Workplane("XY")]
        for i in range(len(shapes) - 2):
            hulls.append(self.hull_from_shapes(shapes[i : (i + 3)]))

        return self.union(hulls)

    def bottom_hull(self, p: t.Any, height: float = 0.001) -> Shape:
        logging.debug("bottom_hull()")
        shape = None
        for item in p:
            vertices = []
            # verts = item.faces('<Z').vertices()
            verts = item.faces().vertices()
            for vert in verts.objects:
                v0 = vert.toTuple()
                v1 = [v0[0], v0[1], -10]
                vertices.append(np.array(v0))
                vertices.append(np.array(v1))

            t_shape = self.hull_from_points(vertices)

            # t_shape = translate(t_shape, [0, 0, height / 2 - 10])

            if shape is None:
                shape = t_shape

            for shp in (*p, shape, t_shape):
                try:
                    shp.vertices()
                except Exception:
                    pass
            shape = self.union([shape, self.hull_from_shapes((shape, t_shape))])

        return shape

    def polyline(self, point_list: t.List[t.Any]) -> Shape:
        return cq.Workplane("XY").polyline(point_list)

    def extrude_poly(
        self,
        outer_poly: Shape,
        inner_polys: t.Optional[Shapes] = None,
        height: float = 1,
    ) -> Shape:
        outer_wires = cq.Wire.assembleEdges(outer_poly.edges().objects)
        inner_wires = []
        if inner_polys is not None:
            for item in inner_polys:
                inner_wires.append(cq.Wire.assembleEdges(item.edges().objects))

        return cq.Workplane("XY").add(
            cq.Solid.extrudeLinear(
                outerWire=outer_wires,
                innerWires=inner_wires,
                vecNormal=cq.Vector(0, 0, height),
            )
        )

    def import_file(self, fname: Path, convexity: int = 2) -> Shape:
        # TODO: clean up log formatting
        filename = fname.with_suffix(".step")
        logging.info("IMPORTING FROM {}".format(filename))
        return cq.Workplane("XY").add(
            cq.importers.importShape(cq.exporters.ExportTypes.STEP, str(filename))
        )

    def export_file(self, shape: Shape, fname: Path) -> None:
        filename = str(fname.with_suffix(".step"))
        logging.info("EXPORTING TO {}".format(fname))
        cq.exporters.export(w=shape, fname=str(filename), exportType="STEP")

    def export_dxf(self, shape: Shape, fname: Path) -> None:
        filename = str(fname.with_suffix(".dxf"))
        logging.info("EXPORTING TO {}".format(filename))
        cq.exporters.export(w=shape, fname=str(filename), exportType="DXF")
