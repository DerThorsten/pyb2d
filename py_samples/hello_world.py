import pyb2d as b2d
from pyb2d.extra_shapes import OpenBoxShape
import pyb2d_playground as pg
import random
import numpy as np
import math


class MySample(pg.Sample):
    def __init__(self, settings, radius=1.0):
        super(MySample, self).__init__(settings)

        # make a open box
        box_dimensions = [100, 10]
        wall_thickness = 0.1

        box_body_id = b2d.create_static_body(self.world_id, position=(0, 0))

        box_shape = OpenBoxShape(box_dimensions, wall_thickness)
        shape_def = b2d.shape_def(friction=0.3)
        b2d.create_shape(box_body_id, shape_def, box_shape)

        n = 1000
        self.bodies_ids = np.zeros(n, dtype="uint64")
        for i in range(n):
            rx = random.uniform(-box_dimensions[0] / 2, box_dimensions[0] / 2)
            ry = (
                random.uniform(-box_dimensions[1] / 2, box_dimensions[1] / 2)
                + box_dimensions[1] * 2
            )
            position = (rx, ry)
            dynamic_body_id = b2d.create_dynamic_body(
                self.world_id,
                position=position,
                angular_damping=0.01,
                linear_damping=0.01,
            )

            b2d.create_shape(
                dynamic_body_id,
                b2d.shape_def(density=1, friction=0.3, restitution=0.9),
                b2d.circle(radius=radius),
            )
            self.bodies_ids[i] = dynamic_body_id

        self._is_down = False

    def mouse_down(self, pos, button, mod):
        self._is_down = True
        self.apply_force(pos)

    def mouse_up(self, pos, button):
        self._is_down = False

    def mouse_move(self, pos):
        if self._is_down:
            self.apply_force(pos)

    def apply_force(self, pos):
        for body_id in self.bodies_ids:
            body_id = int(body_id)
            body_pos = b2d.body_get_position(body_id)

            delta_vec = ((pos[0] - body_pos[0]), (pos[1] - body_pos[1]))

            magnitude = delta_vec[0] ** 2 + delta_vec[1] ** 2
            magnitude = math.sqrt(magnitude)

            delta_vec = (100 * delta_vec[0] / magnitude, 100 * delta_vec[1] / magnitude)

            b2d.body_apply_force_to_center(body_id, delta_vec, True)


pg.run_sample(MySample)
