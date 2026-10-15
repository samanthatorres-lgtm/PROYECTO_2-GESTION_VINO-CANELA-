class Mesa:
    def __init__(self, id_mesa, capacidad_mesa, ubicacion_mesa, estado_mesa=True):
        self.__id_mesa = id_mesa
        self.__capacidad_mesa = capacidad_mesa
        self.__ubicacion_mesa = ubicacion_mesa
        self.__estado_mesa = estado_mesa


    def get_id_mesa(self):
        return self.__id_mesa

    def get_capacidad_mesa(self):
        return self.__capacidad_mesa

    def get_ubicacion_mesa(self):
        return self.__ubicacion_mesa

    def obtener_informacion(self):
        return (
            f"{self.__id_mesa} | {self.__capacidad_mesa} | {self.__ubicacion_mesa}"
        )

    def esta_disponible(self):
        return self.__estado_mesa


    

        
        
        
