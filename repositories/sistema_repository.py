from db.conexion import ConexionBD
import sqlite3
from sqlite3 import Error

class SistemaRepository:
    def __init__(self):
        self.db = ConexionBD()
        self._inicializar_tablas()

    def _inicializar_tablas(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                script = """
                CREATE TABLE IF NOT EXISTS departamentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS proyectos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    rol TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS empleados (
                    id INTEGER PRIMARY KEY,
                    cargo TEXT NOT NULL,
                    departamento_id INTEGER NULL,
                    FOREIGN KEY (id) REFERENCES usuarios(id) ON DELETE CASCADE,
                    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
                );
                CREATE TABLE IF NOT EXISTS empleados_proyectos (
                    empleado_id INTEGER,
                    proyecto_id INTEGER,
                    PRIMARY KEY (empleado_id, proyecto_id),
                    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
                    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
                );
                """
                cursor.executescript(script)
                
                cursor.execute("SELECT * FROM usuarios WHERE correo = 'admin'")
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO usuarios (nombre, correo, password, rol) VALUES (?, ?, ?, ?)",
                        ('Administrador del Sistema', 'admin', 'admin123', 'admin')
                    )
                conexion.commit()
            except Error as e:
                print(f"Error inicializando la base de datos: {e}")
            finally:
                self.db.desconectar(conexion)

    def login(self, correo, password):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM usuarios WHERE correo = ? AND password = ?", (correo, password))
                row = cursor.fetchone()
                return dict(row) if row else None
            except Error as e:
                print(f"Error en login: {e}")
            finally:
                self.db.desconectar(conexion)
        return None

    #CRUD: CREATE (Crear)
    def registrar_empleado(self, nombre, correo, password, cargo):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO usuarios (nombre, correo, password, rol) VALUES (?, ?, ?, ?)", 
                               (nombre, correo, password, 'empleado'))
                id_usuario = cursor.lastrowid
                cursor.execute("INSERT INTO empleados (id, cargo) VALUES (?, ?)", (id_usuario, cargo))
                conexion.commit()
                print(f"Empleado '{nombre}' registrado exitosamente.")
            except sqlite3.IntegrityError:
                print(f"Error: El correo '{correo}' ya está registrado.")
                conexion.rollback()
            except Error as e:
                conexion.rollback()
                print(f"Error al registrar: {e}")
            finally:
                self.db.desconectar(conexion)

    def crear_departamento(self, nombre):
        self._ejecutar_simple("INSERT INTO departamentos (nombre) VALUES (?)", (nombre,))

    def crear_proyecto(self, nombre):
        self._ejecutar_simple("INSERT INTO proyectos (nombre) VALUES (?)", (nombre,))

    #CRUD: READ (Consultar)
    def ver_empleados(self):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT u.id, u.nombre, u.correo, e.cargo, d.nombre as departamento 
                    FROM usuarios u 
                    JOIN empleados e ON u.id = e.id 
                    LEFT JOIN departamentos d ON e.departamento_id = d.id
                """)
                empleados = cursor.fetchall()
                if not empleados:
                    print("No hay empleados registrados.")
                for emp in empleados:
                    depto = emp['departamento'] if emp['departamento'] else "Sin departamento"
                    print(f"ID: {emp['id']} | Nombre: {emp['nombre']} | Correo: {emp['correo']} | Cargo: {emp['cargo']} | Depto: {depto}")
            except Error as e:
                print(f"Error al consultar empleados: {e}")
            finally:
                self.db.desconectar(conexion)

    def ver_departamentos(self):
        return self._obtener_lista("SELECT * FROM departamentos")

    def ver_proyectos(self):
        return self._obtener_lista("SELECT * FROM proyectos")

    def ver_mis_proyectos(self, empleado_id):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("""
                    SELECT p.nombre FROM proyectos p 
                    JOIN empleados_proyectos ep ON p.id = ep.proyecto_id 
                    WHERE ep.empleado_id = ?
                """, (empleado_id,))
                return [dict(row) for row in cursor.fetchall()]
            finally:
                self.db.desconectar(conexion)
        return []

    #CRUD: UPDATE (Actualizar)
    def unirse_departamento(self, empleado_id, depto_id):
        self._ejecutar_simple("UPDATE empleados SET departamento_id = ? WHERE id = ?", (depto_id, empleado_id))

    def unirse_proyecto(self, empleado_id, proyecto_id):
        try:
            self._ejecutar_simple("INSERT INTO empleados_proyectos (empleado_id, proyecto_id) VALUES (?, ?)", (empleado_id, proyecto_id))
        except sqlite3.IntegrityError:
            print("Error: Ya estás unido a este proyecto o el proyecto no existe.")

    #CRUD: DELETE (Eliminar)
    def eliminar_empleado(self, id_usuario):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id = ? AND rol = 'empleado'", (id_usuario,))
                if cursor.rowcount > 0:
                    conexion.commit()
                    print(f"Empleado con ID {id_usuario} eliminado correctamente.")
                else:
                    print("Error: Empleado no encontrado o ID corresponde a un Administrador.")
            except Error as e:
                conexion.rollback()
                print(f"Error al eliminar empleado: {e}")
            finally:
                self.db.desconectar(conexion)

    def _ejecutar_simple(self, query, params):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(query, params)
                conexion.commit()
                print("Operación exitosa.")
            except Error as e:
                conexion.rollback()
                print(f"Error en la operación: {e}")
            finally:
                self.db.desconectar(conexion)

    def _obtener_lista(self, query):
        conexion = self.db.conectar()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute(query)
                return [dict(row) for row in cursor.fetchall()]
            finally:
                self.db.desconectar(conexion)
        return []
