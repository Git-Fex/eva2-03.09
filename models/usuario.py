class Usuario:
    def __init__(self, id_usuario, nombre, correo, rol):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__correo = correo
        self.__rol = rol

    # Métodos Getters
    def get_id(self):
        return self.__id_usuario

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo
        
    def get_rol(self):
        return self.__rol
