class Cliente:
    def __init__(self, id_cliente, nombre_cliente, tel_cliente):
        self.id_cliente = id_cliente
        self.__nombre_cliente = nombre_cliente
        self.tel_cliente = tel_cliente

    def get_id_cliente(self):
        return self.id_cliente

    def get_nombre_cliente(self):
        return self.__nombre_cliente

    def get_tel_cliente(self):
        return self.tel_cliente

    def obtener_informacion(self):
        return (
            f"ID: {self.id_cliente} | Nombre: {self.__nombre_cliente} | Teléfono: {self.tel_cliente}"
        )

    @staticmethod
    def buscar_cliente_ID(lista_clientes, cns_ID_cliente):
        for cliente in lista_clientes:
            if cliente.get_id_cliente() == cns_ID_cliente:
                return cliente
        return None


def generador_ID_cliente( lista_clientes):
    if not lista_clientes:
        return "C001"

    ultimo_id = lista_clientes[-1].get_id_cliente()
    siguiente_numero = int(ultimo_id[1:]) + 1
    nuevo_id = f"C{siguiente_numero:03d}"
    while any(cliente.get_id_cliente() == nuevo_id for cliente in lista_clientes):
        siguiente_numero += 1
        nuevo_id = f"C{siguiente_numero:03d}"
    return nuevo_id


