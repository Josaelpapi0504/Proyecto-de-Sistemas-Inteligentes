import time
from core.kb_manager import KBManager
from core.state_machine import SimonStateMachine
from hardware.leds import LEDController
from hardware.display import DisplayController
from hardware.sound import SoundController

def main():
    # 1. Inicialización de los componentes
    kb = KBManager() 
    leds = LEDController(kb)
    display = DisplayController()
    
    # Si el sonido necesita un pin específico, se configura aquí
    sound = SoundController() 
    
    # 2. LIMPIEZA DE HARDWARE (Para apagar LEDs amarillo/verde rebeldes)
    print("Limpiando hardware...")
    leds.todos_off() 
    if display: 
        display.clear()
        display.mostrar_resultado("SIMON DICE")
    
    # 3. Inicialización del Cerebro (Máquina de Estados)
    # Pasamos todos los controladores para que los estados puedan usarlos
    brain = SimonStateMachine(kb, leds, display, sound)
    
    print("Empieza el juego...")
    
    # 4. Bucle Principal
    while True:
        # La máquina de estados decide qué hacer según el estado actual
        brain.update()
        
        # Pequeña pausa para no saturar el procesador del ESP32
        time.sleep(0.01)

if __name__ == "__main__":
    main()