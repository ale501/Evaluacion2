import requests
import urllib.parse

# Configuración de URLs locales para GraphHopper
geocode_url = "http://localhost:8082/api/1/geocode?"
route_url = "http://localhost:8082/api/1/route?"
key = "f06e9003-35bc-4b4d-b33d-10a0d35be537"

def geocoding (location, key):
    while location == "":
        location = input("Ingresa la ubicación otra vez: ")

    # Construcción de los parámetros de la URL
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    try:
        replydata = requests.get(url)
        json_data = replydata.json()
        json_status = replydata.status_code
    except Exception as e:
        print(f"Error de conexión con la API: {e}")
        return 500, "null", "null", location

    if json_status == 200 and len(json_data.get("hits", [])) != 0:
        # MEJORA 4: Narrativa en español dentro de las variables de localización
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0].get("name", location)
        value = json_data["hits"][0].get("osm_value", "Desconocido")

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(country) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name

        # MEJORA 1: Mensajes informativos de la consola en español
        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status == 200:
            json_status = 404
            print("Ubicación no encontrada: " + location)
        else:
            # Control seguro para evitar KeyError: 'message'
            error_msg = json_data.get("message", "Error sin descripción (Verifica la API Key)")
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + error_msg)

    return json_status, lat, lng, new_loc

# Ciclo principal de la aplicación
while True:
    # MEJORA 1: Textos de entrada del usuario en español
    loc1 = input("Dirección Inicial (o escribe 's'/'salir' para terminar): ")
    # MEJORA 3: Salida del programa aceptando "s", "salir", "q" o "quit"
    if loc1.lower() in ["quit", "q", "s", "salir"]:
        print("Cerrando el sistema de rutas. ¡Hasta luego!")
        break
    orig = geocoding(loc1, key)
    if orig[0] != 200:
        continue

    loc2 = input("Destino (o escribe 's'/'salir' para terminar): ")
    if loc2.lower() in ["quit", "q", "s", "salir"]:
        print("Cerrando el sistema de rutas. ¡Hasta luego!")
        break
    dest = geocoding(loc2, key)
    if dest[0] != 200:
        continue

    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        # Construcción de los puntos geográficos en la URL de la ruta
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp

        try:
            paths_response = requests.get(paths_url)
            paths_status = paths_response.status_code
            paths_data = paths_response.json()
        except Exception as e:
            print(f"Error al conectar con el servidor de rutas: {e}")
            continue

        # MEJORA 1: Consola y estados completamente traducidos al español
        print("Estado de la API de Rutas: " + str(paths_status) + "\nURL de la API de Rutas:\n" + paths_url)

        print("=================================================")
        print("Direcciones detalladas desde " + orig[3] + " hasta " + dest[3])
        print("=================================================")

        if paths_status == 200:
            km = (paths_data["paths"][0]["distance"]) / 1000
            meters = paths_data["paths"][0]["distance"]
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)

            # MEJORA 2: Formateo estricto a dos (2) decimales (`{0:.2f}`)
            print("Distancia Recorrida: {0:.2f} km / {1:.2f} m".format(km, meters))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")

            # MEJORA 4: Narrativa estructurada de las instrucciones en español
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                # Aplicación de dos decimales en el desglose por tramos
                print("{0} ( {1:.2f} km / {2:.2f} m )".format(path, distance / 1000, distance))
            print("=============================================")
        else:
            error_route = paths_data.get("message", "Error desconocido al calcular la ruta")
            print("Mensaje de error del servidor: " + error_route)
            print("*************************************************")
