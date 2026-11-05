# Laboratorio: Código Seguro y Modelo OWASP

## 1. Datos generales

- **Nombre completo:** Erick Ernesto Castillo Zepeda
- **Carné:** Completar
- **Correo institucional:** erickcastillo.ec65@gmail.com
- **Asignatura:** Lenguajes de Programación con Aspectos de Seguridad
- **Fecha:** 2026-11-05

## 2. Descripción

Este laboratorio consiste en desarrollar una aplicación web utilizando Python, implementando controles básicos de seguridad basados en buenas prácticas y el modelo OWASP. Se aplican mecanismos de validación de entradas, consultas parametrizadas, protección de contraseñas, registro de eventos de autenticación y detección de incidentes, incluyendo el cálculo de las métricas MTTD y MTTR.

## 3. Estructura del proyecto

```text
repositorio/
├── proyecto/
│   ├── app.py
│   ├── crearDB.py
│   ├── detector.py
│   ├── requirements.txt
│   ├── .gitignore
│   └── templates/
│       ├── registro.html
│       └── login.html
└── README.md
```

## 4. Ejecución del proyecto

**Paso 1.** Clonar el repositorio.

```bash
git clone URL_DEL_REPOSITORIO
```

**Paso 2.** Ingresar al proyecto.

```bash
cd repositorio/proyecto
```

**Paso 3.** Instalar las dependencias.

```bash
pip install -r requirements.txt
```

**Paso 4.** Crear la base de datos.

```bash
python crearDB.py
```

**Paso 5.** Ejecutar la aplicación.

```bash
python app.py
```

**Paso 6.** En otra terminal, ejecutar el detector de incidentes.

```bash
python detector.py
```

## 5. Resultados de las pruebas (MTTD y MTTR)

Cada escenario consiste en un inicio de sesión correcto, tres intentos fallidos y un inicio de sesión correcto, seguido de la ejecución de `detector.py`.

| Prueba | Usuario    | MTTD (s) | MTTR (s) |
| ------ | ---------- | -------- | -------- |
| 1      | usuario_01 | 13.0     | 22.0     |
| 2      | usuario_02 | 10.0     | 43.0     |
| 3      | usuario_03 | 10.0     | 13.0     |

**MTTD promedio** = (13.0 + 10.0 + 10.0) / 3 = **11.0 segundos**

**MTTR promedio** = (33.0 + 43.0 + 13.0) / 3 = **29.67 segundo**
