from machine import I2S, Pin
import math
import time
import struct

class SoundController:
    def __init__(self):
        self.audio_out = I2S(1, 
                            sck=Pin(18), ws=Pin(8), sd=Pin(17),
                            mode=I2S.TX, 
                            bits=16, 
                            format=I2S.MONO,
                            rate=22050, 
                            ibuf=2048)
        
        self.tonos = {
            0: 261,
            1: 329,
            2: 392,
            3: 523
        }

    def _generate_sine_wave(self, freq, duration_ms, volume=3000):
        """Genera un buffer de audio con una onda senoidal."""
        sample_rate = 22050
        num_samples = int(sample_rate * duration_ms / 1000)
        format_str = "<" + "h" * num_samples
        samples = []
        for i in range(num_samples):
            val = int(volume * math.sin(2 * math.pi * freq * i / sample_rate))
            samples.append(val)
        return struct.pack(format_str, *samples)

    def play_color_tone(self, id_color, duration=400):
        """Reproduce el tono específico de un color."""
        if id_color in self.tonos:
            freq = self.tonos[id_color]
            wave = self._generate_sine_wave(freq, duration)
            self.audio_out.write(wave)

    def play_success_tone(self):
        """Sonido rápido de acierto."""
        wave = self._generate_sine_wave(880, 100, volume=2000)
        self.audio_out.write(wave)

    def play_victory_melody(self):
        """Pequeña melodía al completar la secuencia."""
        for f in [523, 659, 783, 1046]:
            self.audio_out.write(self._generate_sine_wave(f, 150))
            time.sleep_ms(50)

    def play_error_tone(self):
        """Sonido grave de error."""
        wave = self._generate_sine_wave(100, 500, volume=5000)
        self.audio_out.write(wave)

    def deinit(self):
        """Libera el bus I2S."""
        self.audio_out.deinit()