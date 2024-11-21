import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

procesos = []
memoria = None
quantum_rr = 1  # Valor por defecto del quantum para Round Robin
sistema_archivos = {"root": {}}  # Estructura base para el sistema de archivos
directorio_actual = "root"  # Directorio inicial


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
        else:
            self.fallos_pagina += 1
            if len(self.paginas) < self.tamano:
                self.paginas.append(pagina_id)
            else:
                if self.algoritmo == "FIFO":
                    self.paginas.pop(0)
                elif self.algoritmo == "LRU":
                    self.paginas.pop(0)
                self.paginas.append(pagina_id)


def mkdir(nombre):
    if nombre in sistema_archivos[directorio_actual]:
        print(f"Error: El directorio '{nombre}' ya existe.")
    else:
        sistema_archivos[directorio_actual][nombre] = {}
        print(f"Directorio '{nombre}' creado con éxito.")


def ls():
    contenido = sistema_archivos[directorio_actual]
    if contenido:
        print("Contenido del directorio:")
        for nombre in contenido:
            print(f"  - {nombre} {'(directorio)' if isinstance(contenido[nombre], dict) else '(archivo)'}")
    else:
        print("El directorio está vacío.")


def touch(nombre):
    if nombre in sistema_archivos[directorio_actual]:
        print(f"Error: El archivo o directorio '{nombre}' ya existe.")
    else:
        sistema_archivos[directorio_actual][nombre] = None
        print(f"Archivo '{nombre}' creado con éxito.")


def rm(nombre):
    if nombre in sistema_archivos[directorio_actual]:
        del sistema_archivos[directorio_actual][nombre]
        print(f"'{nombre}' eliminado con éxito.")
    else:
        print(f"Error: '{nombre}' no encontrado en el directorio actual.")


def calcular_estadisticas(procesos):
    tiempos_espera = []
    tiempos_retorno = []
    tiempo_acumulado = 0

    for proceso in procesos:
        tiempo_espera = tiempo_acumulado
        tiempo_retorno = tiempo_acumulado + proceso["tiempo"]
        tiempo_acumulado += proceso["tiempo"]
        tiempos_espera.append(tiempo_espera)
        tiempos_retorno.append(tiempo_retorno)

    promedio_espera = sum(tiempos_espera) / len(tiempos_espera)
    promedio_retorno = sum(tiempos_retorno) / len(tiempos_retorno)

    return tiempos_espera, tiempos_retorno, promedio_espera, promedio_retorno


def round_robin(procesos, quantum):
    orden_ejecucion = []
    cola = procesos[:]
    tiempos_restantes = {proceso["id"]: proceso["tiempo"] for proceso in procesos}

    while cola:
        proceso = cola.pop(0)
        pid = proceso["id"]
        tiempo_ejecucion = min(quantum, tiempos_restantes[pid])
        orden_ejecucion.append((pid, tiempo_ejecucion))
        tiempo_restante = tiempos_restantes[pid] - tiempo_ejecucion

        if tiempo_restante > 0:
            tiempos_restantes[pid] = tiempo_restante
            cola.append(proceso)

    return orden_ejecucion


def graficar_estadisticas(tiempos_espera, tiempos_retorno, algoritmo):
    x = range(len(tiempos_espera))
    fig, ax = plt.subplots()

    ax.bar(x, tiempos_espera, label="Tiempo de Espera")
    ax.bar(x, tiempos_retorno, bottom=tiempos_espera, label="Tiempo de Retorno")

    ax.set_xlabel("Procesos")
    ax.set_ylabel("Tiempo")
    ax.set_title(f"Tiempos de Espera y Retorno ({algoritmo})")
    ax.legend()

    plt.show()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistema Operativo")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f4f7")

        self.selected_algorithm = tk.StringVar(value="FIFO")
        self.initialize_menu()
        self.initialize_memory_config()

    def initialize_menu(self):
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="solid")
        frame.pack(pady=50, padx=50, fill="both", expand=True)

        title = tk.Label(
            frame,
            text="Simulador de Sistema Operativo",
            font=("Helvetica", 18, "bold"),
            bg="#ffffff",
            fg="#333333",
        )
        title.pack(pady=20)

        btn_planificacion = tk.Button(
            frame,
            text="Planificación de Procesos",
            font=("Helvetica", 14),
            command=self.planificacion_window,
            bg="#4caf50",
            fg="#ffffff",
            relief="flat",
        )
        btn_planificacion.pack(pady=10)

        btn_memoria = tk.Button(
            frame,
            text="Administración de Memoria",
            font=("Helvetica", 14),
            command=self.memoria_window,
            bg="#2196f3",
            fg="#ffffff",
            relief="flat",
        )
        btn_memoria.pack(pady=10)

        btn_archivos = tk.Button(
            frame,
            text="Sistema de Archivos",
            font=("Helvetica", 14),
            command=self.archivos_window,
            bg="#f44336",
            fg="#ffffff",
            relief="flat",
        )
        btn_archivos.pack(pady=10)

    def initialize_memory_config(self):
        global memoria
        memoria = Memoria(tamano=3, algoritmo="FIFO")

    def planificacion_window(self):
        plan_win = tk.Toplevel(self.root)
        plan_win.title("Planificación de Procesos")
        plan_win.geometry("600x500")
        plan_win.config(bg="#f0f4f7")

        def toggle_quantum_entry(event=None):
            if self.selected_algorithm.get() == "Round Robin":
                quantum_entry.config(state="normal")
            else:
                quantum_entry.config(state="disabled")

        def add_process():
            pid = pid_entry.get()
            tiempo = tiempo_entry.get()
            prioridad = prioridad_entry.get()
            if not pid or not tiempo or not prioridad:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            proceso = {"id": pid, "tiempo": int(tiempo), "prioridad": int(prioridad)}
            procesos.append(proceso)
            memoria.cargar_pagina(pid)
            messagebox.showinfo(
                "Éxito", f"Proceso {pid} añadido y cargado en memoria."
            )

        def execute_processes():
            algoritmo = self.selected_algorithm.get()
            global quantum_rr

            if algoritmo == "Round Robin":
                quantum_rr = int(quantum_entry.get())
                orden = round_robin(procesos, quantum_rr)
                tiempos_espera, tiempos_retorno, promedio_espera, promedio_retorno = calcular_estadisticas(procesos)
                messagebox.showinfo(
                    "Estadísticas",
                    f"Promedio de Espera: {promedio_espera}\nPromedio de Retorno: {promedio_retorno}",
                )
                graficar_estadisticas(tiempos_espera, tiempos_retorno, algoritmo)
            else:
                if algoritmo == "FIFO":
                    procesos.sort(key=lambda p: p["id"])
                elif algoritmo == "SJF":
                    procesos.sort(key=lambda p: p["tiempo"])
                tiempos_espera, tiempos_retorno, promedio_espera, promedio_retorno = calcular_estadisticas(procesos)
                messagebox.showinfo(
                    "Estadísticas",
                    f"Promedio de Espera: {promedio_espera}\nPromedio de Retorno: {promedio_retorno}",
                )
                graficar_estadisticas(tiempos_espera, tiempos_retorno, algoritmo)

        tk.Label(plan_win, text="ID del Proceso:", bg="#f0f4f7").pack()
        pid_entry = tk.Entry(plan_win)
        pid_entry.pack()

        tk.Label(plan_win, text="Tiempo:", bg="#f0f4f7").pack()
        tiempo_entry = tk.Entry(plan_win)
        tiempo_entry.pack()

        tk.Label(plan_win, text="Prioridad:", bg="#f0f4f7").pack()
        prioridad_entry = tk.Entry(plan_win)
        prioridad_entry.pack()

        tk.Label(plan_win, text="Algoritmo:", bg="#f0f4f7").pack()
        algo_menu = ttk.Combobox(
            plan_win,
            values=["FIFO", "SJF", "Round Robin"],
            textvariable=self.selected_algorithm,
        )
        algo_menu.pack()
        algo_menu.bind("<<ComboboxSelected>>", toggle_quantum_entry)

        tk.Label(plan_win, text="Quantum (Solo Round Robin):", bg="#f0f4f7").pack()
        quantum_entry = tk.Entry(plan_win, state="disabled")
        quantum_entry.pack()

        tk.Button(
            plan_win,
            text="Añadir Proceso",
            bg="#4caf50",
            fg="#ffffff",
            command=add_process,
        ).pack(pady=10)
        tk.Button(
            plan_win,
            text="Ejecutar Procesos",
            bg="#2196f3",
            fg="#ffffff",
            command=execute_processes,
        ).pack(pady=10)

    def memoria_window(self):
        mem_win = tk.Toplevel(self.root)
        mem_win.title("Administración de Memoria")
        mem_win.geometry("600x400")
        mem_win.config(bg="#f0f4f7")

        tk.Label(
            mem_win,
            text="Estado de la Memoria",
            font=("Helvetica", 16),
            bg="#f0f4f7",
        ).pack(pady=20)

        def update_memory_table():
            table.delete(*table.get_children())
            for idx, pagina in enumerate(memoria.paginas):
                table.insert("", "end", values=(idx + 1, pagina))

        cols = ("Bloque", "Página (Proceso)")
        table = ttk.Treeview(mem_win, columns=cols, show="headings", height=10)
        table.heading("Bloque", text="Bloque")
        table.heading("Página (Proceso)", text="Página (Proceso)")
        table.pack(pady=20)

        update_memory_table()

    def archivos_window(self):
        arch_win = tk.Toplevel(self.root)
        arch_win.title("Sistema de Archivos")
        arch_win.geometry("600x400")
        arch_win.config(bg="#f0f4f7")

        def ejecutar_comando():
            comando = entrada_comando.get().strip()
            if not comando:
                messagebox.showerror("Error", "Por favor, ingrese un comando.")
                return
            entrada_comando.delete(0, tk.END)

            comando_split = comando.split()
            cmd = comando_split[0]
            args = comando_split[1:]

            if cmd == "mkdir":
                if args:
                    mkdir(args[0])
                    salida.insert(tk.END, f"Directorio '{args[0]}' creado con éxito.\n")
                else:
                    salida.insert(tk.END, "Uso: mkdir <nombre_directorio>\n")
            elif cmd == "ls":
                salida.insert(tk.END, "Contenido del directorio actual:\n")
                contenido = sistema_archivos[directorio_actual]
                if contenido:
                    for nombre in contenido:
                        salida.insert(
                            tk.END,
                            f"  - {nombre} {'(directorio)' if isinstance(contenido[nombre], dict) else '(archivo)'}\n",
                        )
                else:
                    salida.insert(tk.END, "El directorio está vacío.\n")
            elif cmd == "touch":
                if args:
                    touch(args[0])
                    salida.insert(tk.END, f"Archivo '{args[0]}' creado con éxito.\n")
                else:
                    salida.insert(tk.END, "Uso: touch <nombre_archivo>\n")
            elif cmd == "rm":
                if args:
                    rm(args[0])
                    salida.insert(tk.END, f"'{args[0]}' eliminado con éxito.\n")
                else:
                    salida.insert(tk.END, "Uso: rm <nombre>\n")
            elif cmd == "help":
                salida.insert(
                    tk.END,
                    "Comandos disponibles:\n"
                    "  mkdir <nombre_directorio>  - Crear un directorio.\n"
                    "  ls                        - Listar contenido del directorio actual.\n"
                    "  touch <nombre_archivo>    - Crear un archivo.\n"
                    "  rm <nombre>               - Eliminar un archivo o directorio.\n"
                    "  exit                      - Cerrar esta ventana.\n",
                )
            elif cmd == "exit":
                arch_win.destroy()
            else:
                salida.insert(tk.END, f"Comando desconocido: {cmd}\n")

        salida = tk.Text(arch_win, height=15, width=70, state="normal")
        salida.pack(pady=10)

        entrada_comando = tk.Entry(arch_win, width=50)
        entrada_comando.pack(pady=5)

        btn_ejecutar = tk.Button(
            arch_win,
            text="Ejecutar Comando",
            bg="#4caf50",
            fg="#ffffff",
            command=ejecutar_comando,
        )
        btn_ejecutar.pack()

        btn_cerrar = tk.Button(
            arch_win,
            text="Cerrar",
            bg="#f44336",
            fg="#ffffff",
            command=arch_win.destroy,
        )
        btn_cerrar.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
