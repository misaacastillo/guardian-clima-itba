from funciones_app import (
    asegurar_archivo_historial,
    asegurar_archivo_usuarios,
    cargar_variables_desde_env,
    consultar_clima_y_guardar,
    iniciar_sesion,
    mostrar_acerca_de,
    mostrar_consejo_ia,
    mostrar_estadisticas_globales,
    pedir_texto,
    registrar_usuario,
    ver_mi_historial_por_ciudad,
)


# Muestra las opciones del menu principal
def mostrar_menu_principal(username):
    print(f"\n=== Menu principal de {username} ===")
    print("1. Consultar clima actual y guardar en historial global")
    print("2. Ver mi historial personal por ciudad")
    print("3. Ver estadisticas globales")
    print("4. Consejo IA: como me visto hoy")
    print("5. Acerca de...")
    print("6. Cerrar sesion")


# Maneja lo que puede hacer el usuario despues del login
def menu_principal(username):
    while True:
        mostrar_menu_principal(username)
        opcion = pedir_texto("Elegi una opcion: ")

        if opcion is None:
            print(f"\nSesion cerrada para {username}.")
            break

        if opcion == "1":
            consultar_clima_y_guardar(username)
        elif opcion == "2":
            ver_mi_historial_por_ciudad(username)
        elif opcion == "3":
            mostrar_estadisticas_globales()
        elif opcion == "4":
            mostrar_consejo_ia(username)
        elif opcion == "5":
            mostrar_acerca_de()
        elif opcion == "6":
            print(f"\nSesion cerrada para {username}.")
            break
        else:
            print("\nOpcion invalida. Proba de nuevo.")


# Muestra el menu antes del login
def mostrar_menu_acceso():
    print("\n=== GuardianClima ITBA ===")
    print("1. Iniciar sesion")
    print("2. Registrar nuevo usuario")
    print("3. Salir")


# Arranca la app y deja listos los archivos base
def main():
    cargar_variables_desde_env()

    if not asegurar_archivo_usuarios() or not asegurar_archivo_historial():
        print("\nNo se pudo preparar la aplicacion.")
        return

    while True:
        mostrar_menu_acceso()
        opcion = pedir_texto("Elegi una opcion: ")

        if opcion is None:
            print("\nSaliendo de la aplicacion.")
            break

        if opcion == "1":
            usuario = iniciar_sesion()
            if usuario:
                menu_principal(usuario)
        elif opcion == "2":
            usuario = registrar_usuario()
            if usuario:
                menu_principal(usuario)
        elif opcion == "3":
            print("\nSaliendo de la aplicacion.")
            break
        else:
            print("\nOpcion invalida. Proba de nuevo.")


if __name__ == "__main__":
    main()
