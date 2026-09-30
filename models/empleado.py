from models.usuario import Usuario

class Empleado(Usuario):
    def __init__(self, id_usuario, nombre, correo, rol, cargo, departamento_id=None):
        # Herencia: Llama al constructor de la clase padre
        super().__init__(id_usuario, nombre, correo, rol)
        self.__cargo = cargo
        self.__departamento_id = departamento_id

    def get_cargo(self):
        return self.__cargo
