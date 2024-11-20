# Simulador de Sistema Operativo

Este proyecto es un simulador interactivo de sistema operativo diseñado para comprender conceptos fundamentales como la planificación de procesos, la administración de memoria y el manejo de archivos. Todo está integrado en una interfaz gráfica amigable desarrollada en Python con `tkinter`.

## Características

### 1. Planificación de Procesos
- Implementa algoritmos de planificación:
  - **FIFO (First In, First Out):** Procesos se ejecutan en el orden de llegada.
  - **SJF (Shortest Job First):** Procesos con menor tiempo de ejecución se ejecutan primero.
  - **Round Robin:** Procesos ejecutados en intervalos (quantum) específicos.
- Estadísticas:
  - Tiempo promedio de espera.
  - Tiempo promedio de retorno.
- Gráficas dinámicas:
  - Muestra tiempos de espera y retorno de los procesos.

### 2. Administración de Memoria
- Simula la carga de páginas en memoria con los algoritmos de reemplazo:
  - **FIFO:** Reemplaza la página más antigua.
  - **LRU (Least Recently Used):** Reemplaza la página menos utilizada recientemente.
- Visualiza el estado de la memoria.
- Cuenta el número de fallos de página.

### 3. Sistema de Archivos
- Comandos disponibles:
  - `mkdir <nombre>`: Crea un nuevo directorio.
  - `ls`: Lista el contenido del directorio actual.
  - `touch <nombre>`: Crea un archivo vacío.
  - `rm <nombre>`: Elimina un archivo o directorio.
  - `write <nombre> "texto"`: Escribe texto en un archivo.
  - `read <nombre>`: Lee el contenido de un archivo.
- Simula un sistema de archivos interactivo en un entorno gráfico.

## Requisitos

- Python 3.7 o superior.
- Bibliotecas necesarias:
  - `matplotlib`
  - `tkinter` (generalmente incluida con Python).

### Instalación

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone https://github.com/tu-usuario/simulador-sistema-operativo.git
