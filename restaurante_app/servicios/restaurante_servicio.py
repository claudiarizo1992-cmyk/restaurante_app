import os
from modelos.usuario import Usuario
from modelos.producto import Producto
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ruta_usuarios = os.path.join(base_dir, "datos", "usuarios.json")
        self.ruta_productos = os.path.join(base_dir, "datos", "productos.json")

    def obtener_usuarios(self):
        datos = ArchivoServicio.cargar_json(self.ruta_usuarios)
        return [Usuario.from_dict(u) for u in datos]

    def autenticar(self, username, password):
        usuarios = self.obtener_usuarios()
        for u in usuarios:
            if u.username == username and u.password == password:
                return u
            return None

    def obtener_productos(self):
        datos = ArchivoServicio.cargar_json(self.ruta_productos)
        return [Producto.from_dict(p) for p in datos]

    def registrar_producto(self, id_prod, nombre, precio, categoria):
        if not id_prod or not nombre or not precio or not categoria:
            raise ValueError("Todos los campos son obligatorios.")

        try:
            precio_val = float(precio)
            if precio_val <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("El precio debe ser un numero positivo.")

        productos = self.obtener_productos()
        if any(p.id_producto == id_prod for p in productos):
            raise ValueError(f"El ID '{id_prod}' ya existe.")

        nuevo_p = Producto(id_prod, nombre, precio_val, categoria)
        productos.append(nuevo_p)
        self._guardar_productos(productos)
        return nuevo_p

    def buscar_producto(self, id_prod):
        productos = self.obtener_productos()
        for p in productos:
            if p.id_producto == id_prod:
                return p
            return None

    def actualizar_producto(self, id_prod, nombre, precio, categoria):
        if not id_prod or not nombre or not precio or not categoria:
            raise ValueError("Todos los campos son obligatorios.")
        try:
            precio_val = float(precio) 
            if precio_val <= 0:
                raise ValueError
        except ValueError:
            raise ValueError("El precio debe ser un numero positivo.") 

        productos = self.obtener_productos() 
        encontrado = False
        for p in productos:
            if p.id_producto == id_prod:
                p.nombre = nombre
                p.precio = precio_val
                p.categoria = categoria
                encontrado = True
                break
        if not encontrado:
            raise ValueError(f"No se encontro el producto con ID '{id_prod}'.")

        self._guardar_productos(productos)

        def eliminar_producto(self, id_prod):
            productos = self.obtener_productos()
            nuevos_productos = [p for p in productos if p.id_producto != id_prod]

            if len(productos) == len(nuevos_productos):
                raise ValueError(f"No se encontro el producto con ID '{id_prod}'.")

            self._guardar_productos(nuevos_productos)

        def _guardar_productos(self, productos):
            datos = [p.to_dict() for p in productos]
            ArchivoServicio.guardar_json(self.ruta_productos, datos)