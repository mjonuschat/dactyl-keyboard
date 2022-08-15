#!/usr/bin/env python3
from __future__ import annotations

from dactyl_manuform.interfaces.base_plate import BasePlateModel

from dactyl_manuform.types import Shape, Side


class DefaultBasePlateModel(BasePlateModel):
    def render_cadquery(self, side: Side = Side.RIGHT) -> Shape:
        cq = self.engine.inner

        wedge_angle = None
        thumb_cluster = self.thumb_cluster(side=side)

        thumb_shape = thumb_cluster.render(side=side)
        thumb_wall_shape = thumb_cluster.walls(side=side, skeleton=self.config.skeletal)
        thumb_wall_shape = self.engine.union(
            [thumb_wall_shape, *thumb_cluster.outers(side=side)]
        )
        thumb_wall_shape = self.engine.union(
            [thumb_wall_shape, *thumb_cluster.outers(side=side)]
        )

        thumb_connector_shape = thumb_cluster.thumb_connectors()
        thumb_connection_shape = thumb_cluster.connection(side=side)

        thumb_section = self.engine.union(
            [
                thumb_shape,
                thumb_connector_shape,
                thumb_wall_shape,
                thumb_connection_shape,
            ]
        )
        thumb_section = self.engine.difference(
            thumb_section, [self.engine.union(thumb_cluster.holes(side=side))]
        )

        shape = self.engine.union(
            [
                self.case_wall.render(side=side),
                *self.screw_inserts.outers(side=side),
                thumb_section,
            ]
        )

        tool = self.screw_inserts.all_shapes(
            self.config.screw_hole_diameter / 2.0,
            self.config.screw_hole_diameter / 2.0,
            350,
            side=side,
        )
        for item in tool:
            item = self.engine.translate(item, (0, 0, -10))
            shape = self.engine.difference(shape, [item])

        tool = thumb_cluster.insert(
            self.config.screw_hole_diameter / 2.0,
            self.config.screw_hole_diameter / 2.0,
            350,
            side=side,
        )
        for item in tool:
            item = self.engine.translate(item, (0, 0, -10))
            shape = self.engine.difference(shape, [item])

        shape = self.engine.translate(shape, (0, 0, -0.0001))

        plane = None
        square = cq.Workplane("XY").rect(1000, 1000)
        for wire in square.wires().objects:
            plane = cq.Workplane("XY").add(cq.Face.makeFromWires(wire))
        shape = self.engine.intersect(shape, plane)

        outside = shape.vertices(
            cq.DirectionMinMaxSelector(cq.Vector(1, 0, 0), True)
        ).objects[0]
        sizes = []
        max_val = 0
        inner_index = 0
        outer_index = 0
        outer_wire = None
        base_wires = shape.wires().objects
        for i_wire, wire in enumerate(base_wires):
            is_outside = False
            for vert in wire.Vertices():
                if vert.toTuple() == outside.toTuple():
                    outer_wire = wire
                    outer_index = i_wire
                    is_outside = True
                    sizes.append(0)
            if not is_outside:
                sizes.append(len(wire.Vertices()))
            if sizes[-1] > max_val:
                inner_index = i_wire
                max_val = sizes[-1]
        self.log.debug(sizes)
        inner_wire = base_wires[inner_index]

        if wedge_angle is not None:
            # TODO: This code looks dead/broken
            cq.Workplane("XY").add(
                cq.Solid.revolve(
                    outerWire, innerWires, angleDegrees, axisStart, axisEnd
                )
            )
        else:
            inner_shape = cq.Workplane("XY").add(
                cq.Solid.extrudeLinear(
                    outerWire=inner_wire,
                    innerWires=[],
                    vecNormal=cq.Vector(0, 0, self.config.base_thickness),
                )
            )
            inner_shape = self.engine.translate(
                inner_shape, (0, 0, -self.config.base_rim_thickness)
            )

            holes = []
            for i in range(len(base_wires)):
                if i not in [inner_index, outer_index]:
                    holes.append(base_wires[i])
            cutout = [*holes, inner_wire]

            shape = cq.Workplane("XY").add(
                cq.Solid.extrudeLinear(
                    outer_wire, cutout, cq.Vector(0, 0, self.config.base_rim_thickness)
                )
            )
            hole_shapes = []
            for hole in holes:
                loc = hole.Center()
                hole_shapes.append(
                    self.engine.translate(
                        self.engine.cylinder(
                            self.config.screw_cbore_diameter / 2.0,
                            self.config.screw_cbore_depth,
                        ),
                        (loc.x, loc.y, 0),
                    )
                )
            shape = self.engine.difference(shape, hole_shapes)
            shape = self.engine.translate(
                shape, (0, 0, -self.config.base_rim_thickness)
            )
            shape = self.engine.union([shape, inner_shape])

        return shape

    def render_solid(self, side: Side = Side.RIGHT) -> Shape:
        sl = self.engine.inner

        thumb_cluster = self.thumb_cluster(side=side)

        shape = self.engine.union(
            [
                self.case_wall.render(side=side),
                *self.screw_inserts.outers(side=side),
                thumb_cluster.walls(side=side),
                *thumb_cluster.outers(side=side),
            ]
        )

        tool = self.engine.translate(
            self.engine.union(self.screw_inserts.holes(side=side)), (0, 0, -10)
        )
        base = self.engine.box(1000, 1000, 0.01)
        shape = shape - tool
        shape = self.engine.intersect(shape, base)

        shape = self.engine.translate(shape, (0, 0, -0.001))

        return sl.projection(cut=True)(shape)
