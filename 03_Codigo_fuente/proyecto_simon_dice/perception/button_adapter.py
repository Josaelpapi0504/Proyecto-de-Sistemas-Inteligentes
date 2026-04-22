from machine import Pin
import time

class ButtonAdapter:
    def __init__(self, kb):
        self.kb = kb
        self.buttons = {}

        mapa = self.kb.get("hardware_map")
        
        if mapa is None:
            print("Percepción: Error - No se encontró 'hardware_map' en la BC")
            return
        
        for key, data in mapa.items():
            try:
                pin_num = data["btn"]
                # CAMBIO 1: Usamos PULL_DOWN para tu conexión a 3.3V
                self.buttons[int(key)] = Pin(pin_num, Pin.IN, Pin.PULL_DOWN)
                print(f"Percepción: Botón {data['color']} (ID {key}) configurado en pin {pin_num}")
            except Exception as e:
                print(f"Percepción: Error en botón {key}: {e}")
            
        self.debounce_time = 200

    def get_input(self):
        """
        Escanea los botones y devuelve el ID (0-3) si uno es presionado.
        """
        for id_color, pin in self.buttons.items():
            # CAMBIO 2: Detectamos el botón con 1 (High) porque mandas 3.3V
            if pin.value() == 1:
                time.sleep_ms(self.debounce_time)
                print(f"Percepción: Botón detectado -> ID {id_color}")
                # Devolvemos el ID numérico (0, 1, 2, 3)
                return id_color
        
        return None

    def wait_for_any_button(self):
        while True:
            res = self.get_input()
            if res is not None:
                return res
            time.sleep_ms(50)