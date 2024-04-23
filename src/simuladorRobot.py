import tkinter as tk
import math

from src.robot import Robot


class RobotSimulator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Variables para los parámetros del robot
        self.update_id = None
        self.robot_en_canvas = None
        self.robot = None
        self.ancho_robot = tk.DoubleVar(value=10)
        self.largo_robot = tk.DoubleVar(value=10)
        self.angulo_robot = tk.DoubleVar(value=0)
        self.x_robot = tk.DoubleVar(value=300)
        self.y_robot = tk.DoubleVar(value=200)
        self.distancia_entre_ruedas = tk.DoubleVar(value=50)
        self.diametro_ruedas = tk.DoubleVar(value=10)
        self.resolucion_encoder = tk.DoubleVar(value=360)
        self.creando = True

        self.title("Simulador de Robot")  # Establece el título de la ventana
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")  # Crea un lienzo (canvas) en la ventana
        self.canvas.pack()  # Empaqueta el lienzo en la ventana
        # self.robot_id = self.canvas.create_rectangle(295, 195, 305, 205,
        #                                              fill="red")  # Crea un rectángulo rojo para representar al robo

        # Widgets Entry para la entrada de parámetros
        tk.Label(self, text="Ancho del Robot:").pack()  # Crea una etiqueta para el ancho del robot
        self.entry_ancho_robot = tk.Entry(self, textvariable=self.ancho_robot,
                                          width=10)  # Crea un campo de entrada para el ancho del robot
        self.entry_ancho_robot.pack()  # Empaqueta el campo de entrada en la ventana

        tk.Label(self, text="Largo del Robot:").pack()
        self.entry_largo_robot = tk.Entry(self, textvariable=self.largo_robot, width=10)
        self.entry_largo_robot.pack()

        tk.Label(self, text="Distancia entre Ruedas:").pack()
        self.entry_distancia_entre_ruedas = tk.Entry(self, textvariable=self.distancia_entre_ruedas, width=10)
        self.entry_distancia_entre_ruedas.pack()

        tk.Label(self, text="Diámetro de las Ruedas:").pack()
        self.entry_diametro_ruedas = tk.Entry(self, textvariable=self.diametro_ruedas, width=10)
        self.entry_diametro_ruedas.pack()

        tk.Label(self, text="Resolución del Encoder:").pack()
        self.entry_resolucion_encoder = tk.Entry(self, textvariable=self.resolucion_encoder, width=10)
        self.entry_resolucion_encoder.pack()

        tk.Label(self, text="Posicion x:").pack()
        self.entry_posicion_x = tk.Entry(self, textvariable=self.x_robot, width=10)
        self.entry_posicion_x.pack()

        tk.Label(self, text="Posicion y:").pack()
        self.entry_posicion_y = tk.Entry(self, textvariable=self.y_robot, width=10)
        self.entry_posicion_y.pack()

        tk.Label(self, text="Angulo:").pack()
        self.entry_angulo = tk.Entry(self, textvariable=self.angulo_robot, width=10)
        self.entry_angulo.pack()

        # Botón para actualizar parámetros
        self.boton = tk.Button(self, text="Play", command=self.play)
        self.boton.pack()

        # Asociar evento de teclado a método mover_robot
        self.bind("<KeyPress>", self.mover_robot)

    def mover_robot(self, event):
        if self.creando:
            return

        tecla = event.keysym
        if tecla == 'i':
            self.mover_recto(10)
        elif tecla == 'k':
            self.mover_recto(-10)
        elif tecla == 'j':
            self.rotar_izquierda(10)
        elif tecla == 'l':
            self.rotar_derecha(10)
        elif tecla == 'u':
            self.mover_curva(10, 3)
        elif tecla == 'o':
            self.mover_curva(3, 10)

    def play(self):
        self.creando = not self.creando
        if self.creando:
            self.boton.config(text="Play")
            if self.update_id:
                self.after_cancel(self.update_id)
            self.robot = None
            self.canvas.delete(self.robot_en_canvas)

        else:
            self.boton.config(text="Stop")
            self.robot = Robot(
                dimensiones=(self.ancho_robot.get(), self.largo_robot.get()),
                separacion_ruedas=self.distancia_entre_ruedas.get(),
                diametro_ruedas=self.diametro_ruedas.get(),
                resolucion_encoder=self.resolucion_encoder.get(),
                posicion=(self.x_robot.get(), self.y_robot.get()),
                angulo=self.angulo_robot.get()
            )
            self.update()
            #
            # # Calcular puntos para ancho y alto
            # coords_antiguas = self.canvas.coords(self.robot_id)
            # print(coords_antiguas)
            # print(self.ancho_robot.get())
            # print(self.largo_robot.get())
            # self.canvas.coords(self.robot_id, coords_antiguas[0], coords_antiguas[1], coords_antiguas[0] + self.ancho_robot.get(),
            #                    coords_antiguas[1] + self.largo_robot.get())
            # # self.ancho_robot = self.ancho_robot.get()
            # self.largo_robot = self.largo_robot.get()
            # self.distancia_entre_ruedas = self.distancia_entre_ruedas.get()
            # self.diametro_ruedas = self.diametro_ruedas.get()
            # self.resolucion_encoder = self.resolucion_encoder.get()

    # Métodos para realizar los movimientos del robot
    def mover_recto(self, distancia):
        self.robot.posicion = (
            self.robot.posicion[0] + distancia * math.cos(math.radians(self.robot.angulo)),
            self.robot.posicion[1] - distancia * math.sin(math.radians(self.robot.angulo))
        )

        self.mostrar_datos_odometria()

    def rotar_izquierda(self, angulo):
        self.angulo_robot += angulo
        self.actualizar_posicion_robot()
        self.mostrar_datos_odometria()

    def rotar_derecha(self, angulo):
        self.angulo_robot -= angulo
        self.actualizar_posicion_robot()
        self.mostrar_datos_odometria()

    def mover_curva(self, distancia_rueda_derecha, distancia_rueda_izquierda):
        self.x_robot += ((distancia_rueda_derecha + distancia_rueda_izquierda) / 2) * math.cos(
            math.radians(self.angulo_robot))
        self.y_robot -= ((distancia_rueda_derecha + distancia_rueda_izquierda) / 2) * math.sin(
            math.radians(self.angulo_robot))
        self.angulo_robot += math.degrees(
            math.atan((distancia_rueda_derecha - distancia_rueda_izquierda) / self.distancia_entre_ruedas))
        self.actualizar_posicion_robot()
        self.mostrar_datos_odometria()

    # Actualiza la posición del robot en el lienzo
    def actualizar_posicion_robot(self):
        self.canvas.coords(self.robot_id,
                           self.x_robot - self.ancho_robot / 2, self.y_robot - self.largo_robot / 2,
                           self.x_robot + self.ancho_robot / 2, self.y_robot + self.largo_robot / 2)
        self.canvas.update()

    def mostrar_datos_odometria(self):
        print(f"Posición del Robot: {self.robot.posicion}")
        print(f"Orientación del Robot: {self.robot.angulo} grados")

    def update(self):
        self.canvas.delete(self.robot_en_canvas)
        esquinas = self.robot.get_esquinas
        self.canvas.create_oval(esquinas[0][0] - 1, esquinas[0][1] - 1, esquinas[0][0] + 1, esquinas[0][1] + 1,
                                fill="blue")
        self.canvas.create_oval(esquinas[1][0] - 1, esquinas[1][1] - 1, esquinas[1][0] + 1, esquinas[1][1] + 1,
                                fill="blue")
        self.canvas.create_oval(esquinas[2][0] - 1, esquinas[2][1] - 1, esquinas[2][0] + 1, esquinas[2][1] + 1,
                                fill="blue")
        self.canvas.create_oval(esquinas[3][0] - 1, esquinas[3][1] - 1, esquinas[3][0] + 1, esquinas[3][1] + 1,
                                fill="blue")
        self.robot_en_canvas = self.canvas.create_polygon(esquinas, fill=self.robot.color,
                                                          outline="black")
        self.update_id = self.after(10, self.update)


if __name__ == "__main__":
    app = RobotSimulator()
    app.mainloop()
