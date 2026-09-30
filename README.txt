=========================================================
ECOTECH SOLUTIONS - SISTEMA DE GESTIÓN DE EMPLEADOS
=========================================================

1. DESCRIPCIÓN DEL PROYECTO
Este sistema es una aplicación de consola en Python diseñada bajo los principios 
de Programación Orientada a Objetos (POO). Permite la gestión de empleados, 
departamentos y proyectos, cumpliendo con operaciones CRUD completas, 
manejo de excepciones (try-except) y almacenamiento persistente seguro.

2. REQUISITOS DEL SISTEMA
- Python 3.8 o superior.
- Librería 'sqlite3' (incluida por defecto en la instalación oficial de Python).
- No requiere instalación de servidores externos (MySQL/XAMPP) ya que utiliza 
  SQLite3 para almacenamiento local, cumpliendo el requerimiento de librería oficial.

3. INSTRUCCIONES DE CONFIGURACIÓN Y EJECUCIÓN
PASO 1: Estructura de Archivos
Asegúrese de que el proyecto mantiene la siguiente estructura y de que existen 
los archivos '__init__.py' en las carpetas para que sean reconocidas como módulos:
/ecotech_solutions
  /db (contiene conexion.py y __init__.py)
  /models (contiene usuario.py, empleado.py y __init__.py)
  /repositories (contiene sistema_repository.py y __init__.py)
  main.py

PASO 2: Ejecución
Abra una terminal en la ruta principal del proyecto y ejecute el siguiente comando:
> python main.py

PASO 3: Inicialización Automática
Al ejecutarse por primera vez, el sistema creará automáticamente el archivo 
'ecotech_db.sqlite', que contiene la estructura completa de la base de datos y 
registrará al administrador predeterminado.

4. CREDENCIALES DE ACCESO (ADMINISTRADOR)
Para probar el menú de creación de usuarios y departamentos, inicie sesión con:
- Correo / Usuario: admin
- Contraseña: admin123

5. NOTAS TÉCNICAS (Cumplimiento de Rúbrica)
- POO (Encapsulamiento y Herencia): Se evidencia en la carpeta /models. La clase 
  'Empleado' hereda de 'Usuario', y todos los atributos están encapsulados (__).
- Operaciones CRUD: Implementadas en 'sistema_repository.py'. Permite crear (registrar), 
  leer (ver), actualizar (unirse a depto/proyecto) y eliminar empleados.
- Control de Errores: Se validan las entradas vacías (ValueError) y se evitan 
  caídas del sistema mediante bloques try-except en todas las transacciones SQL 
  (sqlite3.Error, sqlite3.IntegrityError).
- Seguridad: Se utilizan consultas parametrizadas (?) para prevenir Inyección SQL, 
  decisión adoptada tras refinar críticamente las sugerencias iniciales de la IA.

6. USO DE INTELIGENCIA ARTIFICIAL (Validación Crítica)
Durante el desarrollo del sistema, nos apoyamos en herramientas de IA generativa 
(como ChatGPT) para optimizar el código basándonos en los requerimientos de la rúbrica:
- Estructuración de menús (HUD): Usamos la IA para que nos ayude a formular la base 
  y la HUD iterativa del sistema, asegurando que la interfaz de consola cubriera de 
  forma lógica y amigable todas las funciones exigidas por la evaluación.
- Optimización Arquitectónica: También nos ayudó en saber cuántas clases colocar 
  para no tener que colocar clases que sobresalgan o sobren en el sistema. Esto nos 
  permitió abstraer el modelo UML correctamente y enfocarnos solo en la herencia 
  entre 'Usuario' y 'Empleado', evitando redundancia o sobreingeniería
- y tambien a la creación de Este readme para no solo poder guiarnos si no que tambien para
guiar a los que no saben