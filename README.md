# 🍷 PROYECTO_2-GESTION_VINO-CANELA-
**Sistema de Gestión de Reservas del restaurante Vino & Canela.**

¡Bienvenido al sistema de reservas del restaurante **Vino & Canela**! Este proyecto es una aplicación de escritorio interactiva desarrollada en Python para gestionar la asignación de 11 mesas (capacidad total de 40 personas) distribuidas en seis cómodas zonas, garantizando la eficiencia de clientes en tres jornadas de atención (Almuerzo, Tarde y Cena) y evitando completamente los sobrecupos o cruces de horarios.

La aplicación cuenta con una versión de consola (con menús y tablas) y una versión GUI (interfaz gráfica) que incorpora un mapa interactivo visual elegante, aplicando el paradigma de la **Programación Orientada a Objetos (POO)** y encapsulamiento para proteger la integridad de los datos.

---

## 🌟 Características Principales

* **Doble Interfaz de Usuario:**
  * **GUI (Interfaz Gráfica):** Ejecutable con Tkinter. Muestra la distribución real y, cuando una mesa está reservada en la jornada seleccionada, superpone automáticamente el aviso "MESA RESERVADA" sobre el plano.
  * **Consola:** Sistema tradicional de menús textuales con validaciones avanzadas y mostrado en tablas de forma ordenada.
* **Mapa de Mesas Interactivo:** Visualiza el espacio físico definido en 6 zonas (según el diseño artesanal): Ventana, Centro, Terraza, Barra, Patio y Salón.
* **Validaciones Robustas:** No permite reservar mesas ya asignadas en el mismo día y jornada, ni superar los límites de capacidad de cada mesa.
* **Persistencia JSON:** Los datos de clientes y reservas se guardan y cargan automáticamente desde los archivos `Cliente.json` y `Reserva.json`.
* **Generadores Automáticos de ID:** Creación de IDs únicos como `C001` o `R001` de forma automática sin intervención del usuario.

---

## 📋 Mesas y Capacidades (Catálogo)

El restaurante tiene una distribución diseñada específicamente para ofrecer experiencias acogedoras:

| Código Mesa | Capacidad | Ubicación |
| :--- | :--- | :--- |
| M001 | 2 | Ventana |
| M002 | 2 | Centro |
| M003 | 2 | Terraza |
| M004 | 2 | Barra |
| M005 | 2 | Patio |
| M006 | 4 | Ventana |
| M007 | 4 | Centro |
| M008 | 4 | Terraza |
| M009 | 6 | Barra |
| M010 | 6 | Patio |
| M011 | 8 | Salón |

---

## 🏗️ Infraestructura del Proyecto (POO)

* `cliente.py`: Define la clase `Cliente`, que guarda la ID, el nombre (privado) y el teléfono. Contiene métodos para obtener información y el generador de ID automático.
* `mesa.py`: Define la clase `Mesa`, con atributos privados para ID, capacidad, ubicación y estado. Permite leer la disponibilidad y capacidades.
* `reserva.py`: Define la clase `Reserva`, vinculada a los objetos `Cliente` y `Mesa`. Contiene el estado de la reserva (Activa/Cancelada), días, jornadas y el método de cancelación.
* `Intro_GUI_rest.py`: Responsable de la interfaz gráfica con `tkinter`, mapa interactivo visual, tablas `treeview`, y formularios de registro.
* `App_restaurante.py`: Responsable de la lógica de consola, guardado y carga JSON, y el flujo del menú principal.


---

## 🚀 Cómo Ejecutar el Programa

Abre una terminal en la raíz de la carpeta del proyecto y ejecuta uno de los siguientes comandos:
**Para ejecutar la Interfaz Gráfica (Recomendado):**
```bash
python Intro_GUI_rest.py

**Para ejecutar en el modo consola:**
```bash
python App_restaurante.py
