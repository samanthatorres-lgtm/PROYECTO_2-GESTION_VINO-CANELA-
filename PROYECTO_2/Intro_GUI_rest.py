import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from cliente import Cliente, generador_ID_cliente
from mesa import Mesa
from reserva import Reserva


CARPETA = Path(__file__).resolve().parent
ARCHIVO_CLIENTES = CARPETA / "Cliente.json"
ARCHIVO_RESERVAS = CARPETA / "Reserva.json"
DIAS = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado")
JORNADAS = {"Almuerzo": "1", "Tarde": "2", "Cena": "3"}
NOMBRES_JORNADA = {codigo: nombre for nombre, codigo in JORNADAS.items()}
MESAS = [
    Mesa("M001", 2, "Ventana"), Mesa("M002", 2, "Centro"),
    Mesa("M003", 2, "Terraza"), Mesa("M004", 2, "Barra"),
    Mesa("M005", 2, "Patio"), Mesa("M006", 4, "Ventana"),
    Mesa("M007", 4, "Centro"), Mesa("M008", 4, "Terraza"),
    Mesa("M009", 6, "Barra"), Mesa("M010", 6, "Patio"),
    Mesa("M011", 8, "Salón"),
]
POSICIONES_MESAS = {
    "M001": (136, 228), "M002": (481, 224), "M003": (730, 231),
    "M004": (275, 457), "M005": (486, 457), "M006": (248, 289),
    "M007": (529, 308), "M008": (809, 302), "M009": (254, 564),
    "M010": (511, 568), "M011": (764, 558),
}


def cargar_datos():
    try:
        with ARCHIVO_CLIENTES.open(encoding="utf-8") as archivo:
            clientes = [
                Cliente(item["id"], item["nombre"], item["telefono"])
                for item in json.load(archivo)
            ]
    except FileNotFoundError:
        clientes = []
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        messagebox.showerror("Error", f"No se pudieron leer los clientes:\n{error}")
        clientes = []

    reservas = []
    reservas_incompletas = []
    try:
        with ARCHIVO_RESERVAS.open(encoding="utf-8") as archivo:
            for item in json.load(archivo):
                jornada = str(item.get("jornada_reserva", "")).strip().capitalize()
                jornada = JORNADAS.get(jornada, jornada)
                dia = str(item.get("dia_reserva", "")).strip().lower()
                estado = item.get("estado_reserva")
                if (
                    item.get("incompleta")
                    or dia not in DIAS
                    or jornada not in NOMBRES_JORNADA
                    or not isinstance(estado, bool)
                ):
                    item["incompleta"] = True
                    reservas_incompletas.append(item)
                    continue

                datos_cliente = item["cliente"]
                cliente = next(
                    (c for c in clientes if c.get_id_cliente() == datos_cliente["id"]),
                    None,
                )
                if cliente is None:
                    cliente = Cliente(
                        datos_cliente["id"],
                        datos_cliente["nombre"],
                        datos_cliente["telefono"],
                    )
                    clientes.append(cliente)

                datos_mesa = item["mesa"]
                mesa = next(
                    (m for m in MESAS if m.get_id_mesa() == datos_mesa["id"]),
                    None,
                )
                if mesa is not None:
                    reservas.append(
                        Reserva(
                            item["id_reserva"],
                            cliente,
                            mesa,
                            jornada,
                            estado,
                            dia,
                        )
                    )
    except FileNotFoundError:
        pass
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        messagebox.showerror("Error", f"No se pudieron leer las reservas:\n{error}")
    return clientes, reservas, reservas_incompletas


def guardar_clientes(clientes):
    datos = [
        {
            "id": cliente.get_id_cliente(),
            "nombre": cliente.get_nombre_cliente(),
            "telefono": cliente.get_tel_cliente(),
        }
        for cliente in clientes
    ]
    with ARCHIVO_CLIENTES.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def guardar_reservas(reservas, reservas_incompletas):
    datos = [
        {
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
        for reserva in reservas
    ] + reservas_incompletas
    with ARCHIVO_RESERVAS.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def main():
    root = tk.Tk()
    root.title("Vino & Canela - Gestión del restaurante")
    root.geometry("1200x850")
    root.minsize(900, 650)
    clientes, reservas, reservas_incompletas = cargar_datos()
    if reservas_incompletas:
        messagebox.showwarning(
            "Reservas incompletas",
            f"Se encontraron {len(reservas_incompletas)} reservas sin día, "
            "jornada o estado válido. No se muestran entre las reservas válidas "
            "y se conservarán en el archivo JSON.",
        )

    contenedor = ttk.Frame(root)
    contenedor.pack(fill="both", expand=True)
    vista = tk.Canvas(contenedor, highlightthickness=0)
    barra = ttk.Scrollbar(contenedor, orient="vertical", command=vista.yview)
    vista.configure(yscrollcommand=barra.set)
    barra.pack(side="right", fill="y")
    vista.pack(side="left", fill="both", expand=True)
    secciones = ttk.Frame(vista, padding=10)
    ventana_secciones = vista.create_window((0, 0), window=secciones, anchor="nw")

    def ajustar_contenido(event):
        vista.itemconfigure(ventana_secciones, width=event.width)
        vista.configure(scrollregion=vista.bbox("all"))

    secciones.bind("<Configure>", lambda _event: vista.configure(scrollregion=vista.bbox("all")))
    vista.bind("<Configure>", ajustar_contenido)

    seccion_clientes = ttk.LabelFrame(secciones, text="Clientes", padding=8)
    seccion_mesas = ttk.LabelFrame(secciones, text="Mesas", padding=8)
    seccion_reservas = ttk.LabelFrame(secciones, text="Reservas", padding=8)
    seccion_clientes.pack(fill="x", pady=(0, 8))
    seccion_mesas.pack(fill="x", pady=(0, 8))
    seccion_reservas.pack(fill="x")

    def crear_tabla(parent, columnas, titulos):
        tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=7)
        for columna, titulo in zip(columnas, titulos):
            tabla.heading(columna, text=titulo)
            tabla.column(columna, width=140, anchor="center")
        tabla.pack(fill="both", expand=True, pady=8)
        return tabla

    # Clientes
    tabla_clientes = crear_tabla(
        seccion_clientes, ("id", "nombre", "telefono"),
        ("Código cliente", "Nombre", "Teléfono"),
    )
    datos_cliente = ttk.LabelFrame(seccion_clientes, text="Registrar / consultar", padding=8)
    datos_cliente.pack(fill="x")
    nombre_var = tk.StringVar()
    telefono_var = tk.StringVar()
    ttk.Label(datos_cliente, text="Nombre").grid(row=0, column=0, sticky="w")
    ttk.Entry(datos_cliente, textvariable=nombre_var, width=28).grid(row=1, column=0, padx=(0, 8))
    ttk.Label(datos_cliente, text="Teléfono").grid(row=0, column=1, sticky="w")
    ttk.Entry(datos_cliente, textvariable=telefono_var, width=18).grid(row=1, column=1, padx=(0, 8))

    consulta_id_var = tk.StringVar()
    telefono_nuevo_var = tk.StringVar()
    ttk.Label(datos_cliente, text="Buscar / modificar por código").grid(row=0, column=2, sticky="w")
    ttk.Entry(datos_cliente, textvariable=consulta_id_var, width=18).grid(row=1, column=2, padx=(0, 8))
    ttk.Label(datos_cliente, text="Nuevo teléfono").grid(row=0, column=3, sticky="w")
    ttk.Entry(datos_cliente, textvariable=telefono_nuevo_var, width=18).grid(row=1, column=3, padx=(0, 8))

    def actualizar_clientes():
        tabla_clientes.delete(*tabla_clientes.get_children())
        for cliente in clientes:
            tabla_clientes.insert(
                "", "end",
                values=(
                    cliente.get_id_cliente(),
                    cliente.get_nombre_cliente(),
                    cliente.get_tel_cliente(),
                ),
            )
        opciones_cliente["values"] = [
            f"{cliente.get_id_cliente()} | {cliente.get_nombre_cliente()}"
            for cliente in clientes
        ]

    def registrar_cliente():
        nombre = nombre_var.get().strip()
        telefono = telefono_var.get().strip()
        if len(nombre) < 3 or nombre.isnumeric():
            messagebox.showwarning("Dato inválido", "Ingresa un nombre de al menos 3 caracteres.")
            return
        if not telefono.isnumeric() or len(telefono) != 10:
            messagebox.showwarning("Dato inválido", "El teléfono debe tener 10 dígitos.")
            return
        clientes.append(Cliente(generador_ID_cliente(clientes), nombre, telefono))
        try:
            guardar_clientes(clientes)
        except OSError as error:
            clientes.pop()
            messagebox.showerror("Error al guardar", str(error))
            return
        nombre_var.set("")
        telefono_var.set("")
        actualizar_clientes()

    def consultar_cliente():
        codigo = consulta_id_var.get().strip().upper()
        cliente = next((c for c in clientes if c.get_id_cliente() == codigo), None)
        if cliente is None:
            messagebox.showinfo("Búsqueda", "No se encontró ese cliente.")
        else:
            messagebox.showinfo("Cliente", cliente.obtener_informacion())

    def modificar_cliente():
        codigo = consulta_id_var.get().strip().upper()
        cliente = next((c for c in clientes if c.get_id_cliente() == codigo), None)
        telefono = telefono_nuevo_var.get().strip()
        if cliente is None:
            messagebox.showwarning("Búsqueda", "No se encontró ese cliente.")
            return
        if not telefono.isnumeric() or len(telefono) != 10:
            messagebox.showwarning("Dato inválido", "El teléfono debe tener 10 dígitos.")
            return
        cliente.tel_cliente = telefono
        guardar_clientes(clientes)
        telefono_nuevo_var.set("")
        actualizar_clientes()

    ttk.Button(datos_cliente, text="Registrar", command=registrar_cliente).grid(row=1, column=4, padx=4)
    ttk.Button(datos_cliente, text="Consultar", command=consultar_cliente).grid(row=1, column=5, padx=4)
    ttk.Button(datos_cliente, text="Modificar teléfono", command=modificar_cliente).grid(row=1, column=6, padx=4)

    # Mesas
    cap_var = tk.StringVar()
    ttk.Label(seccion_mesas, text="Capacidad mínima").pack(anchor="w")
    fila_mesas = ttk.Frame(seccion_mesas)
    fila_mesas.pack(fill="x")
    ttk.Entry(fila_mesas, textvariable=cap_var, width=12).pack(side="left")
    tabla_mesas = crear_tabla(
        seccion_mesas, ("id", "capacidad", "ubicacion"),
        ("Código mesa", "Capacidad", "Ubicación"),
    )

    def mostrar_mesas(lista):
        tabla_mesas.delete(*tabla_mesas.get_children())
        for mesa in lista:
            tabla_mesas.insert(
                "", "end",
                values=(
                    mesa.get_id_mesa(),
                    mesa.get_capacidad_mesa(),
                    mesa.get_ubicacion_mesa(),
                ),
            )

    def filtrar_mesas():
        try:
            capacidad = int(cap_var.get())
        except ValueError:
            messagebox.showwarning("Dato inválido", "Escribe una capacidad numérica.")
            return
        mostrar_mesas([m for m in MESAS if m.get_capacidad_mesa() >= capacidad])

    ttk.Button(fila_mesas, text="Buscar", command=filtrar_mesas).pack(side="left", padx=6)
    ttk.Button(fila_mesas, text="Mostrar todas", command=lambda: mostrar_mesas(MESAS)).pack(side="left")

    # Reservas
    formulario = ttk.LabelFrame(seccion_reservas, text="Registrar reserva", padding=8)
    formulario.pack(fill="x")
    cliente_var = tk.StringVar()
    dia_var = tk.StringVar(value=DIAS[0].capitalize())
    jornada_var = tk.StringVar(value="Almuerzo")
    mesa_id_var = tk.StringVar()
    ttk.Label(formulario, text="Cliente").grid(row=0, column=0, sticky="w")
    opciones_cliente = ttk.Combobox(formulario, textvariable=cliente_var, state="readonly", width=27)
    opciones_cliente.grid(row=1, column=0, padx=(0, 8))
    ttk.Label(formulario, text="Día").grid(row=0, column=1, sticky="w")
    dia_box = ttk.Combobox(
        formulario, textvariable=dia_var,
        values=[dia.capitalize() for dia in DIAS], state="readonly", width=15,
    )
    dia_box.grid(row=1, column=1, padx=(0, 8))
    ttk.Label(formulario, text="Jornada").grid(row=0, column=2, sticky="w")
    jornada_box = ttk.Combobox(
        formulario, textvariable=jornada_var, values=list(JORNADAS),
        state="readonly", width=15,
    )
    jornada_box.grid(row=1, column=2, padx=(0, 8))
    ttk.Label(formulario, text="ID de mesa").grid(row=0, column=3, sticky="w")
    ttk.Entry(formulario, textvariable=mesa_id_var, width=15).grid(row=1, column=3, padx=(0, 8))

    mapa_frame = ttk.Frame(seccion_reservas)
    mapa_frame.pack(fill="both", expand=True, pady=8)
    mapa = tk.Canvas(
        mapa_frame, width=720, height=537,
        highlightthickness=0, scrollregion=(0, 0, 720, 537),
    )
    mapa.pack(anchor="w")
    imagen_mapa = tk.PhotoImage(file=str(CARPETA / "MAPA_MESAS_GUI.png"))
    imagen_aviso = tk.PhotoImage(file=str(CARPETA / "AVISO_GUI.png"))
    mapa.create_image(0, 0, image=imagen_mapa, anchor="nw")
    estado_var = tk.StringVar(value="Elige cliente, día, jornada e ingresa el ID de mesa.")
    ttk.Label(seccion_reservas, textvariable=estado_var).pack(anchor="w")

    def reserva_activa(mesa):
        return any(
            r.esta_activa()
            and r.get_mesa().get_id_mesa() == mesa.get_id_mesa()
            and r.get_dia_reserva().lower() == dia_var.get().lower()
            and r.get_jornada_reserva() == JORNADAS[jornada_var.get()]
            for r in reservas
        )

    def actualizar_mapa(_event=None):
        mapa.delete("marcadores")
        mesa_id_var.set("")
        for mesa in MESAS:
            x, y = POSICIONES_MESAS[mesa.get_id_mesa()]
            x, y = int(x * 720 / 960), int(y * 537 / 717)
            if reserva_activa(mesa):
                mapa.create_image(x, y, image=imagen_aviso, tags="marcadores")
            else:
                mapa.create_text(
                    x, y, text=mesa.get_id_mesa(), fill="#342319",
                    font=("", 10, "bold"), tags="marcadores",
                )

    def registrar_reserva():
        cliente = next(
            (c for c in clientes if cliente_var.get().startswith(c.get_id_cliente())),
            None,
        )
        if cliente is None:
            messagebox.showwarning("Falta cliente", "Selecciona un cliente.")
            return
        id_mesa = mesa_id_var.get().strip().upper()
        mesa = next((m for m in MESAS if m.get_id_mesa() == id_mesa), None)
        if mesa is None:
            messagebox.showwarning("Mesa inválida", "Escribe un ID de mesa válido, por ejemplo M001.")
            return
        if reserva_activa(mesa):
            messagebox.showwarning("Mesa reservada", "Esa mesa ya está reservada para ese día y jornada.")
            return

        reserva = Reserva(
            Reserva.generador_ID_reserva(reservas),
            cliente,
            mesa,
            JORNADAS[jornada_var.get()],
            True,
            dia_var.get().lower(),
        )
        reservas.append(reserva)
        try:
            guardar_reservas(reservas, reservas_incompletas)
        except OSError as error:
            reservas.pop()
            messagebox.showerror("Error al guardar", str(error))
            return
        estado_var.set(f"Reserva {reserva.get_id_reserva()} registrada.")
        actualizar_reservas()
        actualizar_mapa()

    ttk.Button(formulario, text="Registrar reserva", command=registrar_reserva).grid(row=1, column=4)
    dia_box.bind("<<ComboboxSelected>>", actualizar_mapa)
    jornada_box.bind("<<ComboboxSelected>>", actualizar_mapa)

    acciones = ttk.LabelFrame(seccion_reservas, text="Buscar o cancelar reserva", padding=8)
    acciones.pack(fill="x")
    buscar_mesa_var = tk.StringVar()
    buscar_cliente_var = tk.StringVar()
    buscar_dia_var = tk.StringVar(value=DIAS[0].capitalize())
    buscar_jornada_var = tk.StringVar(value="Almuerzo")
    cancelar_var = tk.StringVar()
    ttk.Label(acciones, text="ID mesa").grid(row=0, column=0)
    ttk.Entry(acciones, textvariable=buscar_mesa_var, width=12).grid(row=1, column=0, padx=4)
    ttk.Label(acciones, text="ID cliente").grid(row=0, column=1)
    ttk.Entry(acciones, textvariable=buscar_cliente_var, width=12).grid(row=1, column=1, padx=4)
    ttk.Label(acciones, text="Día").grid(row=0, column=2)
    ttk.Combobox(
        acciones, textvariable=buscar_dia_var, values=[d.capitalize() for d in DIAS],
        state="readonly", width=13,
    ).grid(row=1, column=2, padx=4)
    ttk.Label(acciones, text="Jornada").grid(row=0, column=3)
    ttk.Combobox(
        acciones, textvariable=buscar_jornada_var, values=list(JORNADAS),
        state="readonly", width=13,
    ).grid(row=1, column=3, padx=4)
    ttk.Label(acciones, text="ID reserva para cancelar").grid(row=0, column=4)
    ttk.Entry(acciones, textvariable=cancelar_var, width=15).grid(row=1, column=4, padx=4)

    tabla_reservas = crear_tabla(
        seccion_reservas,
        ("reserva", "cliente", "nombre", "mesa", "dia", "jornada", "estado"),
        ("Código reserva", "Código cliente", "Nombre", "Código mesa", "Día", "Jornada", "Estado"),
    )
    tabla_reservas.configure(height=6)

    def actualizar_reservas(lista=None):
        tabla_reservas.delete(*tabla_reservas.get_children())
        reservas_mostradas = reservas if lista is None else lista
        for reserva in reservas_mostradas:
            tabla_reservas.insert(
                "", "end",
                values=(
                    reserva.get_id_reserva(),
                    reserva.get_cliente().get_id_cliente(),
                    reserva.get_cliente().get_nombre_cliente(),
                    reserva.get_mesa().get_id_mesa(),
                    reserva.get_dia_reserva().capitalize(),
                    NOMBRES_JORNADA.get(
                        reserva.get_jornada_reserva(),
                        reserva.get_jornada_reserva(),
                    ),
                    "Activa" if reserva.esta_activa() else "Cancelada",
                ),
            )

    def buscar_reservas():
        id_mesa = buscar_mesa_var.get().strip().upper()
        id_cliente = buscar_cliente_var.get().strip().upper()
        dia = buscar_dia_var.get().lower()
        jornada = JORNADAS[buscar_jornada_var.get()]
        encontrados = [
            r for r in reservas
            if r.get_dia_reserva().lower() == dia
            and r.get_jornada_reserva() == jornada
            and (not id_mesa or r.get_mesa().get_id_mesa() == id_mesa)
            and (not id_cliente or r.get_cliente().get_id_cliente() == id_cliente)
        ]
        actualizar_reservas(encontrados)

    def cancelar_reserva():
        codigo = cancelar_var.get().strip().upper()
        reserva = next((r for r in reservas if r.get_id_reserva() == codigo), None)
        if reserva is None:
            messagebox.showwarning("Reserva", "No se encontró ese código de reserva.")
            return
        reserva.cancelar_reserva()
        try:
            guardar_reservas(reservas, reservas_incompletas)
        except OSError as error:
            messagebox.showerror("Error al guardar", str(error))
            return
        actualizar_reservas()
        actualizar_mapa()

    ttk.Button(acciones, text="Buscar", command=buscar_reservas).grid(row=1, column=5, padx=4)
    ttk.Button(acciones, text="Mostrar todas", command=actualizar_reservas).grid(row=1, column=6, padx=4)
    ttk.Button(acciones, text="Cancelar", command=cancelar_reserva).grid(row=1, column=7, padx=4)

    actualizar_clientes()
    mostrar_mesas(MESAS)
    actualizar_reservas()
    actualizar_mapa()
    root.mainloop()


if __name__ == "__main__":
    main()
