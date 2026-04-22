import time
import random

class SequenceState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.kb = fsm.kb
        self.leds = fsm.leds
        self.display = fsm.display

    def on_enter(self):
        secuencia = self.kb.get("estado_actual", "secuencia_maestra")
        nivel = len(secuencia) if secuencia else 1
        
        if self.display:
            self.display.mostrar_resultado(f"NIVEL {nivel}")
        
        # ESPERA DINÁMICA: A más nivel, menos espera para empezar
        espera_inicial = max(0.2, 1.0 - (nivel * 0.1))
        time.sleep(espera_inicial)
        
        self.ejecutar_secuencia()
        
        if self.display:
            self.display.mostrar_resultado("TU TURNO")
            
        self.fsm.change_state("USER_INPUT")

    def ejecutar_secuencia(self):
        secuencia = self.kb.get("estado_actual", "secuencia_maestra")
        
        if not secuencia:
            secuencia = [random.choice(["0", "1", "2", "3"])]
            self.kb.update_state("secuencia_maestra", secuencia)

        # --- LÓGICA BASADA EN EL JSON ---
        nivel = len(secuencia)
        base_on = self.kb.get("reglas_inferencia", "ms_encendido_base") or 400
        base_off = self.kb.get("reglas_inferencia", "ms_pausa_base") or 200
        factor = self.kb.get("reglas_inferencia", "factor_aceleracion") or 0.92
        minimo = self.kb.get("reglas_inferencia", "umbral_minimo_ms") or 130

        # CÁLCULO DINÁMICO DE TIEMPOS
        # T = Base * (Factor ^ (Nivel - 1))
        duracion = max(minimo, int(base_on * (factor ** (nivel - 1))))
        pausa = max(int(minimo / 2), int(base_off * (factor ** (nivel - 1))))
        
        print(f"Log: Velocidad -> ON: {duracion}ms, OFF: {pausa}ms")
        
        nombres = {"0": "ROJO", "1": "AZUL", "2": "VERDE", "3": "AMARILLO"}

        # REPRODUCCIÓN DE LA SECUENCIA
        for simbolo in secuencia:
            simbolo_str = str(simbolo)
            nombre_color = nombres.get(simbolo_str, "???")
            
            # --- INTEGRACIÓN DE SONIDO (LAPTOP) ---
            # Mandamos el ID al puerto serial para que el script de la PC lo cache
            print(f"[SND]:{simbolo_str}")
            
            if self.display:
                self.display.mostrar_color(nombre_color)
            
            self.leds.encender(simbolo_str, duracion)
            
            # Tiempo de espera entre destellos
            time.sleep_ms(pausa)