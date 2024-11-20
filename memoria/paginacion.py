class Memoria:
    def __init__(self, tamanio):
        """Inicializa la memoria con un tamaño fijo."""
        self.tamanio = tamanio
        self.bloques = []  # Representa los bloques de memoria
        self.uso_reciente = []  # Para LRU

    def cargar_pagina(self, pagina_id, algoritmo):
        """Carga una página en memoria usando el algoritmo indicado."""
        if pagina_id in self.bloques:
            print(f"Página {pagina_id} ya está cargada en memoria.")
            if algoritmo == "LRU":
                # Actualiza la lista de uso reciente para LRU
                self.uso_reciente.remove(pagina_id)
                self.uso_reciente.append(pagina_id)
            return

        # Si hay espacio disponible
        if len(self.bloques) < self.tamanio:
            self.bloques.append(pagina_id)
            print(f"Página {pagina_id} cargada en memoria.")
            if algoritmo == "LRU":
                self.uso_reciente.append(pagina_id)
        else:
            # Memoria llena, aplicar algoritmo de reemplazo
            if algoritmo == "FIFO":
                reemplazada = self.bloques.pop(0)
            elif algoritmo == "LRU":
                reemplazada = self.uso_reciente.pop(0)
                self.bloques.remove(reemplazada)
            print(f"Página {reemplazada} reemplazada por la página {pagina_id}.")
            self.bloques.append(pagina_id)
            if algoritmo == "LRU":
                self.uso_reciente.append(pagina_id)

    def mostrar_estado(self):
        """Muestra el estado actual de la memoria."""
        print("\nEstado actual de la memoria:")
        print(f"Bloques: {self.bloques}")
        if self.uso_reciente:
            print(f"Orden de uso reciente (LRU): {self.uso_reciente}")
        print("-" * 30)
