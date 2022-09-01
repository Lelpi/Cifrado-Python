"""
  FICHERO: encode.py
  DESCRIPCIÓN: Firma, encriptación y desencriptación de ficheros 
               y generación de claves privada y pública
  AUTHORS: luis.lepore@estudiante.uam.es
           oriol.julian@estudiante.uam.es
"""
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import pad, unpad
import os
from users import get_public_key

PRIVFILENAME = 'privateKey.key'

"""
  FUNCIÓN: string generate_keys()
  ARGS_IN: 
  DESCRIPCIÓN: Genera un par de claves pública y privada.
               La clave privada la almacena en un fichero 
               privateKey.key y devuelve la clave pública
  ARGS_OUT: Clave pública generada
"""
def generate_keys():
    # Generar par de claves
    key = RSA.generate(2048)

    #Almacenar clave privada en privateKey.key
    privFile = open(PRIVFILENAME, 'wb')
    privFile.write(key.export_key('PEM'))
    privFile.close()
    
    return key.public_key().export_key('PEM').decode('utf-8')

"""
  FUNCIÓN: int sign(string fileName)
  ARGS_IN: fileName - Nombre del fichero a firmar
  DESCRIPCIÓN: Firma un fichero y almacena esa firma en /signed_files/fileName
  ARGS_OUT: 1 si no hay error, 
            -1 si no existe fileName o clave privada
"""
def sign(fileName):
    print('Firmando fichero...', end='')
    
    # Leer el fichero a firmar
    try:
        messageFile = open(fileName, 'rb')
    except:
        print('ERROR')
        print('No existe ' + fileName)
        return -1
    message = messageFile.read()
    messageFile.close()

    # Leer clave privada
    try:
        privFile = open(PRIVFILENAME, 'rb')
    except:
        print('ERROR')
        print('Se debe generar una clave privada')
        return -1
    key = RSA.import_key(privFile.read())
    privFile.close()

    # Hash del mensaje
    hashed_message = SHA256.new(message)

    # Directorio de firmas, si no existe se crea
    path = os.path.dirname(os.path.abspath(__file__)) + '/signed_files/'
    if not os.path.exists(path):
        os.mkdir(path);

    # Se almacena firma en /signed_files con el mismo nombre del fichero original
    signFile = open(path + fileName, 'wb')
    # Cifrado RSA
    signFile.write(pkcs1_15.new(key).sign(hashed_message))
    signFile.close()
    print('OK')
    return 1

"""
  FUNCIÓN: int encrypt(string fileName, string destID, string token)
  ARGS_IN: fileName - Nombre del fichero a encriptar
           destID - ID del usuario receptor
           token - token del usuario emisor
  DESCRIPCIÓN: Encripta un fichero y almacena ese fichero en /encrypted_files/fileName
  ARGS_OUT: 1 si no hay error, 
            -1 si no existe fileName o clave pública de destID
"""
def encrypt(fileName, destID, token):
    # Clave pública de destID
    publicKey = get_public_key(destID, token)
    if publicKey is None:
        return -1
        
    print('Cifrando fichero...', end='')
    # Leer mensaje a cifrar
    try:
        messageFile = open(fileName, 'rb')
    except:
        print('ERROR')
        print('No existe ' + fileName)
        return -1
    
    data = messageFile.read()
    messageFile.close()

    # Buscar firma del fichero, si existe se concatena la firma con el mensaje
    signed_path = os.path.dirname(os.path.abspath(__file__)) + '/signed_files/'
    if os.path.exists(signed_path + fileName):
        signFile = open(signed_path + fileName, 'rb')
        data = signFile.read() + data
        signFile.close()
        os.remove(signed_path + fileName)

    # Cifrar firma+mensaje (o mensaje) con AES
    iv = get_random_bytes(16)
    key = get_random_bytes(32)
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    encrypted = aes.encrypt(pad(data, AES.block_size))

    # Cifrar con RSA
    encryptedKey = PKCS1_OAEP.new(RSA.importKey(publicKey)).encrypt(key)
    output = iv + encryptedKey + encrypted

    # Directorio de cifrados, si no existe se crea
    encrypted_path = os.path.dirname(os.path.abspath(__file__)) + '/encrypted_files/'
    if not os.path.exists(encrypted_path):
        os.mkdir(encrypted_path);

    # Almacenar fichero cifrado en /encrypted_files
    outputFile = open(encrypted_path + fileName, 'wb')
    outputFile.write(output)
    outputFile.close()
    print('OK')
    return 1

"""
  FUNCIÓN: int enc_sign(string fileName, string destID, string token)
  ARGS_IN: fileName - Nombre del fichero a encriptar
           destID - ID del usuario receptor
           token - token del usuario emisor
  DESCRIPCIÓN: Firma y encripta un fichero y almacena ese fichero en /encrypted_files/fileName
  ARGS_OUT: 1 si no hay error, 
            -1 si no existe fileName, clave pública de destID o token
"""
def enc_sign(fileName, destID, token):
    if sign(fileName) == -1:
        return -1

    return encrypt(fileName, destID, token)

"""
  FUNCIÓN: string decrypt(string text, string sourceID, string token)
  ARGS_IN: text - Texto a desencriptar
           sourceID - ID del usuario emisor
           token - Token del usuario receptor
  DESCRIPCIÓN: Desencripta un fichero
  ARGS_OUT: El texto desencriptado si no hay error, None en otro caso
"""
def decrypt(text, sourceID, token):
    print('Descifrando fichero...', end='')
    
    iv = text[0:16]
    key = text[16:272]
    signedMessage = text[272:]

    # Obtener clave privada
    try:
        privFile = open(PRIVFILENAME, 'rb')
    except:
        print('ERROR')
        print('Se debe generar una clave privada')
        return None
    privateKey = RSA.import_key(privFile.read())

    # Descifrar clave AES con RSA
    try:
        key = PKCS1_OAEP.new(privateKey).decrypt(key)
    except:
        print('ERROR')
        print('Clave privada incorrecta, este mensaje no es para ti')
        return None

    # Descifrar mensaje con AES
    aes = AES.new(key, AES.MODE_CBC, iv=iv)
    try:
        signedMessage = unpad(aes.decrypt(signedMessage), AES.block_size)
    except:
        print('ERROR')
        print('Clave simétrica incorrecta')
        return None

    print('OK')
    
    sign = signedMessage[0:256]
    message = signedMessage[256:]

    # Obtener clave pública del emisor
    publicKey = get_public_key(sourceID, token)
    if publicKey is None:
        return None

    # Verificar firma
    print('Verificando firma...', end='')
    publicKey = RSA.import_key(publicKey)
    hashed_message = SHA256.new(message)
    try:
        pkcs1_15.new(publicKey).verify(hashed_message, sign)
    except:
        print('ERROR')
        print('Firma no válida')
        return None
    
    print('OK')
    return message
