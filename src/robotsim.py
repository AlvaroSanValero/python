import tkinter as tk
import math
from robot import Robot


class RobotSimulator(tk.Tk):
    MIN_WIDTH = 20
    MAX_WIDTH = 100
    MIN_LENGTH = 20
    MAX_LENGTH = 100
    CANVAS_DIMENSIONS = (600, 400)
    CANVAS_BORDER_PADDING = 10
    WHEEL_WIDTH_MIN_FACTOR = 0.1
    WHEEL_WIDTH_MAX_FACTOR = 0.2
    WHEEL_DISTANCE_MIN_FACTOR = 0.25
    WHEEL_DISTANCE_MAX_FACTOR = 0.75
    WHEEL_DIAMETER_MIN_FACTOR = 0.25
    WHEEL_DIAMETER_MAX_FACTOR = 0.75
    MIN_ENCODER_RESOLUTION = 1440
    MAX_ENCODER_RESOLUTION = 23040
    MIN_MOTOR_SPEED = 64
    MAX_MOTOR_SPEED = 512

    def __init__(self):
        super().__init__()

        self.label_error = None
        self.label_no_error_pos = None
        self.label_real_pos = None
        self.ranges = None
        self.btn_start = None
        self.creating = True
        self.title("Simulador de Robot")
        self.canvas = tk.Canvas(self, width=self.CANVAS_DIMENSIONS[0], height=self.CANVAS_DIMENSIONS[1], bg="white")
        self.canvas.pack()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.scroll_canvas = tk.Canvas(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.scroll_canvas.yview)
        self.scrollable_frame = tk.Frame(self.scroll_canvas)

        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scales = {}
        self.init_scales()
        self.init_buttons()
        self.init_labels()  # Initialize labels
        self.init_bindings()

        self.robot = None
        self.update_id = None
        self.track_points = []

    def init_scales(self):
        labels = [
            "Ancho", "Largo", "Posición X", "Posición Y", "Ángulo",
            "Ancho de la rueda", "Distancia entre ruedas", "Diámetro de la rueda",
            "Resolución del encoder", "Velocidad del motor",
            "Error de fabricación del diámetro de la rueda", "Error de fabricación de la velocidad del motor"
        ]

        self.ranges = {
            "width": (self.MIN_WIDTH, self.MAX_WIDTH),
            "length": (self.MIN_LENGTH, self.MAX_LENGTH),
            "pos_x": (self.CANVAS_BORDER_PADDING + self.MIN_WIDTH / 2,
                      self.CANVAS_DIMENSIONS[0] - (self.CANVAS_BORDER_PADDING + self.MIN_WIDTH / 2)),
            "pos_y": (self.CANVAS_BORDER_PADDING + self.MIN_LENGTH / 2,
                      self.CANVAS_DIMENSIONS[1] - (self.CANVAS_BORDER_PADDING + self.MIN_LENGTH / 2)),
            "angle": (0, 360),
            "wheel_width": (math.floor(self.MIN_WIDTH * self.WHEEL_WIDTH_MIN_FACTOR),
                            math.ceil(self.MAX_WIDTH * self.WHEEL_WIDTH_MAX_FACTOR)),
            "wheel_distance": (math.floor(self.MIN_WIDTH * self.WHEEL_DISTANCE_MIN_FACTOR) +
                               math.floor(self.MIN_WIDTH * self.WHEEL_WIDTH_MIN_FACTOR),
                               math.ceil(self.MAX_WIDTH * self.WHEEL_DISTANCE_MAX_FACTOR) +
                               math.floor(self.MIN_WIDTH * self.WHEEL_WIDTH_MIN_FACTOR)),
            "wheel_diameter": (math.floor(self.MIN_LENGTH * self.WHEEL_DIAMETER_MIN_FACTOR),
                               math.ceil(self.MAX_LENGTH * self.WHEEL_DIAMETER_MAX_FACTOR)),
            "encoder_resolution": (self.MIN_ENCODER_RESOLUTION, self.MAX_ENCODER_RESOLUTION),
            "motor_speed": (self.MIN_MOTOR_SPEED, self.MAX_MOTOR_SPEED),
            "wheel_diameter_error": (-1, 1),
            "motor_speed_error": (-1, 1)
        }

        for label, key in zip(labels, self.ranges.keys()):
            resolution = 0.01 if key in ["wheel_diameter_error", "motor_speed_error"] else 1
            self.add_scale(label, key, resolution)

    def add_scale(self, label, key, resolution=1):
        frame = tk.Frame(self.scrollable_frame)
        frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        lbl = tk.Label(frame, text=label, anchor='w')
        lbl.pack(side=tk.LEFT)

        scale = tk.Scale(frame, from_=self.ranges[key][0], to=self.ranges[key][1], orient=tk.HORIZONTAL,
                         resolution=resolution)
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scale.bind("<ButtonRelease-1>", self.update_ranges)
        self.scales[key] = scale

    def init_buttons(self):
        self.btn_start = tk.Button(self.main_frame, text="Start", command=self.start_stop)
        self.btn_start.pack(side=tk.RIGHT, fill=tk.X, padx=10, pady=5)

    def init_labels(self):
        self.label_real_pos = tk.Label(self, text="Posición Real: (0, 0)")
        self.label_real_pos.pack(side=tk.TOP, fill=tk.X)
        self.label_no_error_pos = tk.Label(self, text="Posición Sin Error: (0, 0)")
        self.label_no_error_pos.pack(side=tk.TOP, fill=tk.X)
        self.label_error = tk.Label(self, text="Error Acumulado: (0, 0)")
        self.label_error.pack(side=tk.TOP, fill=tk.X)

    def init_bindings(self):
        self.bind("<KeyPress>", self.key_pressed)

    def key_pressed(self, event):
        if self.creating:
            return

        actions = {
            'i': (5, 5),
            'k': (-5, -5),
            'j': (1, -1),
            'l': (-1, 1),
            'u': (10, 8),
            'o': (8, 10)
        }

        if event.keysym in actions:
            self.robot.action_wheels(*actions[event.keysym])
            self.add_track_point()

    def update_ranges(self, event):
        width = self.scales["width"].get()
        length = self.scales["length"].get()
        self.scales["pos_x"].config(from_=self.CANVAS_BORDER_PADDING + width / 2,
                                    to=self.CANVAS_DIMENSIONS[0] - (self.CANVAS_BORDER_PADDING + width / 2))
        self.scales["pos_y"].config(from_=self.CANVAS_BORDER_PADDING + length / 2,
                                    to=self.CANVAS_DIMENSIONS[1] - (self.CANVAS_BORDER_PADDING + length / 2))
        self.scales["wheel_width"].config(from_=math.floor(width * self.WHEEL_WIDTH_MIN_FACTOR),
                                          to=math.ceil(width * self.WHEEL_WIDTH_MAX_FACTOR))
        self.scales["wheel_distance"].config(
            from_=math.floor(width * self.WHEEL_DISTANCE_MIN_FACTOR) + math.floor(width * self.WHEEL_WIDTH_MIN_FACTOR),
            to=math.ceil(width * self.WHEEL_DISTANCE_MAX_FACTOR) + math.floor(width * self.WHEEL_WIDTH_MIN_FACTOR))
        self.scales["wheel_diameter"].config(from_=math.floor(length * self.WHEEL_DIAMETER_MIN_FACTOR),
                                             to=math.ceil(length * self.WHEEL_DIAMETER_MAX_FACTOR))

    def start_stop(self):
        self.creating = not self.creating
        if self.creating:
            self.btn_start.config(text="Play")
            if self.update_id:
                self.after_cancel(self.update_id)
            self.robot = None
            self.canvas.delete("all")
            self.track_points.clear()
        else:
            self.create_robot()

    def create_robot(self):
        x_robot = self.scales["pos_x"].get()
        y_robot = self.scales["pos_y"].get()
        width = self.scales["width"].get()
        length = self.scales["length"].get()
        wheel_distance = self.scales["wheel_distance"].get()
        wheel_diameter = self.scales["wheel_diameter"].get()
        encoder_resolution = self.scales["encoder_resolution"].get()
        motor_speed = self.scales["motor_speed"].get()
        angle = self.scales["angle"].get()
        wheel_diameter_error = self.scales["wheel_diameter_error"].get()
        motor_speed_error = self.scales["motor_speed_error"].get()

        self.btn_start.config(text="Stop")
        self.robot = Robot(
            dimensions=(width, length),
            wheel_separation=wheel_distance,
            wheel_diameter=wheel_diameter,
            encoder_resolution=encoder_resolution,
            motor_speed=motor_speed,
            position=(x_robot, y_robot),
            angle=angle,
            wheel_diameter_error=wheel_diameter_error,
            motor_speed_error=motor_speed_error
        )
        self.update_robot()

    def update_robot(self):
        self.canvas.delete("all")
        if self.robot:
            corners = self.robot.get_corners()
            self.canvas.create_polygon(corners, fill=self.robot.color, outline="black")

            wheels = self.robot.get_wheels()
            for wheel in wheels:
                self.canvas.create_polygon(wheel, fill=self.robot.wheel_color, outline="black")

            self.draw_arrow()
            for point in self.track_points:
                self.canvas.create_oval(point[0] - 1, point[1] - 1, point[0] + 1, point[1] + 1, fill="green")

            self.draw_bounding_box()
            self.add_track_point()
            self.update_labels()
            self.update_id = self.after(10, self.update_robot)

    def draw_arrow(self):
        # Calculate the end point of the arrow
        arrow_length = 20
        angle_rad = math.radians(self.robot.angle)
        start_x, start_y = self.robot.position
        end_x = start_x + arrow_length * math.cos(angle_rad)
        end_y = start_y + arrow_length * math.sin(angle_rad)

        # Draw the arrow
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="blue", arrow=tk.LAST)

    def draw_bounding_box(self):
        bbox = self.robot.get_bounding_box()
        for i in range(len(bbox) - 1):
            self.canvas.create_line(bbox[i][0], bbox[i][1], bbox[i + 1][0], bbox[i + 1][1], fill="yellow", dash=(5, 2))

    def add_track_point(self):
        self.track_points.append(self.robot.position)

    def update_labels(self):
        real_x, real_y = self.robot.position
        no_error_x, no_error_y = self.robot.no_error_position
        real_angle = self.robot.angle
        no_error_angle = self.robot.no_error_angle

        error_x = real_x - no_error_x
        error_y = real_y - no_error_y
        error_angle = real_angle - no_error_angle

        self.label_real_pos.config(text=f"Posición y Ángulo Real: (X={real_x}, Y={real_y}, Ángulo={real_angle})")
        self.label_no_error_pos.config(
            text=f"Posición y Ángulo Sin Error: (X={no_error_x}, Y={no_error_y}, Ángulo={no_error_angle})")
        self.label_error.config(text=f"Error Acumulado: (X={error_x}, Y={error_y}, Ángulo={error_angle})")


if __name__ == "__main__":
    app = RobotSimulator()
    app.mainloop()
