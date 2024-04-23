import math


class Robot():
    def __init__(self, dimensiones, separacion_ruedas, diametro_ruedas, resolucion_encoder, posicion, angulo):
        self.color = "red"
        self.dimesiones = dimensiones
        self.separacion_ruedas = separacion_ruedas
        self.diametro_ruedas = diametro_ruedas
        self.resolucion_encoder = resolucion_encoder
        self.encoder_izq = 0
        self.encoder_der = 0
        self.posicion = posicion
        self.angulo = angulo

    def actualizar(self, x, y, alfa):
        self.posicion = (self.posicion[0] + x, self.posicion[1] + y)
        self.angulo = self.angulo + alfa

    def get_esquinas(self):
        rot_1 = self.__rotate_point(
            (self.posicion[0] - self.dimesiones[0] / 2, self.posicion[1] - self.dimesiones[1] / 2), self.angulo
        )
        rot_3 = self.__rotate_point(
            (self.posicion[0] + self.dimesiones[0] / 2, self.posicion[1] + self.dimesiones[1] / 2), self.angulo
        )
        rot_2 = self.__rotate_point(
            (self.posicion[0] - self.dimesiones[0] / 2, self.posicion[1] + self.dimesiones[1] / 2), self.angulo
        )
        rot_4 = self.__rotate_point(
            (self.posicion[0] + self.dimesiones[0] / 2, self.posicion[1] - self.dimesiones[1] / 2), self.angulo
        )
        return (
            rot_1,
            rot_2,
            rot_3,
            rot_4
        )

    def __rotate_point(self, p, angulo):
        # Convertir el ángulo a radianes
        angle_rad = math.radians(angulo)
        # Calcular las nuevas coordenadas después de la rotación
        x_rot = self.posicion[0] + (p[0] - self.posicion[0]) * math.cos(angle_rad) - (
                p[1] - self.posicion[1]) * math.sin(angle_rad)
        y_rot = self.posicion[1] + (p[0] - self.posicion[0]) * math.sin(angle_rad) + (
                p[1] - self.posicion[1]) * math.cos(angle_rad)
        return x_rot, y_rot
