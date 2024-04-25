import base64
import os
from cryptography.fernet import Fernet


def encrypt_dict(diccionario,clave):
    # Crear la clave de cifrado de Fernet
    clave_fernet = Fernet(clave)

    # Crear un nuevo diccionario para almacenar los valores encriptados
    diccionario_encriptado = {}

    # Recorrer cada clave y valor del diccionario original
    for clave, valor in diccionario.items():
        # Convertir el valor a una cadena y codificarlo en UTF-8
        valor_str = str(valor)
        valor_bytes = valor_str.encode('utf-8')

        # Encriptar el valor utilizando la clave de Fernet
        valor_encriptado = clave_fernet.encrypt(valor_bytes)

        # Almacenar el valor encriptado en el nuevo diccionario
        diccionario_encriptado[clave] = valor_encriptado.decode('utf-8')

    return diccionario_encriptado


def decrypt_dict(diccionario_encriptado,clave):
    clave_fernet = Fernet(clave)

    # Crear un nuevo diccionario para almacenar los valores desencriptados
    diccionario_desencriptado = {}

    # Recorrer cada clave y valor del diccionario encriptado
    for clave, valor_encriptado in diccionario_encriptado.items():
        if type(valor_encriptado) != str: continue
        # Decodificar el valor encriptado en bytes
        valor_bytes = valor_encriptado.encode('utf-8')

        # Desencriptar el valor utilizando la clave de Fernet
        valor_desencriptado = clave_fernet.decrypt(valor_bytes)

        # Convertir el valor desencriptado a una cadena y decodificarlo en UTF-8
        valor_str = valor_desencriptado.decode('utf-8')

        # Almacenar el valor desencriptado en el nuevo diccionario
        diccionario_desencriptado[clave] = valor_str

    return diccionario_desencriptado
