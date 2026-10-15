class Reserva:
    def __init__(
        self, id_reserva, cliente, mesa, jornada_reserva, estado_reserva=True,
        dia_reserva="Sin día",
    ):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.mesa = mesa
        self.jornada_reserva = jornada_reserva
        self.estado_reserva = estado_reserva
        self.dia_reserva = dia_reserva

    def get_id_reserva(self):
        return self.id_reserva

    def get_cliente(self):
        return self.cliente

    def get_mesa(self):
        return self.mesa

    def get_jornada_reserva(self):
        return self.jornada_reserva

    def get_dia_reserva(self):
        return self.dia_reserva

    def esta_activa(self):
        return self.estado_reserva

    def cancelar_reserva(self):
        if self.estado_reserva:
            self.estado_reserva = False
            return True

        return False

    def generador_ID_reserva( lista_reservas):
        if not lista_reservas:
            return "R001"

        ultimo_id = lista_reservas[-1].get_id_reserva()
        siguiente_numero = int(ultimo_id[1:]) + 1
        id_reserva = f"R{siguiente_numero:03d}"
        while any(reserva.get_id_reserva() == id_reserva for reserva in lista_reservas):
            siguiente_numero += 1
            id_reserva = f"R{siguiente_numero:03d}"
        return id_reserva

    def obtener_informacion(self):
        if self.estado_reserva:
            texto_estado = "Activa"
        else:
            texto_estado = "Cancelada"

        return (f"ID: {self.id_reserva} | Información del cliente: {self.cliente.get_id_cliente()}, {self.cliente.get_nombre_cliente()}, {self.cliente.get_tel_cliente()} | Informacion de mesa: {self.mesa.get_id_mesa()}, Capacidad: {self.mesa.get_capacidad_mesa()} | Día: {self.dia_reserva} | Jornada: {self.jornada_reserva} | Estado: {texto_estado}"
        )

    def obtener_historial(self):
        if self.estado_reserva:
            texto_estado = "Activa"
        else:
            texto_estado = "Cancelada"

        return (
            f"{self.cliente.get_id_cliente()} | {self.mesa.get_id_mesa()} | {self.jornada_reserva} | {texto_estado}"
        )