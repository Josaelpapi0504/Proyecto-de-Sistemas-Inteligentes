import ujson
import os

class KBManager:
    _instance = None
    _data = None
    _path = "bc_data.json"

    def __new__(cls):
        """Implementación de Singleton para asegurar una única instancia."""
        if cls._instance is None:
            cls._instance = super(KBManager, cls).__new__(cls)
            cls._instance._load_kb()
        return cls._instance

    def _load_kb(self):
        """Carga la Base de Conocimientos desde el sistema de archivos."""
        try:
            with open(self._path, 'r') as f:
                self._data = ujson.load(f)
            print("KB: Base de conocimientos cargada con éxito.")
        except Exception as e:
            print(f"KB: Error al cargar JSON: {e}")
            # Datos por defecto en caso de error crítico
            self._data = {"estado_actual": {"secuencia_maestra": []}}

    def get(self, *keys):
        """
        Consulta inteligente: permite obtener datos anidados.
        Uso: kb.get('reglas_juego', 'ms_encendido')
        """
        temp = self._data
        for k in keys:
            if isinstance(temp, dict) and k in temp:
                temp = temp[k]
            else:
                return None
        return temp

    def update_state(self, key, value):
        """Actualiza la memoria de trabajo (RAM) y persiste en el JSON."""
        if "estado_actual" in self._data:
            self._data["estado_actual"][key] = value
            self.save()

    def save(self):
        """Persiste los cambios de la RAM al archivo flash del ESP32-S3."""
        try:
            with open(self._path, 'w') as f:
                ujson.dump(self._data, f)
        except Exception as e:
            print(f"KB: Error al guardar persistencia: {e}")

    def reset_sequence(self):
        """Regla de inferencia básica para reiniciar el juego."""
        self.update_state("secuencia_maestra", [])
        self.update_state("paso_actual", 0)