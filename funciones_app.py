import csv
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parent
USUARIOS_ARCHIVO = BASE_DIR / "data" / "usuarios_simulados.csv"
HISTORIAL_ARCHIVO = BASE_DIR / "data" / "historial_global.csv"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
NOMBRE_GRUPO = "Grupo 29"
DESARROLLADORES = [
    "Agustin Alberto Dabini",
    "Celio Castro",
    "Misael Castillo",
    "Romeo Cukier",
]


# Pide un texto sin romper la app si el usuario cancela
def pedir_texto(mensaje):
    try:
        return input(mensaje).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nOperacion cancelada por el usuario")
        return None


# Lee el .env y carga las variables que encuentre
def cargar_variables_desde_env():
    archivo_env = BASE_DIR / ".env"

    if not archivo_env.exists():
        return

    try:
        with open(archivo_env, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()

                if not linea or linea.startswith("#") or "=" not in linea:
                    continue

                clave, valor = linea.split("=", 1)
                clave = clave.strip()
                valor = valor.strip().strip('"').strip("'")

                if clave and clave not in os.environ:
                    os.environ[clave] = valor
    except OSError as error:
        print(f"\nNo se pudo leer el archivo .env: {error}")


# Crea el archivo de usuarios si todavia no existe
def asegurar_archivo_usuarios():
    if USUARIOS_ARCHIVO.exists():
        return True

    try:
        with open(USUARIOS_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["username", "password_simulada"])
        return True
    except OSError as error:
        print(f"\nNo se pudo crear el archivo de usuarios: {error}")
        return False


# Crea el historial global si todavia no existe
def asegurar_archivo_historial():
    if HISTORIAL_ARCHIVO.exists():
        return True

    try:
        with open(HISTORIAL_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(
                [
                    "usuario",
                    "ciudad",
                    "fecha_hora",
                    "temperatura_c",
                    "condicion_clima",
                    "humedad_porcentaje",
                    "viento_kmh",
                ]
            )
        return True
    except OSError as error:
        print(f"\nNo se pudo crear el archivo de historial: {error}")
        return False


# Trae los usuarios guardados en el CSV
def cargar_usuarios():
    if not USUARIOS_ARCHIVO.exists() and not asegurar_archivo_usuarios():
        return {}

    try:
        usuarios = {}
        with open(USUARIOS_ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)

            for fila in reader:
                username = fila.get("username", "").strip()
                password = fila.get("password_simulada", fila.get("password", "")).strip()

                if username:
                    usuarios[username] = password

        return usuarios
    except (OSError, csv.Error) as error:
        print(f"\nNo se pudo leer el archivo de usuarios: {error}")
        return {}


# Guarda un usuario nuevo en el archivo
def guardar_usuario(username, password):
    try:
        with open(USUARIOS_ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow([username, password])
        return True
    except (OSError, csv.Error) as error:
        print(f"\nNo se pudo guardar el usuario: {error}")
        return False


# Revisa si la contrasena cumple las reglas basicas
def validar_contrasena(password):
    errores = []
    recomendaciones = []

    if len(password) < 8:
        errores.append("tener al menos 8 caracteres")
        recomendaciones.append("usa una frase corta o una palabra mas larga")

    if not any(caracter.isupper() for caracter in password):
        errores.append("incluir al menos una letra mayuscula")
        recomendaciones.append("agrega una mayuscula, por ejemplo al inicio")

    if not any(caracter.isdigit() for caracter in password):
        errores.append("incluir al menos un numero")
        recomendaciones.append("suma un numero que recuerdes facil")

    es_valida = len(errores) == 0
    return es_valida, errores, recomendaciones


# Pide usuario y contrasena para iniciar sesion
def iniciar_sesion():
    print("\n--- Iniciar sesion ---")
    username = pedir_texto("Nombre de usuario: ")
    password = pedir_texto("Contrasena: ")

    if username is None or password is None:
        return None

    usuarios = cargar_usuarios()

    if username in usuarios and usuarios[username] == password:
        print("\nInicio de sesion exitoso.")
        return username

    print("\nUsuario o contrasena incorrectos.")
    return None


# Registra un usuario nuevo y valida la contrasena
def registrar_usuario():
    print("\n--- Registrar nuevo usuario ---")
    usuarios = cargar_usuarios()

    while True:
        username = pedir_texto("Elegi un nombre de usuario: ")

        if username is None:
            return None

        if not username:
            print("El nombre de usuario no puede estar vacio.")
            continue

        if username in usuarios:
            print("Ese nombre de usuario ya existe. Proba con otro.")
            continue

        break

    print("\nLa contrasena debe cumplir estas 3 reglas:")
    print("- Tener al menos 8 caracteres")
    print("- Tener al menos una letra mayuscula")
    print("- Tener al menos un numero")

    while True:
        password = pedir_texto("\nElegi una contrasena: ")

        if password is None:
            return None

        es_valida, errores, recomendaciones = validar_contrasena(password)

        if es_valida:
            if guardar_usuario(username, password):
                print("\nUsuario registrado correctamente.")
                return username
            return None

        print("\nTu contrasena no cumple con estas reglas:")
        for error in errores:
            print(f"- {error}")

        print("Para una contrasena mas segura, considera:")
        for recomendacion in recomendaciones:
            print(f"- {recomendacion}")


# Lee todas las filas del historial global
def cargar_historial():
    if not HISTORIAL_ARCHIVO.exists() and not asegurar_archivo_historial():
        return []

    try:
        with open(HISTORIAL_ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            return list(reader)
    except (OSError, csv.Error) as error:
        print(f"\nNo se pudo leer el archivo de historial: {error}")
        return []


# Busca la key del clima en las variables cargadas
def obtener_api_key_clima():
    api_key = os.getenv("OPENWEATHER_API_KEY", "").strip()

    if api_key:
        return api_key

    print("\nNo se encontro la API key de OpenWeatherMap.")
    print("Configura la variable de entorno OPENWEATHER_API_KEY para usar esta opcion.")
    return None


# Busca la key de Gemini en las variables cargadas
def obtener_api_key_gemini():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if api_key:
        return api_key

    print("\nNo se encontro la API key de Gemini.")
    print("Configura la variable de entorno GEMINI_API_KEY para usar esta opcion.")
    return None


# Consulta OpenWeatherMap y devuelve el JSON completo
def obtener_clima_ciudad_owm(ciudad, api_key):
    parametros = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",
        "lang": "es",
    }

    try:
        respuesta = requests.get(OPENWEATHER_URL, params=parametros, timeout=10)

        if respuesta.status_code == 401:
            print("\nLa API key de OpenWeatherMap no es valida.")
            return None

        if respuesta.status_code == 404:
            print(f"\nNo se encontro la ciudad '{ciudad}'.")
            return None

        if respuesta.status_code == 429:
            print("\nSe alcanzo el limite de consultas de la API del clima.")
            return None

        if respuesta.status_code >= 500:
            print("\nEl servicio de clima no responde bien en este momento.")
            return None

        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as error:
        print(f"\nNo se pudo consultar la API del clima: {error}")
        return None
    except json.JSONDecodeError:
        print("\nLa respuesta de clima no vino en un formato valido.")
        return None


# Se queda solo con los datos del clima que usamos
def extraer_datos_clima(datos):
    if not datos:
        return None

    try:
        return {
            "ciudad": datos["name"],
            "temperatura_c": round(datos["main"]["temp"], 1),
            "sensacion_termica_c": round(datos["main"]["feels_like"], 1),
            "humedad_porcentaje": datos["main"]["humidity"],
            "condicion_clima": datos["weather"][0]["description"],
            "viento_kmh": round(datos["wind"]["speed"] * 3.6, 1),
        }
    except (KeyError, IndexError, TypeError):
        print("\nLa API devolvio datos inesperados.")
        return None


# Muestra el clima de forma clara en consola
def mostrar_datos_clima(datos_clima):
    print("\n--- Clima actual ---")
    print(f"Ciudad: {datos_clima['ciudad']}")
    print(f"Temperatura: {datos_clima['temperatura_c']} C")
    print(f"Sensacion termica: {datos_clima['sensacion_termica_c']} C")
    print(f"Humedad: {datos_clima['humedad_porcentaje']}%")
    print(f"Condicion: {datos_clima['condicion_clima']}")
    print(f"Viento: {datos_clima['viento_kmh']} km/h")


# Guarda una consulta nueva en el historial global
def guardar_consulta_en_historial(username, datos_clima):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(HISTORIAL_ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(
                [
                    username,
                    datos_clima["ciudad"],
                    fecha_hora,
                    datos_clima["temperatura_c"],
                    datos_clima["condicion_clima"],
                    datos_clima["humedad_porcentaje"],
                    datos_clima["viento_kmh"],
                ]
            )
        return True
    except (OSError, csv.Error) as error:
        print(f"\nNo se pudo guardar la consulta en el historial: {error}")
        return False


# Consulta una ciudad y guarda el resultado en el historial
def consultar_clima_y_guardar(username):
    print("\n--- Consultar clima actual ---")
    ciudad = pedir_texto("Ingresa una ciudad: ")

    if ciudad is None:
        return

    if not ciudad:
        print("La ciudad no puede estar vacia.")
        return

    api_key = obtener_api_key_clima()

    if not api_key:
        return

    datos_api = obtener_clima_ciudad_owm(ciudad, api_key)
    datos_clima = extraer_datos_clima(datos_api)

    if not datos_clima:
        return

    mostrar_datos_clima(datos_clima)

    if guardar_consulta_en_historial(username, datos_clima):
        print("\nLa consulta se guardo en el historial global.")


# Busca la ultima consulta que hizo un usuario
def obtener_ultima_consulta_usuario(username):
    historial = cargar_historial()

    for fila in reversed(historial):
        if fila.get("usuario", "").strip() == username:
            return fila

    return None


# Arma el mensaje que se le manda a Gemini
def construir_prompt_consejo(consulta):
    return f"""
Sos un asistente que da consejos cortos y practicos de vestimenta.
Responde en espanol, en 2 o 3 oraciones, de forma clara y simple.

Datos del clima:
- Ciudad: {consulta['ciudad']}
- Temperatura: {consulta['temperatura_c']} C
- Condicion: {consulta['condicion_clima']}
- Humedad: {consulta['humedad_porcentaje']}%
- Viento: {consulta['viento_kmh']} km/h

Decime como conviene vestirse hoy segun ese clima.
""".strip()


# Hace la consulta a Gemini y devuelve el texto
def obtener_consejo_con_sdk_nuevo(api_key, prompt):
    from google import genai

    modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model=modelo, contents=prompt)

    if response.text:
        return response.text.strip()

    raise ValueError("La respuesta de Gemini no trajo texto.")


# Usa datos del clima para pedir un consejo de vestimenta
def obtener_consejo_ia_gemini(
    api_key_gemini, temperatura, condicion_clima, viento, humedad
):
    consulta = {
        "ciudad": "ultima consulta",
        "temperatura_c": temperatura,
        "condicion_clima": condicion_clima,
        "humedad_porcentaje": humedad,
        "viento_kmh": viento,
    }
    prompt = construir_prompt_consejo(consulta)

    try:
        return obtener_consejo_con_sdk_nuevo(api_key_gemini, prompt)
    except ImportError:
        print("\nNo esta instalado el SDK de Gemini.")
        print("Instala las dependencias con: pip install requests google-genai")
        return None
    except Exception as error:
        print(f"\nNo se pudo generar el consejo con Gemini: {error}")
        return None


# Usa la ultima consulta del usuario para hablar con Gemini
def mostrar_consejo_ia(username):
    print("\n--- Consejo IA: como me visto hoy ---")
    ultima_consulta = obtener_ultima_consulta_usuario(username)

    if not ultima_consulta:
        print("Todavia no tenes consultas guardadas.")
        print("Primero usa la opcion 1 para consultar el clima.")
        return

    print("Se va a usar tu ultima consulta guardada:")
    print(
        f"- {ultima_consulta['fecha_hora']} | "
        f"{ultima_consulta['ciudad']} | "
        f"{ultima_consulta['temperatura_c']} C | "
        f"{ultima_consulta['condicion_clima']}"
    )

    api_key_gemini = obtener_api_key_gemini()

    if not api_key_gemini:
        return

    consejo = obtener_consejo_ia_gemini(
        api_key_gemini,
        ultima_consulta["temperatura_c"],
        ultima_consulta["condicion_clima"],
        ultima_consulta["viento_kmh"],
        ultima_consulta["humedad_porcentaje"],
    )

    if not consejo:
        return

    print("\nConsejo generado por IA:")
    print(consejo)


# Filtra el historial por usuario y por ciudad
def ver_mi_historial_por_ciudad(username):
    print("\n--- Mi historial por ciudad ---")
    ciudad = pedir_texto("Ingresa la ciudad que queres buscar: ")

    if ciudad is None:
        return

    if not ciudad:
        print("La ciudad no puede estar vacia.")
        return

    historial = cargar_historial()
    resultados = []

    for fila in historial:
        mismo_usuario = fila.get("usuario", "").strip() == username
        misma_ciudad = fila.get("ciudad", "").strip().lower() == ciudad.lower()

        if mismo_usuario and misma_ciudad:
            resultados.append(fila)

    if not resultados:
        print("\nNo hay consultas guardadas para esa ciudad.")
        return

    print(f"\nHistorial de {username} para {ciudad}:")
    for fila in resultados:
        print(
            f"- {fila['fecha_hora']} | "
            f"{fila['temperatura_c']} C | "
            f"{fila['condicion_clima']} | "
            f"Humedad {fila['humedad_porcentaje']}% | "
            f"Viento {fila['viento_kmh']} km/h"
        )


# Saca los numeros principales del historial global
def mostrar_estadisticas_globales():
    print("\n--- Estadisticas globales ---")
    historial = cargar_historial()

    if not historial:
        print("Todavia no hay consultas registradas.")
        return

    ciudades = []
    temperaturas = []

    for fila in historial:
        ciudad = fila.get("ciudad", "").strip()
        temperatura = fila.get("temperatura_c", "").strip()

        if ciudad:
            ciudades.append(ciudad)

        try:
            temperaturas.append(float(temperatura))
        except ValueError:
            pass

    total_consultas = len(historial)

    if ciudades:
        ciudad_mas_consultada, cantidad = Counter(ciudades).most_common(1)[0]
        print(f"Ciudad mas consultada: {ciudad_mas_consultada} ({cantidad} consultas)")
    else:
        print("Ciudad mas consultada: sin datos")

    print(f"Total de consultas: {total_consultas}")

    if temperaturas:
        promedio = round(sum(temperaturas) / len(temperaturas), 1)
        print(f"Temperatura promedio global: {promedio} C")
    else:
        print("Temperatura promedio global: sin datos")

    print(f"\nArchivo listo para Excel/Sheets: {HISTORIAL_ARCHIVO.name}")


# Muestra un resumen de la app y los integrantes
def mostrar_acerca_de():
    print("\n--- Acerca de GuardianClima ITBA ---")
    print("GuardianClima ITBA es una aplicacion de consola en Python")
    print("Permite registrar usuarios, consultar clima, guardar historial y ver estadisticas")
    print("\nOpciones del sistema:")
    print("- Menu de acceso: iniciar sesion, registrar usuario o salir")
    print("- Opcion 1: consulta el clima actual y guarda la consulta en el historial global")
    print("- Opcion 2: muestra tu historial filtrado por ciudad")
    print("- Opcion 3: calcula estadisticas globales usando el historial")
    print("- Opcion 4: usa Gemini para dar un consejo de vestimenta")
    print("- Opcion 5: muestra esta descripcion")
    print("- Opcion 6: cierra la sesion actual")
    print("\nNotas tecnicas:")
    print("- Los usuarios se guardan en un CSV solo para esta simulacion educativa")
    print("- En una app real, las contrasenas no se guardan en texto plano")
    print("- Los datos del clima vienen de OpenWeatherMap")
    print("- El consejo de vestimenta usa la API de Gemini")
    print("- El historial global despues sirve para hacer los graficos en Excel")
    print("\nDatos del equipo:")
    print(f"- Nombre del grupo: {NOMBRE_GRUPO}")
    print("- Integrantes:")
    for desarrollador in DESARROLLADORES:
        print(f"  - {desarrollador}")
