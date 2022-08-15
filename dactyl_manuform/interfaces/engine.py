#!/usr/bin/env python3
from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from pathlib import Path
from types import ModuleType

from dactyl_manuform.types import RenderEngine, Shape, Shapes, XYZ


class Engine(ABC):
    @property
    @abstractmethod
    def kind(self) -> RenderEngine:
        ...

    @property
    @abstractmethod
    def inner(self) -> ModuleType:
        ...

    @abstractmethod
    def box(self, width: float, height: float, depth: float) -> Shape:
        ...

    @abstractmethod
    def cylinder(self, radius: float, height: float, segments: int = 100) -> Shape:
        ...

    @abstractmethod
    def sphere(self, radius: float) -> Shape:
        ...

    @abstractmethod
    def cone(self, r1: float, r2: float, height: float) -> Shape:
        ...

    @abstractmethod
    def rotate(self, shape: t.Optional[Shape], angle: XYZ) -> t.Optional[Shape]:
        ...

    @abstractmethod
    def translate(self, shape: t.Optional[Shape], vector: XYZ) -> t.Optional[Shape]:
        ...

    @abstractmethod
    def mirror(self, shape: Shape, plane: str) -> Shape:  # TODO: plane = Optional?
        ...

    @abstractmethod
    def union(self, shapes: Shapes) -> Shape:
        ...

    @abstractmethod
    def add(self, shapes: Shapes) -> Shape:
        ...

    @abstractmethod
    def difference(self, shape: Shape, shapes: Shapes) -> Shape:
        ...

    @abstractmethod
    def intersect(self, shape1: Shape, shape2: t.Optional[Shape]) -> Shape:
        ...

    @abstractmethod
    def hull_from_points(
        self, points: t.List[t.Any]  # TODO: Find actual input type(s)
    ) -> Shape:
        ...

    @abstractmethod
    def hull_from_shapes(
        self,
        shapes: Shapes,
        points: t.Optional[t.List[t.Any]] = None,  # TODO: Find actual input type(s)
    ) -> Shape:
        ...

    @abstractmethod
    def tess_hull(
        self, shapes: Shapes, tolerance: float = 0.5, angular_tolerance: float = 1
    ) -> Shape:
        ...

    @abstractmethod
    def triangle_hulls(self, shapes: Shapes) -> Shape:
        ...

    @abstractmethod
    def bottom_hull(
        self, p: t.Any, height: float = 0.001
    ) -> Shape:  # TODO: Actual input type(s)
        ...

    @abstractmethod
    def polyline(
        self, point_list: t.List[t.Any]
    ) -> Shape:  # TODO: Actual input type(s)
        ...

    @abstractmethod
    def extrude_poly(
        self,
        outer_poly: Shape,
        inner_polys: t.Optional[Shapes] = None,
        height: float = 1,
    ) -> Shape:
        ...

    @abstractmethod
    def import_file(
        self, fname: Path, convexity: int = 2
    ) -> Shape:  # TODO: Convert to Path?
        ...

    @abstractmethod
    def export_file(self, shape: Shape, fname: Path) -> None:
        ...

    @abstractmethod
    def export_dxf(self, shape: Shape, fname: Path) -> None:
        ...
