from machine import I2S, Pin
import time
import math

class VoiceAdapter:
    def __init__(self):
        self.audio_in = I2S(0, 
                           sck=Pin(12), ws=Pin(11), sd=Pin(10),
                           mode=I2S.RX, 
                           bits=16, 
                           format=I2S.MONO,
                           rate=16000, 
                           ibuf=16000)
        
        self.buffer = bytearray(1024)
        self.umbral_voz = 500

    def listen_for_color(self):
        """
        Escucha el ambiente. Si detecta sonido, intenta machear con un color.
        Retorna el ID (0-3) o None si no hay entrada clara.
        """
        num_read = self.audio_in.readinto(self.buffer)
        if num_read == 0:
            return None

        samples = self._bytes_to_samples(self.buffer)
        
        energy = self._calculate_energy(samples)

        if energy > self.umbral_voz:
            print(f"Percepción: Voz detectada (E:{energy})")
            return self._classify_voice(samples)
            
        return None

    def _bytes_to_samples(self, buf):
        import struct
        count = len(buf) // 2
        return struct.unpack(str(count) + 'h', buf)

    def _calculate_energy(self, samples):
        return math.sqrt(sum(s*s for s in samples) / len(samples))

    def _classify_voice(self, samples):
        """
        MOTOR DE INFERENCIA ACÚSTICO:
        Distingue colores por 'Firma de Frecuencia' o 'Duración'.
        """
        crossings = 0
        for i in range(len(samples)-1):
            if (samples[i] > 0 and samples[i+1] < 0) or (samples[i] < 0 and samples[i+1] > 0):
                crossings += 1
        
        if crossings > 150: return 3
        if crossings < 80:  return 0
        
        return None