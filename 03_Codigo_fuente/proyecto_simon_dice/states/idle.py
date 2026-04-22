from machine import Pin, ADC
import time

class IdleState:
    def __init__(self, fsm):
        self.fsm = fsm
        self.kb = fsm.kb 
        
        # --- PERCEPCIÓN: MICRÓFONO (GPIO 11) ---
        self.mic = ADC(Pin(13))
        self.mic.atten(ADC.ATTN_11DB) 
        
        # Configuración de botones
        self.btn_rojo = Pin(1, Pin.IN, Pin.PULL_DOWN)
        self.btn_verde = Pin(2, Pin.IN, Pin.PULL_DOWN)
        self.btn_amarillo = Pin(4, Pin.IN, Pin.PULL_DOWN)
        self.btn_azul = Pin(5, Pin.IN, Pin.PULL_DOWN)

    def on_enter(self):
        print("Estado: IDLE. Esperando inicio (Botón o Aplauso)...")
        if self.fsm.leds:
            self.fsm.leds.todos_off()
            
        if self.fsm.display:
            self.fsm.display.mostrar_resultado("SIMON DICE")

    def update(self):
        # 1. LEER UMBRAL DEL JSON
        umbral = self.kb.get("percepcion_auditiva", "umbral_ruido") or 3400
        lectura_mic = self.mic.read()

        # 2. VERIFICAR ACTIVACIÓN
        btn_presionado = (self.btn_rojo.value() == 1 or self.btn_verde.value() == 1 or 
                          self.btn_amarillo.value() == 1 or self.btn_azul.value() == 1)
        
        sonido_detectado = lectura_mic > umbral

        if btn_presionado or sonido_detectado:
            tipo = "SONIDO" if sonido_detectado else "BOTÓN"
            print(f"Percepción: ¡Inicio detectado por {tipo}! (Valor: {lectura_mic})")
            
            # --- LIMPIEZA DE MEMORIA (FIX PARA EL INICIO LOCO) ---
            # Borramos cualquier rastro de la partida anterior en la BC
            self.kb.update_state("secuencia_maestra", [])
            self.kb.update_state("paso_actual", 0)
            
            # Animación rápida de "Despertar"
            if self.fsm.leds: self.fsm.leds.todos_on()
            time.sleep(0.2)
            if self.fsm.leds: self.fsm.leds.todos_off()
            
            time.sleep(0.3) 
            self.fsm.change_state("SEQUENCE")