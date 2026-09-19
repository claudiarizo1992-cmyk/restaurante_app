import json
import os

class ArchivoServicio:
    @staticmethod
    def cargar_json(ruta):
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception:
            return []

        @staticmethod
        def guardar_json(ruta,datos):
            with open(ruta, 'w', encoding='utf-8') as file:
                json.dump(datos, file, indent=2, ensure_ascii=False)

