from repositories.sistema_repository import SistemaRepository
import sys

def menu_admin(repo):
    while True:
        print("\n=== PANEL DE ADMINISTRADOR ===")
        print("1. Registrar Empleado (Create)")
        print("2. Ver Empleados (Read)")
        print("3. Eliminar Empleado (Delete)")
        print("4. Crear Departamento")
        print("5. Crear Proyecto")
        print("6. Cerrar Sesión")
        
        opcion = input("Seleccione una opción: ")
        
        try:
            if opcion == '1':
                nombre = input("Nombre: ").strip()
                correo = input("Correo: ").strip()
                password = input("Contraseña temporal: ").strip()
                cargo = input("Cargo: ").strip()
                
                # Validación de entradas para evitar caídas (Requisito 2.1.4.G.14)
                if not nombre or not correo or not password or not cargo:
                    raise ValueError("Todos los campos son obligatorios. No pueden estar vacíos.")
                
                repo.registrar_empleado(nombre, correo, password, cargo)
                
            elif opcion == '2':
                print("\n--- Lista de Empleados ---")
                repo.ver_empleados()
                
            elif opcion == '3':
                print("\n--- Eliminar Empleado ---")
                repo.ver_empleados()
                id_eliminar = input("Ingrese el ID del empleado a eliminar: ").strip()
                if not id_eliminar.isdigit():
                    raise ValueError("El ID debe ser un número entero.")
                repo.eliminar_empleado(int(id_eliminar))
                
            elif opcion == '4':
                nombre = input("Nombre del nuevo departamento: ").strip()
                if not nombre: raise ValueError("El nombre no puede estar vacío.")
                repo.crear_departamento(nombre)
                
            elif opcion == '5':
                nombre = input("Nombre del nuevo proyecto: ").strip()
                if not nombre: raise ValueError("El nombre no puede estar vacío.")
                repo.crear_proyecto(nombre)
                
            elif opcion == '6':
                print("Cerrando sesión de Administrador...")
                break
            else:
                print("Opción inválida.")
                
        except ValueError as ve:
            print(f"Error de validación: {ve}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

def menu_empleado(repo, usuario):
    empleado_id = usuario['id']
    while True:
        print(f"\n=== PANEL DE EMPLEADO: {usuario['nombre']} ===")
        print("1. Ver Departamentos disponibles")
        print("2. Unirme a un Departamento (Update)")
        print("3. Ver Proyectos disponibles")
        print("4. Unirme a un Proyecto (Update)")
        print("5. Ver mis Proyectos actuales")
        print("6. Cerrar Sesión")
        
        opcion = input("Seleccione una opción: ")
        
        try:
            if opcion == '1':
                print("\n--- Departamentos ---")
                for d in repo.ver_departamentos():
                    print(f"ID: {d['id']} | Nombre: {d['nombre']}")
                    
            elif opcion == '2':
                depto_id = input("Ingrese el ID del departamento al que desea unirse: ").strip()
                if not depto_id.isdigit(): raise ValueError("El ID debe ser un número.")
                repo.unirse_departamento(empleado_id, int(depto_id))
                
            elif opcion == '3':
                print("\n--- Proyectos ---")
                for p in repo.ver_proyectos():
                    print(f"ID: {p['id']} | Nombre: {p['nombre']}")
                    
            elif opcion == '4':
                proyecto_id = input("Ingrese el ID del proyecto: ").strip()
                if not proyecto_id.isdigit(): raise ValueError("El ID debe ser un número.")
                repo.unirse_proyecto(empleado_id, int(proyecto_id))
                
            elif opcion == '5':
                print("\n--- Mis Proyectos ---")
                proyectos = repo.ver_mis_proyectos(empleado_id)
                if proyectos:
                    for p in proyectos:
                        print(f"- {p['nombre']}")
                else:
                    print("No estás en ningún proyecto aún.")
                    
            elif opcion == '6':
                print("Cerrando sesión de Empleado...")
                break
            else:
                print("Opción inválida.")
                
        except ValueError as ve:
            print(f"Error de entrada: {ve}")

def main():
    repo = SistemaRepository() 
    
    while True:
        print("\n=== ACCESO ECOTECH SOLUTIONS ===")
        print("1. Iniciar Sesión")
        print("2. Salir")
        
        inicio = input("Seleccione: ")
        
        if inicio == '1':
            correo = input("Usuario / Correo: ").strip()
            password = input("Contraseña: ").strip()
            
            usuario = repo.login(correo, password)
            
            if usuario:
                if usuario['rol'] == 'admin':
                    menu_admin(repo)
                else:
                    menu_empleado(repo, usuario)
            else:
                print("Credenciales incorrectas. Intente nuevamente.")
        
        elif inicio == '2':
            print("Saliendo del sistema...")
            sys.exit()

if __name__ == "__main__":
    main()