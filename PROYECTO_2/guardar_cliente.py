import json

from cliente import Cliente

lista_clientes = [
    Cliente("C001", "Juan Pérez", "3197401234"),
    Cliente("C002", "María García", "2094567890"),
    Cliente("C003", "Pedro López", "3094658721"),
]


def cliente_a_diccionario(Cliente):
    return {
        "id": Cliente.get_id_cliente(),
        "nombre": Cliente.get_nombre_cliente(),
        "telefono": Cliente.get_tel_cliente()
    }

def objetos_a_json(objetos_dict):
    with open("Cliente.json", "w", encoding="utf-8") as archivo:
        json.dump(objetos_dict, archivo, indent=4, ensure_ascii=False)

def main():
    ## Pasar una lista de objetos a una lista de diccionarios
    lista_clientes_dict = []
    for c in lista_clientes:
       lista_clientes_dict.append(cliente_a_diccionario(c))
    print("\n" + "=" * 42)
    print("           CLIENTES REGISTRADOS")
    print("=" * 42)
    for cliente_dict in lista_clientes_dict:
        print(f"\n  CLIENTE {cliente_dict['id']}")
        print("  " + "-" * 36)
        print(f"  Nombre:   {cliente_dict['nombre']}")
        print(f"  Teléfono: {cliente_dict['telefono']}")
    print("\n" + "=" * 42)

    #4
    # Pasar de una lista de diccionarios a un archivo JSON
    objetos_a_json(lista_clientes_dict)

if __name__ == "__main__":
    main()