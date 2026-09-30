import sqlite3
from sqlite3 import Error

class ConexionBD:
    def __init__(self):
        self.db_name = 'ecotech_db.sqlite'

    def conectar(self):
        try:
            # Conexión a la base de datos local
            conexion = sqlite3.connect(self.db_name)
            conexion.row_factory = sqlite3.Row 
            conexion.execute("PRAGMA foreign_keys = ON")
            return conexion
        except Error as e:
            print(f"Error crítico de conexión a la base de datos: {e}")
            return None

    def desconectar(self, conexion):
        if conexion:
            conexion.close()
