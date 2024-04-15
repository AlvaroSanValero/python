import tkinter as tk
import math

class RobotSimulator(tk.Tk):
     def __init__(self):
        super().__init__()
        self.title("Simulador de Robot")  # Establece el título de la ventana
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")  # Crea un lienzo (canvas) en la ventana
        self.canvas.pack()  # Empaqueta el lienzo en la ventana
        self.robot = self.canvas.create_rectangle(295, 195, 305, 205, fill="red")  # Crea un rectángulo rojo para representar al robot

        # Variables para los parámetros del robot
        self.ancho_robot = tk.DoubleVar(value=10)
        self.largo_robot = tk.DoubleVar(value=10)
        self.angulo_robot = 0
        self.x_robot = 300
        self.y_robot = 200
        self.distancia_entre_ruedas = tk.DoubleVar(value=50)
        self.diametro_ruedas = tk.DoubleVar(value=10)
        self.resolucion_encoder = tk.DoubleVar(value=360)
        
        # Widgets Entry para la entrada de parámetros
        tk.Label(self, text="Ancho del Robot:").pack()  # Crea una etiqueta para el ancho del robot
        self.entry_ancho_robot = tk.Entry(self, textvariable=self.ancho_robot, width=10)  # Crea un campo de entrada para el ancho del robot
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
        
        # Botón para actualizar parámetros
        tk.Button(self, text="Actualizar Parámetros", command=self.actualizar_parametros).pack()
        
         # Asociar evento de teclado a método mover_robot
        self.bind("<KeyPress>", self.mover_robot)
        
    def mover_robot(self, event):
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
    
    def actualizar_parametros(self):
        self.ancho_robot = self.ancho_robot.get()
        self.largo_robot = self.largo_robot.get()
        self.distancia_entre_ruedas = self.distancia_entre_ruedas.get()
        self.diametro_ruedas = self.diametro_ruedas.get()
        self.resolucion_encoder = self.resolucion_encoder.get()

     # Métodos para realizar los movimientos del robot
    def mover_recto(self, distancia):
        self.x_robot += distancia * math.cos(math.radians(self.angulo_robot))
        self.y_robot -= distancia * math.sin(math.radians(self.angulo_robot))
        self.actualizar_posicion_robot()
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
        self.x_robot += ((distancia_rueda_derecha + distancia_rueda_izquierda) / 2) * math.cos(math.radians(self.angulo_robot))
        self.y_robot -= ((distancia_rueda_derecha + distancia_rueda_izquierda) / 2) * math.sin(math.radians(self.angulo_robot))
        self.angulo_robot += math.degrees(math.atan((distancia_rueda_derecha - distancia_rueda_izquierda) / self.distancia_entre_ruedas))
        self.actualizar_posicion_robot()
        self.mostrar_datos_odometria()
      # Actualiza la posición del robot en el lienzo
    def actualizar_posicion_robot(self):
        self.canvas.coords(self.robot, 
                           self.x_robot - self.ancho_robot / 2, self.y_robot - self.largo_robot / 2,
                           self.x_robot + self.ancho_robot / 2, self.y_robot + self.largo_robot / 2)
        self.canvas.update()

    def mostrar_datos_odometria(self):
        print("Posición del Robot: ({}, {})".format(self.x_robot, self.y_robot))
        print("Orientación del Robot: {} grados".format(self.angulo_robot))

if __name__ == "__main__":
    app = RobotSimulator()
    app.mainloop()
