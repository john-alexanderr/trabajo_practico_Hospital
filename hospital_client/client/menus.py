from client.api_client import HospitalAPIClient
from client.logger import registrar_log
from client.terminal import (
    BOLD,
    CYAN,
    DIM,
    color,
    print_fail,
    print_info,
    print_ok,
    print_sep,
    print_subtitle,
    print_table,
    print_warn,
)


def leer_entero(mensaje: str) -> int | None:
    valor = input(color(mensaje, BOLD)).strip()
    if not valor:
        print_fail("El campo no puede estar vacío.")
        return None
    try:
        return int(valor)
    except ValueError:
        print_fail("Debe ingresar un número válido.")
        return None


def leer_texto(mensaje: str, obligatorio: bool = True) -> str | None:
    valor = input(color(mensaje, BOLD)).strip()
    if obligatorio and not valor:
        print_fail("El campo no puede estar vacío.")
        return None
    return valor


def mostrar_resultado(resultado: dict) -> None:
    if resultado.get("exito"):
        datos = resultado.get("datos")
        if datos:
            if isinstance(datos, list):
                if not datos:
                    print_warn("No hay registros para mostrar.")
                else:
                    print_table(datos)
            elif isinstance(datos, dict):
                print_sep()
                for k, v in datos.items():
                    print_info(f"{k}: {v}")
                print_sep()
        else:
            print_ok(resultado.get("mensaje", "Operación exitosa."))
    else:
        print_fail(resultado.get("mensaje", "Error desconocido."))


def _submenu(titulo: str, acciones: dict[str, tuple]) -> None:
    while True:
        print_subtitle(titulo)
        for k, (desc, _) in acciones.items():
            print(color(f"  {k}) {desc}", CYAN))
        opcion = input(color("\n  Seleccione una opción: ", BOLD)).strip()
        if opcion in acciones:
            _, fn = acciones[opcion]
            fn()
            input(color("\n  Presione Enter para continuar...", DIM))
        elif opcion == str(len(acciones)):
            break
        else:
            print_fail("Opción no válida.")


# --- Pacientes ---

def _alta_paciente(cliente: HospitalAPIClient) -> None:
    print("\n--- ALTA DE PACIENTE ---")
    campos = [("DNI", leer_texto), ("Nombre", leer_texto), ("Apellido", leer_texto),
              ("Edad", leer_entero), ("Teléfono", leer_texto), ("Obra social", leer_texto)]
    datos = {}
    for nombre, reader in campos:
        val = reader(f"  {nombre}: ")
        if val is None:
            return
        datos[nombre.lower().replace(" ", "_")] = val
    datos["dni"], datos["nombre"], datos["apellido"] = datos.pop("dni"), datos.pop("nombre"), datos.pop("apellido")
    datos["edad"], datos["telefono"], datos["obra_social"] = datos.pop("edad"), datos.pop("teléfono"), datos.pop("obra_social")
    r = cliente.crear_paciente(datos)
    mostrar_resultado(r)
    if r.get("exito"):
        registrar_log(cliente.usuario or "?", f"Alta paciente: {datos['nombre']} {datos['apellido']}")


def _buscar_paciente(cliente: HospitalAPIClient) -> None:
    print("\n--- BUSCAR PACIENTE ---")
    id_ = leer_entero("  ID: ")
    if id_ is None:
        return
    r = cliente.buscar_paciente(id_)
    mostrar_resultado(r)


def _modificar_paciente(cliente: HospitalAPIClient) -> None:
    print("\n--- MODIFICAR PACIENTE ---")
    id_ = leer_entero("  ID del paciente a modificar: ")
    if id_ is None:
        return
    r = cliente.buscar_paciente(id_)
    if not r.get("exito"):
        mostrar_resultado(r)
        return
    print("  (Nuevos datos)")
    datos = {}
    for nombre, reader in [("DNI", leer_texto), ("Nombre", leer_texto), ("Apellido", leer_texto),
                           ("Edad", leer_entero), ("Teléfono", leer_texto), ("Obra social", leer_texto)]:
        val = reader(f"  {nombre}: ")
        if val is None:
            return
        datos[nombre.lower().replace(" ", "_")] = val
    datos["dni"], datos["nombre"], datos["apellido"] = datos.pop("dni"), datos.pop("nombre"), datos.pop("apellido")
    datos["edad"], datos["telefono"], datos["obra_social"] = datos.pop("edad"), datos.pop("teléfono"), datos.pop("obra_social")
    r = cliente.modificar_paciente(id_, datos)
    mostrar_resultado(r)


def _eliminar_paciente(cliente: HospitalAPIClient) -> None:
    print("\n--- ELIMINAR PACIENTE ---")
    id_ = leer_entero("  ID del paciente a eliminar: ")
    if id_ is None:
        return
    if input(f"  ¿Confirma eliminar paciente ID {id_}? (s/n): ").strip().lower() != "s":
        print("  Cancelado.")
        return
    r = cliente.eliminar_paciente(id_)
    mostrar_resultado(r)


def _listar_pacientes(cliente: HospitalAPIClient) -> None:
    print("\n--- LISTADO DE PACIENTES ---")
    r = cliente.listar_pacientes()
    mostrar_resultado(r)


def menu_pacientes(cliente: HospitalAPIClient) -> None:
    _submenu("GESTIÓN DE PACIENTES", {
        "1": ("Alta", lambda: _alta_paciente(cliente)),
        "2": ("Buscar por ID", lambda: _buscar_paciente(cliente)),
        "3": ("Modificar", lambda: _modificar_paciente(cliente)),
        "4": ("Eliminar", lambda: _eliminar_paciente(cliente)),
        "5": ("Listar todos", lambda: _listar_pacientes(cliente)),
        "6": ("Volver", lambda: None),
    })


# --- Médicos ---

def _alta_medico(cliente: HospitalAPIClient) -> None:
    print("\n--- ALTA DE MÉDICO ---")
    datos = {}
    for nombre, reader in [("Matrícula", leer_texto), ("Nombre", leer_texto), ("Apellido", leer_texto),
                           ("Especialidad", leer_texto), ("Teléfono", leer_texto)]:
        val = reader(f"  {nombre}: ")
        if val is None:
            return
        datos[nombre.lower()] = val
    datos["matricula"], datos["nombre"], datos["apellido"] = datos.pop("matrícula"), datos.pop("nombre"), datos.pop("apellido")
    datos["especialidad"], datos["telefono"] = datos.pop("especialidad"), datos.pop("teléfono")
    r = cliente.crear_medico(datos)
    mostrar_resultado(r)
    if r.get("exito"):
        registrar_log(cliente.usuario or "?", f"Alta médico: {datos['nombre']} {datos['apellido']}")


def _buscar_medico(cliente: HospitalAPIClient) -> None:
    print("\n--- BUSCAR MÉDICO ---")
    id_ = leer_entero("  ID: ")
    if id_ is None:
        return
    r = cliente.buscar_medico(id_)
    mostrar_resultado(r)


def _modificar_medico(cliente: HospitalAPIClient) -> None:
    print("\n--- MODIFICAR MÉDICO ---")
    id_ = leer_entero("  ID del médico a modificar: ")
    if id_ is None:
        return
    r = cliente.buscar_medico(id_)
    if not r.get("exito"):
        mostrar_resultado(r)
        return
    datos = {}
    for nombre, reader in [("Matrícula", leer_texto), ("Nombre", leer_texto), ("Apellido", leer_texto),
                           ("Especialidad", leer_texto), ("Teléfono", leer_texto)]:
        val = reader(f"  {nombre}: ")
        if val is None:
            return
        datos[nombre.lower()] = val
    datos["matricula"], datos["nombre"], datos["apellido"] = datos.pop("matrícula"), datos.pop("nombre"), datos.pop("apellido")
    datos["especialidad"], datos["telefono"] = datos.pop("especialidad"), datos.pop("teléfono")
    r = cliente.modificar_medico(id_, datos)
    mostrar_resultado(r)


def _eliminar_medico(cliente: HospitalAPIClient) -> None:
    print("\n--- ELIMINAR MÉDICO ---")
    id_ = leer_entero("  ID del médico a eliminar: ")
    if id_ is None:
        return
    if input(f"  ¿Confirma eliminar médico ID {id_}? (s/n): ").strip().lower() != "s":
        print("  Cancelado.")
        return
    r = cliente.eliminar_medico(id_)
    mostrar_resultado(r)


def _listar_medicos(cliente: HospitalAPIClient) -> None:
    print("\n--- LISTADO DE MÉDICOS ---")
    r = cliente.listar_medicos()
    mostrar_resultado(r)


def menu_medicos(cliente: HospitalAPIClient) -> None:
    _submenu("GESTIÓN DE MÉDICOS", {
        "1": ("Alta", lambda: _alta_medico(cliente)),
        "2": ("Buscar por ID", lambda: _buscar_medico(cliente)),
        "3": ("Modificar", lambda: _modificar_medico(cliente)),
        "4": ("Eliminar", lambda: _eliminar_medico(cliente)),
        "5": ("Listar todos", lambda: _listar_medicos(cliente)),
        "6": ("Volver", lambda: None),
    })


# --- Internaciones ---

def _alta_internacion(cliente: HospitalAPIClient) -> None:
    print("\n--- ALTA DE INTERNACIÓN ---")
    paciente_id = leer_entero("  ID del paciente: ")
    if paciente_id is None:
        return
    medico_id = leer_entero("  ID del médico: ")
    if medico_id is None:
        return
    fecha = leer_texto("  Fecha de ingreso (YYYY-MM-DD): ")
    if fecha is None:
        return
    diagnostico = leer_texto("  Diagnóstico: ")
    if diagnostico is None:
        return
    habitacion = leer_entero("  Nro. de habitación: ")
    if habitacion is None:
        return
    print("  Estados: activa, alta, derivada, fallecido")
    estado = leer_texto("  Estado: ")
    if estado is None:
        return
    datos = {"paciente_id": paciente_id, "medico_id": medico_id, "fecha_ingreso": fecha,
             "diagnostico": diagnostico, "habitacion": habitacion, "estado": estado}
    r = cliente.crear_internacion(datos)
    mostrar_resultado(r)
    if r.get("exito"):
        registrar_log(cliente.usuario or "?", f"Alta internación: Paciente ID {paciente_id}, Médico ID {medico_id}")


def _buscar_internacion(cliente: HospitalAPIClient) -> None:
    print("\n--- BUSCAR INTERNACIÓN ---")
    id_ = leer_entero("  ID: ")
    if id_ is None:
        return
    r = cliente.buscar_internacion(id_)
    mostrar_resultado(r)


def _modificar_internacion(cliente: HospitalAPIClient) -> None:
    print("\n--- MODIFICAR INTERNACIÓN ---")
    id_ = leer_entero("  ID de la internación a modificar: ")
    if id_ is None:
        return
    r = cliente.buscar_internacion(id_)
    if not r.get("exito"):
        mostrar_resultado(r)
        return
    paciente_id = leer_entero("  ID del paciente: ")
    if paciente_id is None:
        return
    medico_id = leer_entero("  ID del médico: ")
    if medico_id is None:
        return
    fecha = leer_texto("  Fecha de ingreso (YYYY-MM-DD): ")
    if fecha is None:
        return
    diagnostico = leer_texto("  Diagnóstico: ")
    if diagnostico is None:
        return
    habitacion = leer_entero("  Nro. de habitación: ")
    if habitacion is None:
        return
    print("  Estados: activa, alta, derivada, fallecido")
    estado = leer_texto("  Estado: ")
    if estado is None:
        return
    datos = {"paciente_id": paciente_id, "medico_id": medico_id, "fecha_ingreso": fecha,
             "diagnostico": diagnostico, "habitacion": habitacion, "estado": estado}
    r = cliente.modificar_internacion(id_, datos)
    mostrar_resultado(r)


def _eliminar_internacion(cliente: HospitalAPIClient) -> None:
    print("\n--- ELIMINAR INTERNACIÓN ---")
    id_ = leer_entero("  ID de la internación a eliminar: ")
    if id_ is None:
        return
    if input(f"  ¿Confirma eliminar internación ID {id_}? (s/n): ").strip().lower() != "s":
        print("  Cancelado.")
        return
    r = cliente.eliminar_internacion(id_)
    mostrar_resultado(r)


def _listar_internaciones(cliente: HospitalAPIClient) -> None:
    print("\n--- LISTADO DE INTERNACIONES ---")
    r = cliente.listar_internaciones()
    mostrar_resultado(r)


def menu_internaciones(cliente: HospitalAPIClient) -> None:
    _submenu("GESTIÓN DE INTERNACIONES", {
        "1": ("Alta", lambda: _alta_internacion(cliente)),
        "2": ("Buscar por ID", lambda: _buscar_internacion(cliente)),
        "3": ("Modificar", lambda: _modificar_internacion(cliente)),
        "4": ("Eliminar", lambda: _eliminar_internacion(cliente)),
        "5": ("Listar todos", lambda: _listar_internaciones(cliente)),
        "6": ("Volver", lambda: None),
    })
