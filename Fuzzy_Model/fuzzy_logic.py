import sys
import requests
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

# === Configuración de la API ===
API_KEY = '53a319025f3945729a8164157242210'
BASE_URL = "https://api.weatherapi.com/v1/current.json"


def obtener_datos_climaticos(ciudad):
    """
    Función para obtener los datos climáticos de una ciudad utilizando la API de WeatherAPI.
    """
    url = f"{BASE_URL}?key={API_KEY}&q={ciudad}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperatura = data['current']['temp_c']
        humedad = data['current']['humidity']
        icon_url = "https:" + data['current']['condition']['icon']
        condition_text = data['current']['condition']['text']
        return temperatura, humedad, icon_url, condition_text
    else:
        return None, None, None, None


# === Definición de las Variables Difusas ===
# Variables de entrada
temperatura = ctrl.Antecedent(np.arange(-10, 41, 1), 'temperatura')
humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')

# Variable de salida
ajuste_ac = ctrl.Consequent(np.arange(0, 101, 1), 'ajuste_ac')

# Definición de las funciones de membresía para la temperatura
temperatura['fria'] = fuzz.trapmf(temperatura.universe, [-10, -10, 0, 15])
temperatura['moderada'] = fuzz.trimf(temperatura.universe, [10, 20, 30])
temperatura['caliente'] = fuzz.trapmf(temperatura.universe, [25, 30, 40, 40])

# Definición de las funciones de membresía para la humedad
humedad['baja'] = fuzz.trapmf(humedad.universe, [0, 0, 30, 50])
humedad['media'] = fuzz.trimf(humedad.universe, [30, 50, 70])
humedad['alta'] = fuzz.trapmf(humedad.universe, [60, 80, 100, 100])

# Definición de las funciones de membresía para el ajuste del AC
ajuste_ac['bajo'] = fuzz.trapmf(ajuste_ac.universe, [0, 0, 30, 50])
ajuste_ac['medio'] = fuzz.trimf(ajuste_ac.universe, [30, 50, 70])
ajuste_ac['alto'] = fuzz.trapmf(ajuste_ac.universe, [60, 80, 100, 100])

# Definición de las reglas difusas
regla1 = ctrl.Rule(temperatura['fria'] | humedad['baja'], ajuste_ac['bajo'])
regla2 = ctrl.Rule(temperatura['moderada'], ajuste_ac['medio'])
regla3 = ctrl.Rule(temperatura['caliente'] & humedad['alta'], ajuste_ac['alto'])

# Creación del sistema de control y simulación
control_ac = ctrl.ControlSystem([regla1, regla2, regla3])
simulacion_ac = ctrl.ControlSystemSimulation(control_ac)


class VentanaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Control Difuso para AC")
        self.setFixedSize(600, 500)

        # Atributos para las animaciones
        self.direccion = 1  # Dirección del movimiento (1 = abajo, -1 = arriba)
        self.gato_pos_inicial = None  # Guardará la posición inicial del ícono

        self.setup_ui()
        self.animar_entrada()
        self.iniciar_movimiento_salto()

    def iniciar_movimiento_salto(self):
        """Iniciar movimiento de salto del ícono."""
        self.gato_pos_inicial = self.icono_label.pos()  # Guardar la posición inicial

        # Iniciar un temporizador para el movimiento de salto
        self.timer_salto = QtCore.QTimer()
        self.timer_salto.timeout.connect(self.mover_salto)
        self.timer_salto.start(100)  # Actualización cada 100ms

    def mover_salto(self):
        """Mover el ícono hacia arriba y hacia abajo."""
        new_y = self.icono_label.y() + (2 * self.direccion)  # Movimiento de 2 píxeles

        # Cambiar dirección si alcanza los límites
        if new_y > self.gato_pos_inicial.y() + 20 or new_y < self.gato_pos_inicial.y() - 20:
            self.direccion *= -1

        self.icono_label.move(self.icono_label.x(), new_y)

    def animar_entrada(self):
        """Animación de aparición de la ventana."""
        self.setWindowOpacity(0)
        self.animacion = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.animacion.setDuration(500)
        self.animacion.setStartValue(0)
        self.animacion.setEndValue(1)
        self.animacion.start()

    def animar_gato(self):
        """Animación de levitación del ícono (no se usa en este código)."""
        self.animacion_gato = QtCore.QPropertyAnimation(self.icono_label, b"pos")
        self.animacion_gato.setDuration(2000)
        self.animacion_gato.setStartValue(QtCore.QPoint(260, 50))
        self.animacion_gato.setEndValue(QtCore.QPoint(260, 55))
        self.animacion_gato.setEasingCurve(QtCore.QEasingCurve.InOutSine)
        self.animacion_gato.setLoopCount(-1)
        self.animacion_gato.start()

    def setup_ui(self):
        """Configuración de la interfaz de usuario."""
        # Imagen de fondo
        self.background_label = QtWidgets.QLabel(self)
        self.background_label.setGeometry(0, 0, 600, 500)
        pixmap = QtGui.QPixmap("background.jpg")
        pixmap = pixmap.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(pixmap)
        self.background_label.lower()  # Enviar al fondo

        fuente_label = QtGui.QFont("Arial", 14, QtGui.QFont.Bold)

        # Widget central y layout principal
        central_widget = QtWidgets.QWidget(self)
        central_widget.setGeometry(0, 0, 600, 500)
        central_widget.setStyleSheet("background: transparent;")
        self.setCentralWidget(central_widget)

        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Título de la aplicación
        titulo = QtWidgets.QLabel("Sistema de Control Difuso para AC")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setFont(QtGui.QFont("Arial", 26, QtGui.QFont.Bold))
        titulo.setStyleSheet("color: #1565C0;")  # Azul profundo

        # Efecto de sombra en el título
        efecto_sombra = QtWidgets.QGraphicsDropShadowEffect()
        efecto_sombra.setBlurRadius(10)
        efecto_sombra.setOffset(2, 2)
        efecto_sombra.setColor(QtGui.QColor(0, 0, 0, 180))
        titulo.setGraphicsEffect(efecto_sombra)

        main_layout.addWidget(titulo)

        # Ícono animado
        self.icono_label = QtWidgets.QLabel(self)
        self.icono_label.setAlignment(QtCore.Qt.AlignCenter)
        icono_pixmap = QtGui.QPixmap("icon.png")
        icono_pixmap = icono_pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.icono_label.setPixmap(icono_pixmap)
        main_layout.addWidget(self.icono_label)
        self.icono_label.move(260, 50)  # Posición inicial

        # Imagen del clima
        self.imagen_label = QtWidgets.QLabel()
        self.imagen_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.imagen_label)

        # Campo de entrada de la ciudad
        entrada_layout = QtWidgets.QHBoxLayout()
        ciudad_label = QtWidgets.QLabel("Ingrese la ciudad:")
        ciudad_label.setFont(fuente_label)
        ciudad_label.setStyleSheet("color: white;")
        entrada_layout.addWidget(ciudad_label)

        self.ciudad_entry = QtWidgets.QLineEdit()
        self.ciudad_entry.setFont(fuente_label)
        self.ciudad_entry.returnPressed.connect(self.ejecutar_simulacion)
        self.ciudad_entry.setStyleSheet("""
            QLineEdit {
                background-color: rgba(33, 150, 243, 80);
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QLineEdit:focus {
                background-color: rgba(33, 150, 243, 100);
            }
        """)
        entrada_layout.addWidget(self.ciudad_entry)
        main_layout.addLayout(entrada_layout)

        # Botón de ejecución
        self.ejecutar_button = QtWidgets.QPushButton("Ejecutar Simulación")
        self.ejecutar_button.setFont(fuente_label)
        self.ejecutar_button.clicked.connect(self.ejecutar_simulacion)
        self.ejecutar_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1E88E5, stop:1 #1565C0);
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
                transition: all 0.3s ease-in-out;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42A5F5, stop:1 #1E88E5);
                transform: scale(1.08);
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        main_layout.addWidget(self.ejecutar_button)

        # Etiqueta de resultados
        self.resultado_label = QtWidgets.QLabel()
        self.resultado_label.setFont(fuente_label)
        self.resultado_label.setAlignment(QtCore.Qt.AlignTop)
        self.resultado_label.setWordWrap(True)
        self.resultado_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 150);
                color: #F0F0F0;
                border: 2px solid #2196F3;
                border-radius: 10px;
                padding: 10px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 150);
            }
        """)
        main_layout.addWidget(self.resultado_label, stretch=1)

    def ejecutar_simulacion(self):
        """Ejecutar la simulación al presionar el botón o presionar Enter."""
        ciudad = self.ciudad_entry.text()

        # Animación de opacidad en la imagen del clima
        self.imagen_label.setGraphicsEffect(QtWidgets.QGraphicsOpacityEffect())
        animacion_opacidad = QtCore.QPropertyAnimation(self.imagen_label, b"opacity")
        animacion_opacidad.setDuration(500)
        animacion_opacidad.setStartValue(0)
        animacion_opacidad.setEndValue(1)
        animacion_opacidad.start()

        if not ciudad:
            QtWidgets.QMessageBox.warning(self, "Entrada inválida", "Por favor, ingrese una ciudad.")
            return

        temp, hum, icon_url, condition_text = obtener_datos_climaticos(ciudad)
        if temp is not None and hum is not None:
            try:
                # Cargar y mostrar el ícono del clima
                image_data = requests.get(icon_url).content
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(image_data)
                pixmap = pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                self.imagen_label.setPixmap(pixmap)
            except Exception as e:
                self.imagen_label.clear()

            # Actualizar el sistema difuso con los datos obtenidos
            simulacion_ac.input['temperatura'] = temp
            simulacion_ac.input['humedad'] = hum
            simulacion_ac.compute()

            ajuste = simulacion_ac.output['ajuste_ac']
            resultado = (f"<b>Ciudad:</b> {ciudad}<br>"
                         f"<b>Condición Climática:</b> {condition_text}<br>"
                         f"<b>Temperatura Exterior:</b> {temp} °C<br>"
                         f"<b>Humedad Exterior:</b> {hum}%<br>"
                         f"<b>Ajuste del Aire Acondicionado:</b> {ajuste:.2f}%")
            self.resultado_label.setText(resultado)
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "No se pudo obtener la información necesaria.")


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        ventana = VentanaPrincipal()
        ventana.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
