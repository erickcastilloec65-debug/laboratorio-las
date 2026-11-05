import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVENTOS_LOG = os.path.join(BASE_DIR, "eventos.log")
RESPUESTA_LOG = os.path.join(BASE_DIR, "respuesta.log")

FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"
UMBRAL_INTENTOS = 3


def registrar_respuesta(usuario):
    fecha = datetime.now().strftime(FORMATO_FECHA)

    with open(RESPUESTA_LOG, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},USUARIO_BLOQUEADO,{usuario}\n")

    return fecha


def usuarios_ya_bloqueados():
    if not os.path.exists(RESPUESTA_LOG):
        return set()

    bloqueados = set()
    with open(RESPUESTA_LOG, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            if len(partes) == 3 and partes[1] == "USUARIO_BLOQUEADO":
                bloqueados.add(partes[2])
    return bloqueados


def leer_intentos_fallidos():
    intentos = {}

    with open(EVENTOS_LOG, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue

            fecha, tipo, usuario = linea.split(",")

            if tipo == "LOGIN_FALLIDO":
                intentos.setdefault(usuario, []).append(fecha)

    return intentos


def main():
    if not os.path.exists(EVENTOS_LOG):
        print("No existe eventos.log. Genere eventos desde la aplicación.")
        return

    intentos = leer_intentos_fallidos()
    bloqueados = usuarios_ya_bloqueados()

    for usuario, registros in intentos.items():
        if len(registros) < UMBRAL_INTENTOS or usuario in bloqueados:
            continue

        inicio = datetime.strptime(registros[0], FORMATO_FECHA)
        deteccion = datetime.strptime(registros[UMBRAL_INTENTOS - 1], FORMATO_FECHA)

        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Intentos fallidos:", len(registros))
        print("Primer intento:", registros[0])
        print("Detección:", registros[UMBRAL_INTENTOS - 1])

        fecha_respuesta = registrar_respuesta(usuario)
        respuesta = datetime.strptime(fecha_respuesta, FORMATO_FECHA)

        print("Acción aplicada: bloqueo de usuario")
        print("Respuesta:", fecha_respuesta)

        mttd = (deteccion - inicio).total_seconds()
        mttr = (respuesta - deteccion).total_seconds()

        print("MTTD:", mttd, "segundos")
        print("MTTR:", mttr, "segundos")
        print()


if __name__ == "__main__":
    main()
