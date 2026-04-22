from machine import Pin
import time

class LEDController:
    def __init__(self, kb):
        self.fsm_kb = kb # Guardamos la referencia a la BC
        self.leds = {}
        
        # En lugar de get_all, buscamos los IDs directamente 0, 1, 2, 3
        # Esto es más robusto y evita el error de atributo
        for i in range(4):
            id_str = str(i)
            # Buscamos el pin en hardware_map -> id -> led
            pin_num = self.fsm_kb.get("hardware_map", id_str).get("led")
            if pin_num:
                self.leds[id_str] = Pin(pin_num, Pin.OUT)
                self.leds[id_str].value(0)
                print(f"LED {id_str} configurado en pin {pin_num}")

    def encender(self, id_color, ms):
        id_str = str(id_color)
        if id_str in self.leds:
            self.leds[id_str].value(1)
            time.sleep_ms(ms)
            self.leds[id_str].value(0)

    def todos_off(self):
        for led in self.leds.values():
            led.value(0)

    def todos_on(self):
        for led in self.leds.values():
            led.value(1)

    def secuencia_error(self):
        # El parpadeo de "Game Over"
        for _ in range(3):
            self.todos_on()
            time.sleep_ms(150)
            self.todos_off()
            time.sleep_ms(150)