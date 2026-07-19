import requests
from typing import Any


class HospitalAPIClient:
    def __init__(self, url_base: str = "http://localhost:8000") -> None:
        self.url_base = url_base
        self.token: str | None = None
        self.usuario: str | None = None

    def _auth_headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def login(self, usuario: str, contrasena: str) -> dict[str, Any]:
        try:
            r = requests.post(
                f"{self.url_base}/login",
                data={"username": usuario, "password": contrasena},
                timeout=10,
            )
            if r.status_code == 200:
                self.token = r.json().get("access_token")
                self.usuario = usuario
                return {"exito": True, "mensaje": "Login exitoso."}
            return {"exito": False, "mensaje": r.json().get("detail", "Error desconocido.")}
        except requests.ConnectionError:
            return {"exito": False, "mensaje": "No se pudo conectar con la API."}
        except requests.Timeout:
            return {"exito": False, "mensaje": "Tiempo de espera agotado."}
        except requests.RequestException as e:
            return {"exito": False, "mensaje": f"Error de red: {e}"}

    def listar_pacientes(self) -> dict[str, Any]:
        return self._get("/pacientes")

    def buscar_paciente(self, paciente_id: int) -> dict[str, Any]:
        return self._get(f"/pacientes/{paciente_id}")

    def crear_paciente(self, datos: dict[str, Any]) -> dict[str, Any]:
        return self._post("/pacientes", datos)

    def modificar_paciente(self, paciente_id: int, datos: dict[str, Any]) -> dict[str, Any]:
        return self._put(f"/pacientes/{paciente_id}", datos)

    def eliminar_paciente(self, paciente_id: int) -> dict[str, Any]:
        return self._delete(f"/pacientes/{paciente_id}")

    def listar_medicos(self) -> dict[str, Any]:
        return self._get("/medicos")

    def buscar_medico(self, medico_id: int) -> dict[str, Any]:
        return self._get(f"/medicos/{medico_id}")

    def crear_medico(self, datos: dict[str, Any]) -> dict[str, Any]:
        return self._post("/medicos", datos)

    def modificar_medico(self, medico_id: int, datos: dict[str, Any]) -> dict[str, Any]:
        return self._put(f"/medicos/{medico_id}", datos)

    def eliminar_medico(self, medico_id: int) -> dict[str, Any]:
        return self._delete(f"/medicos/{medico_id}")

    def listar_internaciones(self) -> dict[str, Any]:
        return self._get("/internaciones")

    def buscar_internacion(self, internacion_id: int) -> dict[str, Any]:
        return self._get(f"/internaciones/{internacion_id}")

    def crear_internacion(self, datos: dict[str, Any]) -> dict[str, Any]:
        return self._post("/internaciones", datos)

    def modificar_internacion(self, internacion_id: int, datos: dict[str, Any]) -> dict[str, Any]:
        return self._put(f"/internaciones/{internacion_id}", datos)

    def eliminar_internacion(self, internacion_id: int) -> dict[str, Any]:
        return self._delete(f"/internaciones/{internacion_id}")

    def _get(self, endpoint: str) -> dict[str, Any]:
        return self._request("GET", endpoint)

    def _post(self, endpoint: str, datos: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", endpoint, json=datos)

    def _put(self, endpoint: str, datos: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("PUT", endpoint, json=datos)

    def _delete(self, endpoint: str) -> dict[str, Any]:
        return self._request("DELETE", endpoint)

    def _request(self, method: str, endpoint: str, **kwargs) -> dict[str, Any]:
        headers = self._auth_headers()
        if "json" in kwargs:
            kwargs["json"] = kwargs.pop("json")
        try:
            r = requests.request(
                method,
                f"{self.url_base}{endpoint}",
                headers=headers,
                timeout=10,
                **kwargs,
            )
            if r.status_code in (200, 201):
                return {"exito": True, "datos": r.json()}
            if r.status_code == 401:
                return {"exito": False, "mensaje": "No autorizado. Inicie sesión nuevamente."}
            if r.status_code == 422:
                errores = r.json().get("detail", [])
                msgs = [f"  - {' -> '.join(str(c) for c in e.get('loc', []))}: {e.get('msg', '')}" for e in errores]
                return {"exito": False, "mensaje": "Error de validación:\n" + "\n".join(msgs)}
            return {"exito": False, "mensaje": r.json().get("detail", "Error desconocido.")}
        except requests.ConnectionError:
            return {"exito": False, "mensaje": "No se pudo conectar con la API."}
        except requests.Timeout:
            return {"exito": False, "mensaje": "Tiempo de espera agotado."}
        except requests.RequestException as e:
            return {"exito": False, "mensaje": f"Error de red: {e}"}
