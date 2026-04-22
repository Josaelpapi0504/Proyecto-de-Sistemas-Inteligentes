import time
from machine import Pin
from core.inference import InferenceEngine

class UserInputState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.kb = fsm.kb
        self.leds = fsm.leds
        self.display = fsm.display
        self.inference = InferenceEngine(self.kb)
        
        # CONFIGURACIÓN FÍSICA DIRECTA (Pines ISC-UNITEC validados)
        self.btn_rojo = Pin(1, Pin.IN, Pin.PULL_DOWN)      # ID 0
        self.btn_azul = Pin(5, Pin.IN, Pin.PULL_DOWN)      # ID 1
        self.btn_verde = Pin(2, Pin.IN, Pin.PULL_DOWN)     # ID 2
        self.btn_amarillo = Pin(4, Pin.IN, Pin.PULL_DOWN)  # ID 3

    def on_enter(self):
        print("Estado: USER_INPUT. Esperando tu respuesta...")
        if self.display:
            self.display.mostrar_resultado("TU TURNO")
        
        self.kb.update_state("paso_actual", 0)

    def update(self):
        entrada = None

        # 1. Escaneo de pines
        if self.btn_rojo.value() == 1:       entrada = "0"
        elif self.btn_azul.value() == 1:     entrada = "1"
        elif self.btn_verde.value() == 1:    entrada = "2"
        elif self.btn_amarillo.value() == 1: entrada = "3"

        if entrada is not None:
            # --- LECTURA DE SENSIBILIDAD DESDE LA BC ---
            t_feedback = self.kb.get("reglas_inferencia", "feedback_usuario_ms") or 80
            t_debounce = self.kb.get("reglas_inferencia", "debounce_ms") or 60
            
            nombres = {"0": "ROJO", "1": "AZUL", "2": "VERDE", "3": "AMARILLO"}
            
            # --- DISPARADOR DE SONIDO (LAPTOP) ---
            print(f"[SND]:{entrada}") 

            if self.display:
                self.display.mostrar_color(nombres.get(entrada))
            
            # Feedback físico
            self.leds.encender(entrada, t_feedback)
            
            # Espera mínima de rebote definida en JSON
            time.sleep_ms(t_debounce) 
            
            self.procesar_logica(entrada)

    def procesar_logica(self, simbolo):
        resultado = self.inference.validar_entrada(simbolo)
        
        if resultado == "SUCCESS_STEP":
            print(f"¡Bien! ID {simbolo} correcto.")
            
        elif resultado == "SUCCESS_COMPLETE":
            # --- DISPARADOR DE SONIDO: ÉXITO ---
            print("[SND]:SUCCESS")
            
            print("¡Ronda superada!")
            time.sleep(0.4)
            self.inference.generar_nuevo_paso()
            self.fsm.change_state("SEQUENCE")
            
        elif resultado == "ERROR_USUARIO":
            # --- DISPARADOR DE SONIDO: ERROR ---
            print("[SND]:ERROR")
            
            print("¡Error! Secuencia incorrecta.")
            self.leds.secuencia_error()
            
            secuencia = self.kb.get("estado_actual", "secuencia_maestra")
            puntos = len(secuencia) if secuencia else 0
            
            record = self.kb.get("estado_actual", "record_maximo") or 0
            if puntos > record:
                print(f"¡NUEVO RÉCORD: {puntos}!")
                self.kb.update_state("record_maximo", puntos)
            
            if self.display:
                self.display.mostrar_resultado(f"FIN. PTS: {puntos}")
            
            time.sleep(1.5)
            self.kb.update_state("secuencia_maestra", [])
            self.fsm.change_state("IDLE")