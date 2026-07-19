import sys

from client.api_client import HospitalAPIClient
from client.logger import registrar_log
from client.menus import menu_internaciones, menu_medicos, menu_pacientes


def _banner() -> None:
    print("\n" + "=" * 50)
    print("  SISTEMA DE GESTIÓN HOSPITALARIA")
    print("  API REST + Cliente de Consola")
    print("=" * 50)


def _login(cliente: HospitalAPIClient) -> bool:
    print("\n--- INICIO DE SESIÓN ---")
    for intento in range(3):
        usuario = input("  Usuario: ").strip()
        contrasena = input("  Contraseña: ").strip()
        if not usuario or not contrasena:
            print("  ✗ Campos vacíos.")
            continue
        r = cliente.login(usuario, contrasena)
        if r.get("exito"):
            print(f"  ✓ {r['mensaje']} Bienvenido, {usuario}.")
            registrar_log(usuario, "Inicio de sesión exitoso")
            return True
        print(f"  ✗ {r['mensaje']}")
        print(f"  Intentos restantes: {2 - intento}")
    print("\n  ✗ Intentos agotados.")
    return False


def _menu_principal(cliente: HospitalAPIClient) -> None:
    while True:
        _banner()
        print("1 - Gestionar pacientes")
        print("2 - Gestionar médicos")
        print("3 - Gestionar internaciones")
        print("4 - Salir")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            menu_pacientes(cliente)
        elif opcion == "2":
            menu_medicos(cliente)
        elif opcion == "3":
            menu_internaciones(cliente)
        elif opcion == "4":
            registrar_log(cliente.usuario or "desconocido", "Cierre de sesión")
            print("\n  ¡Hasta luego!\n")
            sys.exit(0)
        else:
            print("  ✗ Opción no válida.")


def main() -> None:
    cliente = HospitalAPIClient()
    _banner()
    if not _login(cliente):
        sys.exit(1)
    _menu_principal(cliente)


if __name__ == "__main__":
    main()
