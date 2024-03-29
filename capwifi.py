import subprocess
import os

def obtener_contraseñas_wifi():
    # Obtener la lista de perfiles de Wi-Fi
    perfiles = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    nombres_perfiles = [linea.split(':')[1].strip() for linea in perfiles if "Perfil de todos los usuarios" in linea]

    # Obtener las contraseñas de los perfiles de Wi-Fi
    contraseñas = []
    for nombre in nombres_perfiles:
        try:
            resultado = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', 'name="' + nombre + '"', 'key=clear']).decode('latin-1').split('\n')
            linea_contraseña = [linea.split(':')[1].strip() for linea in resultado if "clave" in linea][0]
            contraseñas.append((nombre, linea_contraseña))
        except subprocess.CalledProcessError:
            contraseñas.append((nombre, "No se pudo obtener la contraseña"))

    return contraseñas

def guardar_contraseñas_en_archivo(contraseñas, nombre_archivo):
    ruta_archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre_archivo)
    with open(ruta_archivo, 'w') as archivo:
        for nombre, contraseña in contraseñas:
            archivo.write(f"Nombre de red: {nombre}\nContraseña: {contraseña}\n\n")
    print(f"Las contraseñas se han guardado en el archivo '{ruta_archivo}'.")

# Ejecutar la función para obtener las contraseñas y guardarlas en un archivo
contraseñas = obtener_contraseñas_wifi()
guardar_contraseñas_en_archivo(contraseñas, 'contraseñas_wifi.txt')