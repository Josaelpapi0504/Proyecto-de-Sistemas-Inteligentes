import time
from machine import Pin, SoftI2C
import ssd1306

class DisplayController:
    def __init__(self, width=128, height=64):
        self.width = width
        self.height = height
        self.iniciar_i2c()
        print("Display: Modo visual activo.")

    def iniciar_i2c(self):
        """Crea la conexión básica con la pantalla."""
        try:
            self.i2c = SoftI2C(sda=Pin(18, Pin.IN, Pin.PULL_UP), scl=Pin(17, Pin.IN, Pin.PULL_UP), freq=10000)
            self.oled = ssd1306.SSD1306_I2C(self.width, self.height, self.i2c)
            # Damos un pequeño respiro a la energía
            time.sleep(0.1) 
        except Exception as e:
            self.oled = None

    def mostrar_resultado(self, mensaje):
        """Muestra texto. Si la energía falla, atrapa el error y se reinicia sola."""
        if not self.oled: return
        try:
            self.oled.fill(0)
            self.oled.text(mensaje, 30, 30)
            self.oled.show()
        except OSError:
            # Mecanismo de rescate básico: reconectamos y lo intentamos de nuevo
            self.iniciar_i2c()
            if self.oled:
                self.oled.fill(0)
                self.oled.text(mensaje, 30, 30)
                self.oled.show()

    def mostrar_color(self, nombre):
        if not self.oled: return
        try:
            self.oled.fill(0)
            self.oled.rect(0, 0, 128, 64, 1)
            self.oled.text("COLOR:", 40, 15)
            self.oled.text(nombre.upper(), 40, 35)
            self.oled.show()
        except OSError:
            # Mecanismo de rescate básico
            self.iniciar_i2c()
            if self.oled:
                self.oled.fill(0)
                self.oled.rect(0, 0, 128, 64, 1)
                self.oled.text("COLOR:", 40, 15)
                self.oled.text(nombre.upper(), 40, 35)
                self.oled.show()

    def clear(self):
        if not self.oled: return
        try:
            self.oled.fill(0)
            self.oled.show()
        except OSError:
            self.iniciar_i2c()