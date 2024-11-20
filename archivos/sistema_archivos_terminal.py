class SistemaArchivos:
    def __init__(self):
        self.estructura = {"root": {}}  # Árbol de directorios inicial
        self.directorio_actual = self.estructura["root"]  # Directorio donde el usuario está
        self.ruta_actual = "/root"  # Ruta textual del directorio actual

    def mkdir(self, nombre):
        if nombre in self.directorio_actual:
            print(f"Error: El directorio '{nombre}' ya existe.")
        else:
            self.directorio_actual[nombre] = {}
            print(f"Directorio '{nombre}' creado.")

    def ls(self):
        print("Contenido del directorio actual:")
        for item in self.directorio_actual:
            if isinstance(self.directorio_actual[item], dict):
                print(f"[DIR] {item}")
            else:
                print(f"[FILE] {item}")

    def touch(self, nombre):
        if nombre in self.directorio_actual:
            print(f"Error: '{nombre}' ya existe.")
        else:
            self.directorio_actual[nombre] = ""  # Los archivos inician vacíos
            print(f"Archivo '{nombre}' creado.")

    def rm(self, nombre):
        if nombre not in self.directorio_actual:
            print(f"Error: '{nombre}' no existe.")
        else:
            del self.directorio_actual[nombre]
            print(f"'{nombre}' eliminado.")

    def escribir_archivo(self, nombre, contenido):
        if nombre not in self.directorio_actual or isinstance(self.directorio_actual[nombre], dict):
            print(f"Error: '{nombre}' no es un archivo válido.")
        else:
            self.directorio_actual[nombre] += contenido
            print(f"Contenido agregado al archivo '{nombre}'.")

    def leer_archivo(self, nombre):
        if nombre not in self.directorio_actual or isinstance(self.directorio_actual[nombre], dict):
            print(f"Error: '{nombre}' no es un archivo válido.")
        else:
            print(f"Contenido del archivo '{nombre}':")
            print(self.directorio_actual[nombre])

    def cd(self, nombre):
        if nombre == "..":
            if self.ruta_actual != "/root":
                self.ruta_actual = "/".join(self.ruta_actual.split("/")[:-1]) or "/root"
                self.directorio_actual = self._navegar_a_ruta(self.ruta_actual)
            else:
                print("Ya estás en el directorio raíz.")
        elif nombre in self.directorio_actual and isinstance(self.directorio_actual[nombre], dict):
            self.directorio_actual = self.directorio_actual[nombre]
            self.ruta_actual = f"{self.ruta_actual}/{nombre}"
        else:
            print(f"El directorio '{nombre}' no existe.")

    def pwd(self):
        print(f"Directorio actual: {self.ruta_actual}")

    def clear(self):
        print("\033[H\033[J", end="")  # Limpia la pantalla

    def _navegar_a_ruta(self, ruta):
        partes = ruta.split("/")[1:]  # Quita la raíz vacía
        actual = self.estructura["root"]
        for parte in partes:
            actual = actual[parte]
        return actual

    def simular_terminal(self):
        print("Simulación de terminal activa. Escribe 'exit' para salir.")
        print("Comandos disponibles: mkdir, ls, touch, rm, pwd, cd, clear, read, write")
        while True:
            try:
                comando = input(f"{self.ruta_actual}$ ").strip()
                if comando == "exit":
                    print("Saliendo de la terminal.")
                    break
                elif comando.startswith("mkdir "):
                    nombre = comando[6:].strip()
                    self.mkdir(nombre)
                elif comando == "ls":
                    self.ls()
                elif comando.startswith("touch "):
                    nombre = comando[6:].strip()
                    self.touch(nombre)
                elif comando.startswith("rm "):
                    nombre = comando[3:].strip()
                    self.rm(nombre)
                elif comando == "pwd":
                    self.pwd()
                elif comando.startswith("cd "):
                    nombre = comando[3:].strip()
                    self.cd(nombre)
                elif comando == "clear":
                    self.clear()
                elif comando.startswith("write "):
                    partes = comando.split(" ", 2)
                    if len(partes) < 3:
                        print("Uso: write <archivo> <contenido>")
                    else:
                        nombre = partes[1]
                        contenido = partes[2]
                        self.escribir_archivo(nombre, contenido)
                elif comando.startswith("read "):
                    nombre = comando[5:].strip()
                    self.leer_archivo(nombre)
                else:
                    print(f"Comando no reconocido: {comando}")
            except Exception as e:
                print(f"Error: {e}")
