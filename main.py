from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog, QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QMessageBox, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
from planificacion.fifo import PlanificadorFIFO
from planificacion.round_robin import PlanificadorRoundRobin
from planificacion.sjf import PlanificadorSJF
from memoria.paginacion import Memoria
from archivos.sistema_archivos_terminal import SistemaArchivos


class SimuladorSO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Sistema Operativo")
        self.setGeometry(100, 100, 800, 600)

        # Configuración del estilo general
        self.setStyleSheet("background-color: #FFF8DC;")

        # Crear contenedor principal
        container = QWidget()
        layout = QVBoxLayout()

        # Etiqueta principal (Título)
        title_label = QLabel("Simulador de Sistema Operativo")
        title_label.setFont(QFont("Arial", 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #FF8C00;")
        layout.addWidget(title_label)

        # Botones principales
        btn_planificacion = QPushButton("Planificación de Procesos")
        btn_planificacion.setFixedSize(300, 60)
        btn_planificacion.setStyleSheet("""
            background-color: #FFD700;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
        """)
        btn_planificacion.clicked.connect(self.menu_planificacion)
        layout.addWidget(btn_planificacion, alignment=Qt.AlignCenter)

        btn_memoria = QPushButton("Administración de Memoria")
        btn_memoria.setFixedSize(300, 60)
        btn_memoria.setStyleSheet("""
            background-color: #FFA500;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
        """)
        btn_memoria.clicked.connect(self.menu_memoria)
        layout.addWidget(btn_memoria, alignment=Qt.AlignCenter)

        btn_archivos = QPushButton("Sistema de Archivos")
        btn_archivos.setFixedSize(300, 60)
        btn_archivos.setStyleSheet("""
            background-color: #FF4500;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
            color: white;
        """)
        btn_archivos.clicked.connect(self.menu_archivos)
        layout.addWidget(btn_archivos, alignment=Qt.AlignCenter)

        btn_salir = QPushButton("Salir")
        btn_salir.setFixedSize(300, 60)
        btn_salir.setStyleSheet("""
            background-color: #CD5C5C;
            border-radius: 30px;
            font-size: 18px;
            font-weight: bold;
            color: white;
        """)
        btn_salir.clicked.connect(self.close)
        layout.addWidget(btn_salir, alignment=Qt.AlignCenter)

        # Configurar el layout principal
        container.setLayout(layout)
        self.setCentralWidget(container)

    def menu_planificacion(self):
        """Muestra el menú para Planificación de Procesos."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Planificación de Procesos")
        dialog.setGeometry(200, 200, 400, 400)
        dialog.setStyleSheet("background-color: #FFD700;")

        layout = QVBoxLayout()

        # Selección de algoritmo
        label = QLabel("Seleccione el Algoritmo:")
        label.setFont(QFont("Arial", 14))
        layout.addWidget(label)

        combo_algoritmo = QComboBox()
        combo_algoritmo.addItems(["FIFO", "Round Robin", "SJF"])
        layout.addWidget(combo_algoritmo)

        # Botón para configurar procesos
        btn_configurar = QPushButton("Configurar Procesos")
        btn_configurar.setStyleSheet("background-color: #FFA500; border-radius: 10px; font-size: 14px;")
        btn_configurar.clicked.connect(lambda: self.configurar_procesos(combo_algoritmo.currentText()))
        layout.addWidget(btn_configurar)

        dialog.setLayout(layout)
        dialog.exec_()

    def configurar_procesos(self, algoritmo):
        """Configura y ejecuta los procesos según el algoritmo seleccionado."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Configurar Procesos - {algoritmo}")
        dialog.setGeometry(200, 200, 400, 400)
        dialog.setStyleSheet("background-color: #FFD700;")

        layout = QVBoxLayout()

        procesos = []

        # Configuración de cada proceso
        form_layout = QFormLayout()
        for i in range(3):  # Configuración de 3 procesos
            pid_input = QLineEdit()
            pid_input.setPlaceholderText(f"ID Proceso {i+1}")
            tiempo_input = QSpinBox()
            tiempo_input.setRange(1, 100)
            tiempo_input.setValue((i + 1) * 2)

            form_layout.addRow(f"Proceso {i+1}:", pid_input)
            form_layout.addRow("Tiempo:", tiempo_input)

            procesos.append((pid_input, tiempo_input))

        layout.addLayout(form_layout)

        # Botón para ejecutar el algoritmo
        btn_ejecutar = QPushButton("Ejecutar")
        btn_ejecutar.setStyleSheet("background-color: #FF8C00; border-radius: 10px; font-size: 14px;")
        btn_ejecutar.clicked.connect(lambda: self.ejecutar_planificacion(algoritmo, procesos))
        layout.addWidget(btn_ejecutar)

        dialog.setLayout(layout)
        dialog.exec_()

    def ejecutar_planificacion(self, algoritmo, procesos):
        """Ejecuta el algoritmo de planificación con los datos ingresados."""
        planificador = None

        if algoritmo == "FIFO":
            planificador = PlanificadorFIFO()
        elif algoritmo == "Round Robin":
            planificador = PlanificadorRoundRobin(quantum=2)
        elif algoritmo == "SJF":
            planificador = PlanificadorSJF()
        else:
            QMessageBox.warning(self, "Error", "Algoritmo no reconocido.")
            return

        for pid_input, tiempo_input in procesos:
            pid = pid_input.text()
            tiempo = tiempo_input.value()

            if pid.strip() == "":
                QMessageBox.warning(self, "Error", "Todos los procesos deben tener un ID válido.")
                return

            planificador.agregar_proceso({'id': pid, 'tiempo': tiempo, 'prioridad': 1})

        planificador.ejecutar()
        QMessageBox.information(self, "Éxito", "Planificación ejecutada correctamente.")

    def menu_memoria(self):
        """Muestra el menú para Administración de Memoria con tabla."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Administración de Memoria")
        dialog.setGeometry(200, 200, 600, 400)
        dialog.setStyleSheet("background-color: #FFF8DC;")

        layout = QVBoxLayout()

        # Tabla de memoria
        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Página", "Estado", "Algoritmo"])
        layout.addWidget(self.table)

        # Selección de algoritmo
        algoritmo_label = QLabel("Seleccione el Algoritmo:")
        algoritmo_label.setFont(QFont("Arial", 12))
        layout.addWidget(algoritmo_label)

        self.combo_algoritmo = QComboBox()
        self.combo_algoritmo.addItems(["FIFO", "LRU"])
        layout.addWidget(self.combo_algoritmo)

        # Botón para cargar páginas
        btn_cargar = QPushButton("Cargar Páginas")
        btn_cargar.setStyleSheet("background-color: #FF8C00; border-radius: 10px; font-size: 14px;")
        btn_cargar.clicked.connect(self.cargar_paginas)
        layout.addWidget(btn_cargar)

        dialog.setLayout(layout)
        dialog.exec_()

    def cargar_paginas(self):
        """Carga páginas en memoria y actualiza la tabla."""
        algoritmo = self.combo_algoritmo.currentText()
        memoria = Memoria(5)
        estado_paginas = []

        for i in range(1, 11):
            if algoritmo == "FIFO":
                memoria.cargar_pagina(i)
            elif algoritmo == "LRU":
                memoria.cargar_pagina_lru(i)

            estado_paginas.append({
                "pagina": i,
                "estado": "Cargada" if i in memoria.paginas else "Reemplazada",
                "algoritmo": algoritmo
            })

        self.actualizar_tabla(estado_paginas)

    def actualizar_tabla(self, estado_paginas):
        """Actualiza la tabla con el estado de las páginas."""
        self.table.clearContents()
        for i, pagina in enumerate(estado_paginas):
            self.table.setItem(i, 0, QTableWidgetItem(str(pagina["pagina"])))
            self.table.setItem(i, 1, QTableWidgetItem(pagina["estado"]))
            self.table.setItem(i, 2, QTableWidgetItem(pagina["algoritmo"]))

    def menu_archivos(self):
        """Muestra el menú para Sistema de Archivos."""
        sistema = SistemaArchivos()
        sistema.simular_terminal()


# Crear la aplicación
def main():
    app = QApplication(sys.argv)
    ventana = SimuladorSO()
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
