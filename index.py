import Crypto
from base64 import b64decode
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')

def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a

def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()

def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print()

def menu_principal():
    opciones = {
        '1': ('Generar Llaves RSA.', generateRSAKeys),
        '2': ('Encriptar Información Sensible.', encryptRSA),
        '3': ('Descifrar Información Recibida', decryptRSA),
        '4': ('Salir del Programa', salir)
    }
    generar_menu(opciones, '4')

def generateRSAKeys():
    random_generator = Crypto.Random.new().read

    private_key = RSA.generate(2048, random_generator)
    public_key = private_key.publickey()

    name_key_private = "private"
    name_key_public = "public"

    with open (name_key_private + ".key", "wb") as prv_file:
        prv_file.write(private_key.exportKey("PEM"))

    with open (name_key_public + ".crt", "wb") as pub_file:
        pub_file.write(public_key.exportKey("PEM"))
    
    print("Llaves generadas exitosamente.")

def encryptRSA():
    message = "Mensaje de prueba"
    name_file_key = "public"

    with open( name_file_key + ".crt", 'rb') as key_file:
        key = RSA.importKey(key_file.read())

    cipher = PKCS1_OAEP.new(key)
    message_encrypted = cipher.encrypt(message.encode())
    encode = b64encode(message_encrypted).decode("UTF-8")
    print(encode)

def decryptRSA():
    # NOTA: Es necesario realizar el proceso con un bloque de datos que hayan usado los mismos certificados para cifrar.
    encrypted_message = "IM3HQ41rHg5gi4grq/xWfcaNz1XV2Tsnmo+a3avxzr0oWAELNkoN2H6GAvNoUerVAgIJhnV7fkKMbfPzdc6pl9tjcXb/d3Vi88WVjzZz8/mece7sZvGLk4p0B/osDUZj9rPUW9kdnhUxE9A6h2XtCFMWISq8dmu4loG7BCWYV+etN/rXIweLmQmHKXzk+GNDuP/cS6ddaWfl92wvsRYWDKdCrGIWMJTyP6lUmUniosY8/5pEknMIRzaeMUXGqtVZiSX4Jrih7IevxvmgLxJz/duMLMWKwdQercJzVo0kH2NQ8MHiiI7ei3YSIR/Sn7LZ88Sqen2XI3luXAUM9hRweA=="
    encrypted_message = b64decode(encrypted_message.encode())

    name_file_key = "private"
    with open( name_file_key + ".key", 'rb') as key_file:
        key = RSA.importKey(key_file.read())

    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(encrypted_message)
    print(message)
    # encryptedNumber =  int.from_bytes(encrypted_message, 'big')
    # decryptedNumber = key._decrypt(encryptedNumber)
    # decryptedData = decryptedNumber.to_bytes(key.size_in_bytes(), 'big')
    # print(decryptedData.decode('unicode_escape').encode('utf-8'))

def salir():
    print('Saliendo')

if __name__ == '__main__':
    menu_principal()
