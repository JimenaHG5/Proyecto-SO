
# Simulador de Sistema Operativo Completo

Este proyecto simula un sistema operativo básico con las siguientes funcionalidades:

## Funcionalidades
1. **Planificación de Procesos**:
   - Algoritmos: FIFO, Round Robin, SJF.
   - Permite agregar procesos con tiempos y prioridades.

2. **Administración de Memoria**:
   - Simula un esquema básico de paginación.
   - Implementa algoritmos de reemplazo de páginas: FIFO y LRU.

3. **Sistema de Archivos**:
   - Simula una terminal con comandos básicos (`mkdir`, `ls`, `touch`, `rm`).

## Uso
1. Ejecuta el archivo `main.py`:
   ```bash
   python main.py
   ```

2. Selecciona una opción en el menú para interactuar con la funcionalidad correspondiente.

## Requisitos
- Python 3.x

## Ejemplo
- **Simulación de terminal**:
```bash
$ mkdir proyectos
$ touch notas.txt
$ ls
[DIR] proyectos
[FILE] notas.txt
$ rm notas.txt
$ ls
[DIR] proyectos
$ exit
Saliendo de la terminal.
```
