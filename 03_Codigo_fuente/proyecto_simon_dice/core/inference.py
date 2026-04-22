import random
import os
import time

class InferenceEngine:
    def __init__(self, kb):
        self.kb = kb
        # --- FIX DE ENTROPÍA (REEMPLAZO DE machine.rng) ---
        # Generamos una semilla única usando bytes aleatorios del hardware
        try:
            semilla = int.from_bytes(os.urandom(4), 'little')
            random.seed(semilla)
        except:
            # Respaldo por si urandom fallara en algún boot
            random.seed(time.ticks_us())

    def validar_entrada(self, simbolo_recibido):
        """
        Aplica la regla de inferencia:
        SI el símbolo recibido coincide con el símbolo en la posición actual 
        de la secuencia maestra, ENTONCES es un ACIERTO.
        """
        secuencia = self.kb.get("estado_actual", "secuencia_maestra")
        paso_actual = self.kb.get("estado_actual", "paso_actual")

        if not secuencia or paso_actual >= len(secuencia):
            return "ERROR_LOGICO"

        color_esperado = str(secuencia[paso_actual])
        
        if str(simbolo_recibido) == color_esperado:
            return self._procesar_acierto(paso_actual, len(secuencia))
        else:
            return "ERROR_USUARIO"

    def _procesar_acierto(self, paso_actual, total_secuencia):
        """
        Deduce si el acierto completa la secuencia o solo un paso.
        """
        nuevo_paso = paso_actual + 1
        self.kb.update_state("paso_actual", nuevo_paso)

        if nuevo_paso == total_secuencia:
            self._incrementar_puntuacion()
            return "SUCCESS_COMPLETE"
        
        return "SUCCESS_STEP"

    def _incrementar_puntuacion(self):
        """Actualiza los hechos en la BC al completar una ronda."""
        puntos = self.kb.get("estado_actual", "puntuacion") or 0
        nueva_puntuacion = puntos + 1
        self.kb.update_state("puntuacion", nueva_puntuacion)
        
        record = self.kb.get("estado_actual", "record_maximo") or 0
        if nueva_puntuacion > record:
            self.kb.update_state("record_maximo", nueva_puntuacion)

    def generar_nuevo_paso(self):
        """
        Regla: Añadir un nuevo símbolo aleatorio (0-3) a la secuencia.
        """
        secuencia = self.kb.get("estado_actual", "secuencia_maestra") or []
        
        # Agitamos la semilla antes de cada nuevo color usando entropía de hardware
        try:
            nueva_semilla = int.from_bytes(os.urandom(4), 'little')
            random.seed(nueva_semilla)
        except:
            random.seed(time.ticks_cpu())
        
        nuevo_simbolo = random.randint(0, 3)
        secuencia.append(nuevo_simbolo)
        
        self.kb.update_state("secuencia_maestra", secuencia)
        self.kb.update_state("paso_actual", 0)
        return secuencia