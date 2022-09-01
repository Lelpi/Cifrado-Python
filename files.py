"""
  FICHERO: files.py
  DESCRIPCIÓN: Manejo de ficheros con el servidor
  AUTHORS: luis.lepore@estudiante.uam.es
           oriol.julian@estudiante.uam.es
"""
import requests
import os
from encode import decrypt, enc_sign
import json

"""
  FUNCIÓN: void upload(string file_name, string destID, string token)
  ARGS_IN: file_name - Nombre del fichero a subir, se debe encontrar en la raíz del programa
           destID - ID del usuario al que el fichero va destinado
           token - Token identificador del usuario emisor
  DESCRIPCIÓN: Sube un fichero al servidor
  ARGS_OUT: void
"""
def upload(file_name, destID, token):
    # Firmar y encriptar el fichero
    if enc_sign(file_name, destID, token) == -1:
        return

    # Subir el fichero de /encrypted_files/file_name al servidor
    print('Subiendo fichero a servidor...', end='')
    url = 'http://vega.ii.uam.es:8080/api/files/upload'
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + '/encrypted_files/'
        file = open(path + file_name, 'rb')
    except:
        print('ERROR')
        print('No existe ' + file_name)
        return
    
    args = {'ufile': file}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, files=args, headers=headers)

    # Impresión del resultado
    data = json.loads(response.text)
    if response.status_code != 200:
        print('ERROR')
        print(data['description'])
    else:
        print('OK')
        print('Subida realizada correctamente, ID del fichero: ' + data['file_id'])
    
    file.close()

    # Eliminar el fichero encriptado
    os.remove(path + file_name)

"""
  FUNCIÓN: void download(string file_id, string sourceID, string token)
  ARGS_IN: file_id - Identificador del fichero a descargar
           destID - ID del usuario emisor
           token - Token identificador del usuario receptor
  DESCRIPCIÓN: Descarga un fichero del servidor
  ARGS_OUT: void
"""
def download(file_id, sourceID, token):
    # Acceso al servidor
    print('Descargando fichero a servidor...', end='')
    url = 'http://vega.ii.uam.es:8080/api/files/download'
    args = {'file_id': file_id}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, json=args, headers=headers)

    # Impresión del resultado
    if response.status_code != 200:
        print('ERROR')
        print(response.text.split('\"description\": \"')[1].split(')\"}')[0])
        return
    print('OK')
    print(response.headers['Content-Length'] + ' bytes descargados correctamente')
    # 'Content-Disposition': 'attachment; filename="prueba.txt"', nombre original del fichero subido
    fileName = response.headers['Content-Disposition'].split('"')[1]

    message = decrypt(response.content, sourceID, token)
    if message is None:
        return

    # Directorio de descargas, si no existe se crea
    downloaded_path = os.path.dirname(os.path.abspath(__file__)) + '/downloaded_files/'
    if not os.path.exists(downloaded_path):
        os.mkdir(downloaded_path);
    
    # Se crea un fichero en la carpeta del mismo nombre que el fichero original con el contenido
    encryptedFile = open(downloaded_path + fileName, 'wb')
    encryptedFile.write(message)
    encryptedFile.close()
    return

"""
  FUNCIÓN: void list_files(string token)
  ARGS_IN: token - Token identificador del usuario
  DESCRIPCIÓN: Lista los ficheros del usuario subidos en el servidor
  ARGS_OUT: void
"""
def list_files(token):
    # Acceso al servidor
    print('Listando ficheros...', end='')
    url = 'http://vega.ii.uam.es:8080/api/files/list'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, headers=headers)

    # Impresión de ficheros
    data = json.loads(response.text)
    print('OK')
    print(str(data['num_files']) + ' ficheros encontrados:')
    i = 1
    for file in data['files_list']:
        # [número] Fichero: nombre, ID: fileID
        print('[' + str(i) + '] ' +'Fichero: ' + file['fileName'] + ', ID: ' + file['fileID'] + '\n')
        i += 1

"""
  FUNCIÓN: void delete_file(string file_id, string token)
  ARGS_IN: file_id - Identificador del fichero a borrar
           token - Token identificador del usuario
  DESCRIPCIÓN: Elimina un fichero del servidor
  ARGS_OUT: void
"""
def delete_file(file_id, token):
    # Acceso al servidor
    print('Solicitando borrado del fichero #' + file_id + '...', end='')
    url = 'http://vega.ii.uam.es:8080/api/files/delete'
    args = {'file_id': file_id}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, json=args, headers=headers)

    # Impresión de resultados
    data = json.loads(response.text)
    if response.status_code != 200:
        print('ERROR')
        print(data['description'])
    else:
        print('OK')
        print('Fichero con ID#' + data['file_id'] + ' borrado correctamente')
