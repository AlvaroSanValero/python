import math


class Robot:
    def __init__(self, dimensions, wheel_separation, wheel_diameter, encoder_resolution, motor_speed, position, angle,
                 wheel_diameter_error, motor_speed_error):
        self.dimensions = dimensions
        self.wheel_separation = wheel_separation
        self.left_wheel_diameter = wheel_diameter + int(wheel_diameter_error / 3 * wheel_diameter)
        self.right_wheel_diameter = wheel_diameter - int(wheel_diameter_error / 3 * wheel_diameter)
        self.encoder_resolution = encoder_resolution
        self.position = position
        self.no_error_position = position
        self.prev_no_error_position = position
        self.angle = angle
        self.no_error_angle = angle
        self.prev_no_error_angle = angle
        self.no_error_motor_speed = motor_speed
        self.left_motor_speed = motor_speed + int(motor_speed_error / 3 * motor_speed)
        self.right_motor_speed = motor_speed - int(motor_speed_error / 3 * motor_speed)
        self.encoder_left = 0
        self.encoder_right = 0
        self.color = "red"
        self.wheel_color = "pink"
        self.no_error_conversion_factor = math.pi * wheel_diameter / encoder_resolution
        self.left_conversion_factor = math.pi * (
                wheel_diameter + wheel_diameter_error / 3 * wheel_diameter) / encoder_resolution
        self.right_conversion_factor = math.pi * (
                wheel_diameter - wheel_diameter_error / 3 * wheel_diameter) / encoder_resolution
        print(self.right_conversion_factor)
        self.wheel_width = 5
        self.wheels = []
        self.update_wheels()

    def action_wheels(self, left, right):
        self.encoder_left = (self.encoder_left + left) % self.encoder_resolution
        self.encoder_right = (self.encoder_right + right) % self.encoder_resolution

        delta_no_error_left = self.no_error_conversion_factor * left
        delta_no_error_right = self.no_error_conversion_factor * right

        delta_left = self.left_conversion_factor * left
        delta_right = self.right_conversion_factor * right

        self.no_error_move(delta_no_error_left * self.no_error_motor_speed,
                           delta_no_error_right * self.no_error_motor_speed)
        self.move(delta_left * self.left_motor_speed, delta_right * self.right_motor_speed)

    def move(self, v_left, v_right):
        prev_position = self.position
        prev_angle = self.angle

        if v_left == v_right:
            self.position = (
                int(self.position[0] + v_left * math.cos(math.radians(self.angle))),
                int(self.position[1] + v_left * math.sin(math.radians(self.angle)))
            )

        elif v_left == -v_right:
            omega = (v_right - v_left) / self.wheel_separation
            self.angle += math.degrees(omega)
        else:
            # Movimiento en arco
            r = (self.wheel_separation / 2) * (v_right + v_left) / (v_right - v_left)
            omega = (v_right - v_left) / self.wheel_separation
            dtheta = omega

            # Centro instantáneo de curvatura (ICC)
            icc_x = self.position[0] - r * math.sin(math.radians(self.angle))
            icc_y = self.position[1] + r * math.cos(math.radians(self.angle))

            # Nueva posición
            new_x = math.cos(dtheta) * (self.position[0] - icc_x) - math.sin(dtheta) * (
                        self.position[1] - icc_y) + icc_x
            new_y = math.sin(dtheta) * (self.position[0] - icc_x) + math.cos(dtheta) * (
                        self.position[1] - icc_y) + icc_y

            self.position = (int(new_x), int(new_y))
            self.angle += math.degrees(dtheta)

        bb_top_left_corner, _, bb_bottom_right_corner, _, _ = self.get_bounding_box()
        bb_min_x, bb_min_y = bb_top_left_corner
        bb_max_x, bb_max_y = bb_bottom_right_corner

        canvas_max_x, canvas_max_y = (600, 400)
        canvas_max_x -= 10
        canvas_max_y -= 10

        if bb_min_x < 0 or bb_min_y < 0 or bb_max_x > canvas_max_x or bb_max_y > canvas_max_y:
            self.position = prev_position
            self.angle = prev_angle
            self.no_error_position = self.prev_no_error_position
            self.no_error_angle = self.prev_no_error_angle
        else:
            self.update_wheels()
            print(f"New real position and angle: X={self.position[0]}, Y={self.position[1]}, Angle={self.angle}")
            print(f"New errorless position and angle: X={self.no_error_position[0]}, "
                  f"Y={self.no_error_position[1]}, Angle={self.no_error_angle}")

    def no_error_move(self, v_left, v_right):
        self.prev_no_error_position = self.no_error_position
        self.prev_no_error_angle = self.no_error_angle
        if v_left == v_right:
            self.no_error_position = (
                int(self.no_error_position[0] + v_left * math.cos(math.radians(self.no_error_angle))),
                int(self.no_error_position[1] + v_left * math.sin(math.radians(self.no_error_angle)))
            )

        elif v_left == -v_right:
            omega = (v_right - v_left) / self.wheel_separation
            self.no_error_angle += math.degrees(omega)
        else:
            # Movimiento en arco
            r = (self.wheel_separation / 2) * (v_right + v_left) / (v_right - v_left)
            omega = (v_right - v_left) / self.wheel_separation
            dtheta = omega

            # Centro instantáneo de curvatura (ICC)
            icc_x = self.no_error_position[0] - r * math.sin(math.radians(self.no_error_angle))
            icc_y = self.no_error_position[1] + r * math.cos(math.radians(self.no_error_angle))

            # Nueva posición
            new_x = math.cos(dtheta) * (self.no_error_position[0] - icc_x) - math.sin(dtheta) * (
                    self.no_error_position[1] - icc_y) + icc_x
            new_y = math.sin(dtheta) * (self.no_error_position[0] - icc_x) + math.cos(dtheta) * (
                    self.no_error_position[1] - icc_y) + icc_y

            self.no_error_position = (int(new_x), int(new_y))
            self.no_error_angle += math.degrees(dtheta)

    def get_corners(self):
        half_width = self.dimensions[0] / 2
        half_length = self.dimensions[1] / 2
        corners = [
            (self.position[0] - half_width, self.position[1] - half_length),
            (self.position[0] - half_width, self.position[1] + half_length),
            (self.position[0] + half_width, self.position[1] + half_length),
            (self.position[0] + half_width, self.position[1] - half_length)
        ]
        return [self.rotate_point(corner) for corner in corners]

    def rotate_point(self, point):
        angle_rad = math.radians(self.angle)
        x_rot = self.position[0] + (point[0] - self.position[0]) * math.cos(angle_rad) - (
                point[1] - self.position[1]) * math.sin(angle_rad)
        y_rot = self.position[1] + (point[0] - self.position[0]) * math.sin(angle_rad) + (
                point[1] - self.position[1]) * math.cos(angle_rad)
        return x_rot, y_rot

    def update_wheels(self):
        half_separation = self.wheel_separation / 2
        left_half_diameter = self.left_wheel_diameter / 2
        right_half_diameter = self.right_wheel_diameter / 2
        self.wheels = [
            [self.rotate_point((self.position[0] - left_half_diameter, self.position[1] - half_separation)),
             self.rotate_point((self.position[0] + left_half_diameter, self.position[1] - half_separation)),
             self.rotate_point(
                 (self.position[0] + left_half_diameter, self.position[1] - half_separation - self.wheel_width)),
             self.rotate_point(
                 (self.position[0] - left_half_diameter, self.position[1] - half_separation - self.wheel_width))],
            [self.rotate_point((self.position[0] - right_half_diameter, self.position[1] + half_separation)),
             self.rotate_point((self.position[0] + right_half_diameter, self.position[1] + half_separation)),
             self.rotate_point(
                 (self.position[0] + right_half_diameter, self.position[1] + half_separation + self.wheel_width)),
             self.rotate_point(
                 (self.position[0] - right_half_diameter, self.position[1] + half_separation + self.wheel_width))]
        ]

    def get_wheels(self):
        return self.wheels

    def get_bounding_box(self):
        corners = self.get_corners()
        min_x = min(corner[0] for corner in corners)
        max_x = max(corner[0] for corner in corners)
        min_y = min(corner[1] for corner in corners)
        max_y = max(corner[1] for corner in corners)

        return [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y), (min_x, min_y)]
