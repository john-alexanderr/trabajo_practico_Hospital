import sys

from client.api_client import HospitalAPIClient
from client.logger import registrar_log
from client.menus import menu_internaciones, menu_medicos, menu_pacientes
from client.terminal import color, clean_screen, print_fail, print_info, print_ok, print_title, CYAN, BOLD, GREEN, YELLOW


def _banner() -> None:
    print_title("SISTEMA DE GESTIÓN HOSPITALARIA")
    print(color("     API REST + Cliente de Consola", GREEN))
    print()


def _login(cliente: HospitalAPIClient) -> bool:
    print(color("─── INICIO DE SESIÓN ───", YELLOW, BOLD))
    print()
    for intento in range(3):
        usuario = input("  Usuario: ").strip()
        contrasena = input("  Contraseña: ").strip()
        if not usuario or not contrasena:
            print_fail("Campos vacíos.")
            continue
        r = cliente.login(usuario, contrasena)
        if r.get("exito"):
            print_ok(f"{r['mensaje']} Bienvenido, {usuario}.")
            registrar_log(usuario, "Inicio de sesión exitoso")
            return True
        print_fail(r["mensaje"])
        print_info(f"Intentos restantes: {2 - intento}")
    print_fail("Intentos agotados.")
    return False


def _menu_principal(cliente: HospitalAPIClient) -> None:
    while True:
        clean_screen()
        _banner()
        print(color("  ┌──────────────────────────────────────┐", CYAN, BOLD))
        print(color("  │ 1) Gestionar Pacientes               │", CYAN))
        print(color("  │ 2) Gestionar Médicos                  │", CYAN))
        print(color("  │ 3) Gestionar Internaciones            │", CYAN))
        print(color("  │ 4) Salir                              │", CYAN))
        print(color("  └──────────────────────────────────────┘", CYAN, BOLD))
        opcion = input(color("\n  Seleccione una opción: ", BOLD)).strip()
        if opcion == "1":
            clean_screen()
            menu_pacientes(cliente)
        elif opcion == "2":
            clean_screen()
            menu_medicos(cliente)
        elif opcion == "3":
            clean_screen()
            menu_internaciones(cliente)
        elif opcion == "4":
            registrar_log(cliente.usuario or "desconocido", "Cierre de sesión")
            clean_screen()
            print_title("¡HASTA LUEGO!")
            sys.exit(0)
        else:
            print_fail("Opción no válida.")
            input(color("\n  Presione Enter para continuar...", DIM))


def main() -> None:
    clean_screen()
    cliente = HospitalAPIClient()
    _banner()
    if not _login(cliente):
        sys.exit(1)
    _menu_principal(cliente)


if __name__ == "__main__":
    main()
