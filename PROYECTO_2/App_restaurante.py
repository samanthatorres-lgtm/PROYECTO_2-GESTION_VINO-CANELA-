import json
from pathlib import Path

from reserva import Reserva
from mesa import Mesa
from cliente import Cliente, generador_ID_cliente

##JSON
#JSON PARA CLIENTE
def cliente_a_diccionario(cliente):
    return {
        "id": cliente.get_id_cliente(),
        "nombre": cliente.get_nombre_cliente(),
        "telefono": cliente.get_tel_cliente()
    }

def clientes_objetos_a_json(objetos_dict):
    with open(Path(__file__).with_name("Cliente.json"), "w", encoding="utf-8") as archivo:
        json.dump(objetos_dict, archivo, indent=4)

def json_a_objetos(clientes):
    try:
        with open(Path(__file__).with_name("Cliente.json"), "r", encoding="utf-8") as archivo:
            lista_clientes_dict = json.load(archivo)
            for cliente_dict in lista_clientes_dict:
                cliente = Cliente(
                    cliente_dict["id"],
                    cliente_dict["nombre"],
                    cliente_dict["telefono"]
                )
                clientes.append(cliente)
    except FileNotFoundError:
        print("El archivo 'Cliente.json' no existe. Se creará uno nuevo al guardar clientes.")
    except json.JSONDecodeError:
        print("El archivo 'Cliente.json' está vacío o tiene un formato incorrecto.")


#JSON PARA RESERVA
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
        "dia_reserva": reserva.get_dia_reserva(),
        "jornada_reserva": reserva.get_jornada_reserva(),
        "estado_reserva": reserva.esta_activa(),
    }

def reservas_objetos_a_json(objetos_dict):
    with open("Reserva.json", "w", encoding="utf-8") as archivo:
        json.dump(objetos_dict, archivo, indent=4)

def reservas_json_a_objetos(reservas, clientes, mesas):
    try:
        with open("Reserva.json", "r", encoding="utf-8") as archivo:
            lista_reservas_dict = json.load(archivo)
            for reserva_dict in lista_reservas_dict:
                cliente_dict = reserva_dict["cliente"]
                cliente = buscar_cliente_ID(clientes, cliente_dict["id"])
                if cliente is None:
                    cliente = Cliente(
                        cliente_dict["id"],
                        cliente_dict["nombre"],
                        cliente_dict["telefono"],
                    )
                    clientes.append(cliente)

                mesa_dict = reserva_dict["mesa"]
                mesa = next(
                    (mesa for mesa in mesas if mesa.get_id_mesa() == mesa_dict["id"]),
                    None,
                )
                if mesa is None:
                    mesa = Mesa(
                        mesa_dict["id"],
                        mesa_dict["capacidad"],
                        mesa_dict["ubicacion"],
                    )
                    mesas.append(mesa)

                reserva = Reserva(
                    reserva_dict["id_reserva"],
                    cliente,
                    mesa,
                    reserva_dict["jornada_reserva"],
                    reserva_dict["estado_reserva"],
                    reserva_dict.get("dia_reserva", "Sin día"),
                )
                reservas.append(reserva)
    except FileNotFoundError:
        print("El archivo 'Reserva.json' no existe. Se creará uno nuevo al guardar reservas.")
    except json.JSONDecodeError:
        print("El archivo 'Reserva.json' está vacío o tiene un formato incorrecto.")

#_________

#FUNCIONES GENERALES
def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingrese un número entero válido.")

def imprimir_tabla(encabezados, filas):
    anchos = [
        max(len(str(encabezado)), *(len(str(fila[indice])) for fila in filas))
        for indice, encabezado in enumerate(encabezados)
    ]
    separador = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"

    print(separador)
    print(
        "| "
        + " | ".join(
            str(encabezado).ljust(anchos[indice])
            for indice, encabezado in enumerate(encabezados)
        )
        + " |"
    )
    print(separador)
    for fila in filas:
        print(
            "| "
            + " | ".join(
                str(valor).ljust(anchos[indice])
                for indice, valor in enumerate(fila)
            )
            + " |"
        )
    print(separador)


#FUNCIONES PARA CLIENTE
def registro_nuevo_cliente(lista_clientes):

    while True:
        nombre_cliente_us = input("Ingrese el nombre del cliente: ")
        if not nombre_cliente_us:
            print("El nombre del cliente no puede estar vacío.")
        elif nombre_cliente_us.isnumeric():
            print("El nombre del cliente no puede ser un número.")
        elif len(nombre_cliente_us) < 3:
            print("El nombre del cliente debe tener al menos 3 caracteres.")
        else: 
            break
        
    while True:         
        tel_cliente_us = input("Ingrese el teléfono del cliente: ")
        if not tel_cliente_us:
            print("El teléfono del cliente no puede estar vacío.")
        elif not tel_cliente_us.isnumeric():
            print("El teléfono del cliente debe ser un número.")
        elif len(tel_cliente_us) < 10 or len(tel_cliente_us) > 10:
            print("El teléfono del cliente debe tener exactamente 10 caracteres.")
        else:
            break

    return lista_clientes.append(Cliente(generador_ID_cliente(lista_clientes), nombre_cliente_us, tel_cliente_us))

def buscar_cliente_ID(lista_clientes, cns_ID_cliente):
    for cliente in lista_clientes:
        if cliente.get_id_cliente() == cns_ID_cliente:
            return cliente
        
    return None

def mostrar_clientes(lista_clientes):
    if not lista_clientes:
        print("No hay clientes registrados.")
        return

    filas = [
        [
            cliente.get_id_cliente(),
            cliente.get_nombre_cliente(),
            cliente.get_tel_cliente(),
        ]
        for cliente in lista_clientes
    ]
    print("\nCLIENTES REGISTRADOS")
    imprimir_tabla(["Código cliente", "Nombre", "Teléfono"], filas)

def modificar_telefono(cns_ID_cliente, new_tel_cliente, lista_clientes):
    cliente = buscar_cliente_ID(lista_clientes, cns_ID_cliente)
    if cliente:
        cliente.tel_cliente = new_tel_cliente
        return True
    return False

def validar_telefono():
    while True:
        new_tel_cliente = input("Ingrese el nuevo teléfono del cliente: ").strip()
        if not new_tel_cliente:
            print("El teléfono del cliente no puede estar vacío.")
        elif not new_tel_cliente.isnumeric():
            print("El teléfono del cliente debe ser un número.")
        elif len(new_tel_cliente) != 10:
            print("El teléfono del cliente debe tener exactamente 10 caracteres.")
        else:
            return new_tel_cliente

def validar_id_cliente(lista_clientes):
    cns_ID_cliente = input("Ingrese el ID del cliente cuyo teléfono desea modificar: ").strip().upper()
    for cliente in lista_clientes:
        if cliente.get_id_cliente() == cns_ID_cliente:
            return cliente
    return None        


#FUNCIONES PARA MESA
def buscar_mesa_capacidad_cliente(lista_mesas, cns_capacidad_cliente):
        lista_mesas_encontradas = []
        for mesa in lista_mesas:
            if mesa.get_capacidad_mesa() >= cns_capacidad_cliente:
                lista_mesas_encontradas.append(mesa)
        return lista_mesas_encontradas

def buscar_mesa_ubicacion(lista_mesas, cns_ubicacion_cliente):
        lista_mesas_encontradas = []
        for mesa in lista_mesas:
            if mesa.get_ubicacion_mesa().lower() == cns_ubicacion_cliente.lower():
                lista_mesas_encontradas.append(mesa)
        return lista_mesas_encontradas

def mostrar_mesas(lista_mesas):
    if not lista_mesas:
        print("No hay mesas registradas.")
        return

    filas = [
        [
            mesa.get_id_mesa(),
            mesa.get_capacidad_mesa(),
            mesa.get_ubicacion_mesa(),
        ]
        for mesa in lista_mesas
    ]
    print("\nMESAS DEL RESTAURANTE")
    imprimir_tabla(["Código mesa", "Capacidad", "Ubicación"], filas)

def validar_id_mesa(id_mesa, lista_mesas):
    while True:
        for mesa in lista_mesas:
            if mesa.get_id_mesa() != id_mesa:
                print(f"El ID de la mesa {id_mesa} no existe en la lista de mesas.")
            else:
                return mesa.obtener_informacion()


#FUNCIONES PARA RESERVA
def registrar_reserva( lista_clientes, lista_mesas, lista_reservas):
    if not lista_clientes:
        print("No hay clientes registrados.")
        return
    if not lista_mesas:
        print("No hay mesas disponibles.")
        return

    mostrar_clientes(lista_clientes)
    while True:
        id_cliente_us = input("Ingrese el ID del cliente: ").strip().upper()
        c = buscar_cliente_ID(lista_clientes, id_cliente_us)
        if c is not None:
            print(c.obtener_informacion())
            break
        print("No se encontró un cliente con ese ID.")

    dias = {
        "lunes": "lunes",
        "martes": "martes",
        "miercoles": "miércoles",
        "jueves": "jueves",
        "viernes": "viernes",
        "sabado": "sábado",
    }
    while True:
        dia = input(
            "Ingrese el día de la reserva (lunes, martes, miércoles, jueves, viernes o sábado): "
        ).strip().lower().replace("é", "e").replace("á", "a")
        if dia in dias:
            dia_reserva_us = dias[dia]
            break
        print("Ingrese un día válido de lunes a sábado.")

    while True:
        jornada_reserva_us = input(
            "Ingrese la jornada de la reserva (1: Almuerzo, 2: Tarde, 3: Cena): "
        ).strip()
        if jornada_reserva_us in ["1", "2", "3"]:
            break
        print("La jornada debe ser '1', '2' o '3'.")

    mesas_disponibles = [
        mesa for mesa in lista_mesas
        if not hay_reserva_activa_en_mesa(
            lista_reservas, mesa.get_id_mesa(), jornada_reserva_us, dia_reserva_us
        )
    ]
    if not mesas_disponibles:
        print("No hay mesas disponibles para esa jornada.")
        return
    mostrar_mesas(mesas_disponibles)

    while True:
        id_mesa_us = input("Ingrese el ID de la mesa: ").strip().upper()
        m = next(
            (mesa for mesa in mesas_disponibles if mesa.get_id_mesa() == id_mesa_us),
            None,
        )
        if m is not None:
            break
        print("Ingrese el código de una mesa disponible para esa jornada.")

    if hay_reserva_activa_en_mesa(
        lista_reservas, m.get_id_mesa(), jornada_reserva_us, dia_reserva_us
    ):
        print("La mesa ya está reservada para esa jornada.")
        return

    lista_reservas.append(
        Reserva(
            Reserva.generador_ID_reserva(lista_reservas),
            c,
            m,
            jornada_reserva_us,
            True,
            dia_reserva_us,
        )
    )
    print("Reserva registrada correctamente.")

def hay_reserva_activa_en_mesa(lista_reservas, id_mesa, jornada_reserva, dia_reserva=None):
    for reserva in lista_reservas:
        if (
            reserva.esta_activa()
            and reserva.get_mesa().get_id_mesa() == id_mesa
            and reserva.get_jornada_reserva().lower() == jornada_reserva.lower()
            and (
                dia_reserva is None
                or reserva.get_dia_reserva().lower() == dia_reserva.lower()
            )
        ):
            return True
    return False

def busqueda_reserva_por_mesa_jornada(lista_reservas, lista_mesas):
    if not lista_mesas:
        print("No hay mesas registradas.")
        return

    while True:
        id_mesa_us = input("Ingrese el ID de la mesa: ").strip().upper()
        mesa = next(
            (mesa for mesa in lista_mesas if mesa.get_id_mesa() == id_mesa_us),
            None,
        )
        if mesa is not None:
            break
        print("No se encontró una mesa con ese ID.")

    while True:
        jornada_reserva_us = input(
            "Ingrese la jornada (1: Almuerzo, 2: Tarde, 3: Cena): "
        ).strip()
        if jornada_reserva_us in ["1", "2", "3"]:
            break
        print("La jornada debe ser '1', '2' o '3'.")

    reservas_encontradas = [
        reserva
        for reserva in lista_reservas
        if reserva.get_mesa().get_id_mesa() == mesa.get_id_mesa()
        and reserva.get_jornada_reserva() == jornada_reserva_us
    ]
    if reservas_encontradas:
        mostrar_reservas(reservas_encontradas)
    else:
        print("No se encontró una reserva con esa mesa y jornada.")

def busqueda_reserva_por_cliente_jornada(lista_reservas, lista_clientes):
    if not lista_clientes:
        print("No hay clientes registrados.")
        return

    while True:
        id_cliente_us = input("Ingrese el ID del cliente: ").strip().upper()
        cliente = buscar_cliente_ID(lista_clientes, id_cliente_us)
        if cliente is not None:
            break
        print("No se encontró un cliente con ese ID.")

    while True:
        jornada_reserva_us = input(
            "Ingrese la jornada (1: Almuerzo, 2: Tarde, 3: Cena): "
        ).strip()
        if jornada_reserva_us in ["1", "2", "3"]:
            break
        print("La jornada debe ser '1', '2' o '3'.")

    reservas_encontradas = [
        reserva
        for reserva in lista_reservas
        if reserva.get_cliente().get_id_cliente() == cliente.get_id_cliente()
        and reserva.get_jornada_reserva() == jornada_reserva_us
    ]
    if reservas_encontradas:
        mostrar_reservas(reservas_encontradas)
    else:
        print("No se encontró una reserva con ese cliente y jornada.")

def mostrar_reservas(reservas, incluir_numero=False):
    encabezados = [
        "Código reserva",
        "Código cliente",
        "Nombre cliente",
        "Código mesa",
        "Día",
        "Jornada",
        "Estado",
    ]
    filas = []

    if incluir_numero:
        encabezados.insert(0, "N.º")

    for indice, reserva in enumerate(reservas, start=1):
        fila = [
            reserva.get_id_reserva(),
            reserva.get_cliente().get_id_cliente(),
            reserva.get_cliente().get_nombre_cliente(),
            reserva.get_mesa().get_id_mesa(),
            reserva.get_dia_reserva().capitalize(),
            reserva.get_jornada_reserva().capitalize(),
            "Activa" if reserva.esta_activa() else "Cancelada",
        ]
        if incluir_numero:
            fila.insert(0, indice)
        filas.append(fila)

    if not filas:
        print("No hay reservas registradas.")
        return

    print("\nRESERVAS")
    imprimir_tabla(encabezados, filas)

def obtener_historial_reservas(lista_reservas):
    if not lista_reservas:
        print("No hay reservas registradas.")
        return

    print("\nHISTORIAL DE RESERVAS")
    mostrar_reservas(lista_reservas)

def validar_jornada_reserva(jornada_reserva):
    while True:
        if jornada_reserva not in ["1", "2", "3"]:
            print("La jornada de reserva debe ser '1', '2' o '3'. (1: Almuerzo, 2: Tarde, 3: Cena)")
        else:
            return jornada_reserva

        


##MENUS!!!!!

def menu_clientes(lista_clientes):
    opcion_c = 0

    while opcion_c != 6:
        print("\n--- MENÚ CLIENTES ---")
        print("1. Registrar cliente nuevo")
        print("2. Consultar cliente por ID")
        print("3. Modificar teléfono de cliente")
        print("4. Mostrar todos los clientes")
        print("5. Guardar clientes en JSON")
        print("6. Volver al menú principal")
        opcion_c = leer_entero("Seleccione una opción: ")

        if opcion_c == 1:
            registro_nuevo_cliente(lista_clientes)

        elif opcion_c == 2:
            cns_ID_cliente = input("Ingrese el ID del cliente a consultar: ").strip().upper()
            cliente = buscar_cliente_ID(lista_clientes, cns_ID_cliente)
            if cliente is None:
                print("No se encontró un cliente con ese ID.")
            else:
                print(cliente.obtener_informacion())

        elif opcion_c == 3:
            cliente = validar_id_cliente(lista_clientes)
            if cliente is None:
                print("No se puede modificar el teléfono de un cliente que no existe.")
            else:
                print(cliente.obtener_informacion())
                new_tel_cliente = validar_telefono()
                if modificar_telefono(
                    cliente.get_id_cliente(), new_tel_cliente, lista_clientes
                ):
                    print("Teléfono del cliente actualizado correctamente.")

        elif opcion_c == 4:
            mostrar_clientes(lista_clientes)

        elif opcion_c == 5:
                    lista_clientes_dict = []
                    for c in lista_clientes:
                        lista_clientes_dict.append(cliente_a_diccionario(c))
                    clientes_objetos_a_json(lista_clientes_dict)
                    print("Clientes guardados en 'Cliente.json'.")

        elif opcion_c == 6:
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida")

def menu_mesas(lista_mesas):
    opcion_m = 0

    while opcion_m != 3:
        print("\n--- MENÚ MESAS ---")
        print("1. Consultar mesa por capacidad")
        print("2. Mostrar todas las mesas")
        print("3. Volver al menú principal")
        opcion_m = leer_entero("Seleccione una opción: ")

        if opcion_m == 1:
            cns_capacidad_cliente = leer_entero("Ingrese la capacidad de la mesa a consultar: ")
            if cns_capacidad_cliente <= 0 or cns_capacidad_cliente > 8:
                print("la capacidad de la mesa debe ser un número positivo y no mayor a 8.")
            else:
                mesas_encontradas = buscar_mesa_capacidad_cliente(
                    lista_mesas, cns_capacidad_cliente
                )
                if mesas_encontradas:
                    for mesa in mesas_encontradas:
                        print(mesa.obtener_informacion())
                else:
                    print("No se encontraron mesas con esa capacidad.")
       
        elif opcion_m == 2:
            mostrar_mesas(lista_mesas)
        elif opcion_m == 3:
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida")

def menu_reservas(lista_reservas, lista_clientes, lista_mesas):
    opcion_r = 0

    while opcion_r != 7:
        print("\n--- MENÚ RESERVAS ---")
        print("1. Registrar nueva reserva")
        print("2. Buscar reserva por mesa y jornada")
        print("3. Buscar reserva por cliente y jornada")
        print("4. Cancelar una reserva")
        print("5. Consultar historial de reservas")
        print("6. Guardar reservas en JSON")
        print("7. Volver al menú principal")
        opcion_r = leer_entero("Seleccione una opción: ")

        if opcion_r == 1:
            registrar_reserva( lista_clientes, lista_mesas, lista_reservas)
        elif opcion_r == 2:
            busqueda_reserva_por_mesa_jornada(lista_reservas, lista_mesas)
        elif opcion_r == 3:
            busqueda_reserva_por_cliente_jornada(lista_reservas, lista_clientes)
        elif opcion_r == 4:
            id_reserva = input("Ingrese el código de la reserva que desea cancelar: ").strip().upper()
            for reserva in lista_reservas:
                if reserva.get_id_reserva() == id_reserva:
                    if reserva.cancelar_reserva():
                        print("Reserva cancelada correctamente.")
                    else:
                        print("La reserva ya estaba cancelada.")
                    break
            else:
                print("No se encontró una reserva con ese código.")
        elif opcion_r == 5:
            obtener_historial_reservas(lista_reservas)

        elif opcion_r == 6:
                    lista_reservas_dict = []
                    for c in lista_reservas:
                        lista_reservas_dict.append(reserva_a_diccionario(c))
                    reservas_objetos_a_json(lista_reservas_dict)
                    print("Reservas guardadas en 'Reserva.json'.")
        elif opcion_r == 7:
            print("Volviendo al menú principal...")
        else:
            print("Opción inválida")

def main ():
    # Las 11 mesas físicas tienen una capacidad total de 40 personas.
    lista_mesas = [
        Mesa("M001", 2, "Ventana", True),
        Mesa("M002", 2, "Centro", True),
        Mesa("M003", 2, "Terraza", True),
        Mesa("M004", 2, "Barra", True),
        Mesa("M005", 2, "Patio", True),
        Mesa("M006", 4, "Ventana", True),
        Mesa("M007", 4, "Centro", True),
        Mesa("M008", 4, "Terraza", True),
        Mesa("M009", 6, "Barra", True),
        Mesa("M010", 6, "Patio", True),
        Mesa("M011", 8, "Salón", True),
    ]

    lista_clientes = []
    lista_reservas = []
    json_a_objetos(lista_clientes)
    reservas_json_a_objetos(lista_reservas, lista_clientes, lista_mesas)
    opcion = 0

    while opcion != 4:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Gestión de Clientes")
        print("2. Gestión de Mesas")
        print("3. Gestión de Reservas")
        print("4. Salir")
        opcion = leer_entero("Seleccione una opción: ")

        if opcion == 1:
            menu_clientes(lista_clientes)
        elif opcion == 2:
            menu_mesas(lista_mesas)
        elif opcion == 3:
            menu_reservas(lista_reservas, lista_clientes, lista_mesas)
        elif opcion == 4:
            print("Fin del programa")
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
