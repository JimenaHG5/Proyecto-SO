import matplotlib.pyplot as plt

class PlanificadorSJF:
    def __init__(self):
        self.procesos = []

    def agregar_proceso(self, proceso):
        self.procesos.append(proceso)

    def ejecutar(self):
        self.procesos.sort(key=lambda p: p['tiempo'])  # Ordenar por tiempo de ejecución
        tiempo_actual = 0
        tiempos_espera = []
        tiempos_retorno = []

        print("\nEjecución de SJF:")
        for proceso in self.procesos:
            print(f"Ejecutando proceso {proceso['id']}...")
            tiempo_espera = tiempo_actual
            tiempo_actual += proceso['tiempo']
            tiempo_retorno = tiempo_actual

            tiempos_espera.append(tiempo_espera)
            tiempos_retorno.append(tiempo_retorno)

            print(f"Proceso {proceso['id']}: Tiempo de espera = {tiempo_espera}, Tiempo de retorno = {tiempo_retorno}")

        tiempo_promedio_espera = sum(tiempos_espera) / len(self.procesos)
        tiempo_promedio_retorno = sum(tiempos_retorno) / len(self.procesos)
        print(f"\nTiempo promedio de espera: {tiempo_promedio_espera}")
        print(f"Tiempo promedio de retorno: {tiempo_promedio_retorno}")

        self.graficar_resultados(tiempos_espera, tiempos_retorno)

    def graficar_resultados(self, tiempos_espera, tiempos_retorno):
        ids = [proceso['id'] for proceso in self.procesos]
        plt.bar(ids, tiempos_espera, label='Tiempo de espera', alpha=0.7)
        plt.bar(ids, tiempos_retorno, label='Tiempo de retorno', alpha=0.7)
        plt.xlabel("Procesos")
        plt.ylabel("Tiempo")
        plt.title("SJF: Tiempo de espera y retorno por proceso")
        plt.legend()
        plt.show()
