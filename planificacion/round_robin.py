import matplotlib.pyplot as plt

class PlanificadorRoundRobin:
    def __init__(self, quantum):
        self.procesos = []
        self.quantum = quantum

    def agregar_proceso(self, proceso):
        """Agrega un proceso a la lista de procesos."""
        self.procesos.append({
            'id': proceso['id'],
            'tiempo': proceso['tiempo'],
            'prioridad': proceso['prioridad'],
            'tiempo_restante': proceso['tiempo']
        })

    def ejecutar(self):
        """Ejecuta los procesos utilizando el algoritmo Round Robin."""
        cola = self.procesos[:]  # Copia de la lista de procesos
        tiempo_actual = 0
        tiempos_espera = {proceso['id']: 0 for proceso in self.procesos}
        tiempos_retorno = {}

        print("\nEjecución de Round Robin:")
        while cola:
            proceso = cola.pop(0)  # Extraer el proceso actual
            if proceso['tiempo_restante'] > 0:  # Validar si aún requiere tiempo
                print(f"Ejecutando proceso {proceso['id']}...")
                if proceso['tiempo_restante'] > self.quantum:
                    tiempo_actual += self.quantum
                    proceso['tiempo_restante'] -= self.quantum
                    cola.append(proceso)  # Reagregar a la cola
                else:
                    tiempo_actual += proceso['tiempo_restante']
                    proceso['tiempo_restante'] = 0
                    tiempos_retorno[proceso['id']] = tiempo_actual

        # Calcular tiempos de espera
        for proceso in self.procesos:
            tiempos_espera[proceso['id']] = (
                tiempos_retorno[proceso['id']] - proceso['tiempo']
            )

        # Mostrar resultados
        self.mostrar_estadisticas(tiempos_espera, tiempos_retorno)
        self.graficar_resultados(tiempos_espera, tiempos_retorno)

    def mostrar_estadisticas(self, tiempos_espera, tiempos_retorno):
        """Muestra estadísticas de tiempos de espera y retorno."""
        print("\nEstadísticas:")
        tiempo_promedio_espera = sum(tiempos_espera.values()) / len(self.procesos)
        tiempo_promedio_retorno = sum(tiempos_retorno.values()) / len(self.procesos)
        print(f"Tiempo promedio de espera: {tiempo_promedio_espera}")
        print(f"Tiempo promedio de retorno: {tiempo_promedio_retorno}")

    def graficar_resultados(self, tiempos_espera, tiempos_retorno):
        """Genera una gráfica de los tiempos de espera y retorno."""
        ids = [proceso['id'] for proceso in self.procesos]
        espera = [tiempos_espera[pid] for pid in ids]
        retorno = [tiempos_retorno[pid] for pid in ids]

        plt.bar(ids, espera, label='Tiempo de espera', alpha=0.7)
        plt.bar(ids, retorno, label='Tiempo de retorno', alpha=0.7, bottom=espera)
        plt.xlabel("Procesos")
        plt.ylabel("Tiempo")
        plt.title("Round Robin: Tiempo de espera y retorno por proceso")
        plt.legend()
        plt.show()
