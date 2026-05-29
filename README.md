# GuardianClima ITBA

GuardianClima ITBA es una aplicacion de consola hecha en Python.
Permite registrar usuarios, iniciar sesion, consultar el clima actual, guardar un historial global de consultas, ver estadisticas y pedir un consejo de vestimenta usando inteligencia artificial.

## Que hace la app

- registra usuarios nuevos en un archivo CSV
- valida contrasenas con reglas basicas de seguridad
- consulta el clima actual de una ciudad con OpenWeatherMap
- guarda cada consulta en un historial global
- muestra historial personal por ciudad
- calcula estadisticas globales
- genera un consejo de vestimenta con Gemini a partir de la ultima consulta

## Tecnologias usadas

- Python 3
- `requests`
- API de OpenWeatherMap
- API de Gemini
- archivos CSV para guardar usuarios e historial

## Instalacion

Crear un entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install requests google-genai
```

## Configuracion de API keys

La app busca las claves en un archivo `.env` dentro de la carpeta del proyecto.

Crear un archivo llamado `.env` con este formato:

```env
OPENWEATHER_API_KEY=tu_api_key_de_openweathermap
GEMINI_API_KEY=tu_api_key_de_gemini
GEMINI_MODEL=gemini-2.5-flash
```

Importante:

- no subir `.env` al repositorio
- no pegar las keys en el codigo
- si no estan las keys, las opciones de clima e IA no van a funcionar

## Ejecucion

Con el entorno virtual activado:

```bash
python3 main.py
```

## Flujo de uso

### Menu de acceso

1. Iniciar sesion
2. Registrar nuevo usuario
3. Salir

### Menu principal

1. Consultar clima actual y guardar en historial global
2. Ver mi historial personal por ciudad
3. Ver estadisticas globales
4. Consejo IA: como me visto hoy
5. Acerca de
6. Cerrar sesion

## Archivos principales

```text
guardian-clima-itba/
├── main.py
├── funciones_app.py
└── data/
    ├── usuarios_simulados.csv
    └── historial_global.csv
```

## Archivos de datos

- `data/usuarios_simulados.csv`
  guarda los usuarios y sus contrasenas simuladas

- `data/historial_global.csv`
  guarda todas las consultas de clima hechas por todos los usuarios

## Datos que se guardan en el historial global

Cada consulta guarda:

- usuario
- ciudad
- fecha y hora
- temperatura
- condicion climatica
- humedad
- viento

Ese archivo despues se puede abrir en Excel o Google Sheets para hacer los graficos pedidos en la consigna.

## Manejo de errores

La app intenta manejar de forma simple estos casos:

- ciudad vacia
- opcion invalida en los menus
- usuario repetido
- contrasena que no cumple las reglas
- API key faltante
- ciudad no encontrada
- errores de conexion con las APIs
- errores al leer o guardar archivos CSV

## Aclaracion importante

Este proyecto guarda contrasenas en texto plano solo porque es una simulacion educativa.
En una aplicacion real habria que usar hashing y mejores practicas de autenticacion.
