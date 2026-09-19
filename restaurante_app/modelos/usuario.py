class Usuario:
    def __init__(self, username, password, nombre, rol):
        self.username = username
        self.password = password
        self.nombre = nombre
        self.rol = rol

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "nombre": self.nombre,
            "rol": self.rol
        }

    @staticmethod
    def from_dict(data):
        return Usuario(data["username"], data["password"], data["nombre"], data["rol"])
        