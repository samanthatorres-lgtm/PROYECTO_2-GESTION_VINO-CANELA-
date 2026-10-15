import json

from guardar_cliente import lista_clientes
from mesa import Mesa
from reserva import Reserva


def reserva_a_diccionario(reserva):
    return {
        "id_reserva": reserva.get_id_reserva(),
        "cliente": {
            "id": reserva.get_cliente().get_id_cliente(),
            "nombre": reserva.get_cliente().get_nombre_cliente(),
            "telefono": reserva.get_cliente().get_tel_cliente(),
        },
        "mesa": {
            "id": reserva.get_mesa().get_id_mesa(),
            "capacidad": reserva.get_mesa().get_capacidad_mesa(),
            "ubicacion": reserva.get_mesa().get_ubicacion_mesa(),
        },
        "jornada_reserva": reserva.get_jornada_reserva(),
        "estado_reserva": reserva.esta_activa(),
    }


def objetos_a_json(objetos_dict):
    with open("Reserva.json", "w", encoding="utf-8") as archivo:
        json.dump(objetos_dict, archivo, indent=4, ensure_ascii=False)


def main():
    mesa_1 = Mesa("M001", 2, "Ventana")
    mesa_2 = Mesa("M002", 2, "Centro")
    reserva_1 = Reserva("R001", lista_clientes[0], mesa_1, "martes", "Almuerzo", False)
    reserva_2 = Reserva("R002", lista_clientes[1], mesa_2, "viernes", "Cena", False)

    lista_reservas = [reserva_1, reserva_2]
    lista_reservas_dict = []
    for reserva in lista_reservas:
        lista_reservas_dict.append(reserva_a_diccionario(reserva))
    print("\n" + "=" * 48)
    print("              RESERVAS REGISTRADAS")
    print("=" * 48)
    for reserva_dict in lista_reservas_dict:
        print(f"\n  RESERVA {reserva_dict['id_reserva']}")
        print("  " + "-" * 42)
        print(
            f"  Cliente:  {reserva_dict['cliente']['nombre']}"
            f" ({reserva_dict['cliente']['id']})"
        )
        print(f"  Teléfono: {reserva_dict['cliente']['telefono']}")
        print(
            f"  Mesa:     {reserva_dict['mesa']['id']}"
            f" | {reserva_dict['mesa']['ubicacion']}"
            f" | Capacidad: {reserva_dict['mesa']['capacidad']} personas"
        )
        print(f"  Jornada:  {reserva_dict['jornada_reserva']}")
        estado = "Activa" if reserva_dict["estado_reserva"] else "Cancelada"
        print(f"  Estado:   {estado}")
    print("\n" + "=" * 48)

    objetos_a_json(lista_reservas_dict)

if __name__ == "__main__":
    main()