class Memoria:
    def __init__(self, tamano, algoritmo="FIFO"):
        self.tamano = tamano
        self.paginas = []
        self.algoritmo = algoritmo.upper()
        self.fallos_pagina = 0

    def cargar_pagina(self, pagina_id):
        if pagina_id in self.paginas:
            if self.algoritmo == "LRU":
                self.paginas.remove(pagina_id)
                self.paginas.append(pagina_id)
            print(f"Página {pagina_id} ya está en memoria.")
        else:
            self.fallos_pagina += 1
            if len(self.paginas) < self.tamano:
                self.paginas.append(pagina_id)
                print(f"Página {pagina_id} cargada en memoria.")
            else:
                if self.algoritmo == "FIFO":
                    eliminada = self.paginas.pop(0)
                    print(f"Página {eliminada} eliminada (FIFO).")
                elif self.algoritmo == "LRU":
                    eliminada = self.paginas.pop(0)
                    print(f"Página {eliminada} eliminada (LRU).")
                self.paginas.append(pagina_id)
                print(f"Página {pagina_id} cargada en memoria.")

    def mostrar_estado(self):
        print("Estado actual de la memoria:")
        print(self.paginas)
        print(f"Fallos de página hasta ahora: {self.fallos_pagina}")
