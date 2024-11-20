from planificacion.fifo import PlanificadorFIFO
from planificacion.round_robin import PlanificadorRoundRobin
from planificacion.sjf import PlanificadorSJF
from memoria.paginacion import Memoria
from archivos.sistema_archivos_terminal import SistemaArchivos


def solicitar_entero(mensaje):
    """Solicita un número entero al usuario y valida la entrada."""
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Por favor, ingrese un número entero válido.")


def menu_planificacion():
    """Módulo para Planificación de Procesos."""
    print("\nSeleccione el algoritmo de planificación:")
    print("1. FIFO (First In First Out)")
    print("2. Round Robin")
    print("3. SJF (Shortest Job First)")
    alg = solicitar_entero("Seleccione una opción: ")

    if alg == 1:
        planificador = PlanificadorFIFO()
    elif alg == 2:
        quantum = solicitar_entero("Ingrese el quantum para Round Robin: ")
        planificador = PlanificadorRoundRobin(quantum)
    elif alg == 3:
        planificador = PlanificadorSJF()
    else:
        print("Algoritmo no válido. Volviendo al menú principal.")
        return

    num_procesos = solicitar_entero("Ingrese el número de procesos: ")
    for i in range(num_procesos):
        print(f"Configurando proceso {i + 1} de {num_procesos}")
        pid = input("ID del proceso: ").strip()
        while not pid:
            print("El ID del proceso no puede estar vacío.")
            pid = input("ID del proceso: ").strip()

        tiempo = solicitar_entero(f"Tiempo de ejecución del proceso {pid}: ")
        prioridad = solicitar_entero(f"Prioridad del proceso {pid}: ")
        planificador.agregar_proceso({'id': pid, 'tiempo': tiempo, 'prioridad': prioridad})

    print("\nEjecución del algoritmo seleccionado:")
    planificador.ejecutar()


def menu_memoria():
    """Módulo para Administración de Memoria."""
    print("\nSeleccione el algoritmo de reemplazo de páginas:")
    print("1. FIFO")
    print("2. LRU (Least Recently Used)")
    alg = solicitar_entero("Seleccione una opción: ")

    if alg == 1:
        algoritmo = "FIFO"
    elif alg == 2:
        algoritmo = "LRU"
    else:
        print("Opción no válida. Volviendo al menú principal.")
        return

    tamanio_memoria = solicitar_entero("Ingrese el tamaño de la memoria (en bloques): ")
    memoria = Memoria(tamanio_memoria)

    num_paginas = solicitar_entero("Ingrese el número de páginas a cargar: ")
    for i in range(num_paginas):
        pagina_id = solicitar_entero(f"Ingrese el ID de la página {i + 1}: ")
        memoria.cargar_pagina(pagina_id, algoritmo)

    memoria.mostrar_estado()


def menu_archivos():
    """Módulo para Sistema de Archivos."""
    sistema = SistemaArchivos()
    sistema.simular_terminal()


def main():
    """Menú principal del programa."""
    while True:
        print("\nBienvenido al Simulador de Sistema Operativo")
        print("1. Planificación de Procesos")
        print("2. Administración de Memoria")
        print("3. Sistema de Archivos")
        print("4. Salir")
        
        opcion = solicitar_entero("Seleccione una opción: ")

        if opcion == 1:
            menu_planificacion()
        elif opcion == 2:
            menu_memoria()
        elif opcion == 3:
            menu_archivos()
        elif opcion == 4:
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    main()
