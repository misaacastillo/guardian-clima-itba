# GuardianClima ITBA

GuardianClima ITBA es una aplicacion de consola hecha en Python.
Permite registrar usuarios, iniciar sesion, consultar el clima actual, guardar un historial global de consultas, ver estadisticas y pedir un consejo de vestimenta con inteligencia artificial.

## Resumen

- registra usuarios nuevos en un archivo CSV
- valida contrasenas con reglas basicas de seguridad
- consulta el clima actual de una ciudad con OpenWeatherMap
- guarda cada consulta en un historial global
- muestra historial personal por ciudad
- calcula estadisticas globales
- genera un consejo de vestimenta con Gemini a partir de la ultima consulta

## Tecnologias

- Python 3
- `requests`
- API de OpenWeatherMap
- API de Gemini
- archivos CSV

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

## Configuracion

La app busca las claves en un archivo `.env` dentro de la carpeta del proyecto.

Crear un archivo llamado `.env` con este formato:

```env
OPENWEATHER_API_KEY=tu_api_key_de_openweathermap
GEMINI_API_KEY=tu_api_key_de_gemini
GEMINI_MODEL=gemini-2.5-flash
```

## Menu

Menu de acceso:

1. Iniciar sesion
2. Registrar nuevo usuario
3. Salir

Menu principal:

1. Consultar clima actual y guardar en historial global
2. Ver mi historial personal por ciudad
3. Ver estadisticas globales
4. Consejo IA: como me visto hoy
5. Acerca de
6. Cerrar sesion

## Archivos

```text
guardian-clima-itba/
├── main.py
├── funciones_app.py
└── data/
    ├── usuarios_simulados.csv
    └── historial_global.csv
```

## Datos guardados

`data/usuarios_simulados.csv`
- guarda usuarios y contrasenas simuladas

`data/historial_global.csv`
- guarda usuario, ciudad, fecha y hora, temperatura, condicion climatica, humedad y viento
- sirve despues para hacer los graficos en Excel o Google Sheets
