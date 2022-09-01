"""
  FICHERO: users.py
  DESCRIPCIÓN: Gestión de usuarios del servidor
  AUTHORS: luis.lepore@estudiante.uam.es
           oriol.julian@estudiante.uam.es
"""
import requests
import json

"""
  FUNCIÓN: void create_id(string username, string email, string token)
  ARGS_IN: username - nombre de usuario del servidor
           email - email del usuario del servidor
           token - Token identificador del usuario
  DESCRIPCIÓN: Añade una nueva cuenta de usuario en el servidor
  ARGS_OUT: void
"""
def create_id(username, email, token):
    # Para evitar imports circulares
    from encode import generate_keys
    publicKey = generate_keys()

    # Acceso al servidor
    url = 'http://vega.ii.uam.es:8080/api/users/register'
    args = {'nombre': username, 'email': email, 'publicKey': publicKey}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, json=args, headers=headers)

    # Impresión del resultado
    data = json.loads(response.text)
    if response.status_code != 200:
        print('ERROR')
        print(data['description'])
    else:
        print('OK')
        print('Identidad con ID#' + data['userID'] + ' creada correctamente')

"""
  FUNCIÓN: string get_public_key(string userID, string token)
  ARGS_IN: userID - Identificador del usuario a buscar
           token - Token identificador de tu usuario
  DESCRIPCIÓN: Obtiene la clave pública de un usuario en concreto
  ARGS_OUT: Clave pública del usuario
            None si hay algún error
"""
def get_public_key(userID, token):
    # Acceso al servidor
    print('Buscando clave pública de ' + '\'' + userID + '\' en el servidor...', end='')
    url = 'http://vega.ii.uam.es:8080/api/users/getPublicKey'
    args = {'userID': userID}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, json=args, headers=headers)

    # Impresión de errores
    data = json.loads(response.text)
    if response.status_code != 200:
        print('ERROR')
        print(data['description'])
        return None
    if data['publicKey'] is None:
        print('ERROR')
        print('El usuario no tiene clave pública')
        return None
    print('OK')
    return data['publicKey']

"""
  FUNCIÓN: void search_id(string data_search, string token)
  ARGS_IN: data_search - Cadena de búsqueda
           token - Token identificador de tu usuario
  DESCRIPCIÓN: Imprime los usuarios donde su nombre o email
               contenga data_search
  ARGS_OUT: void
"""
def search_id(data_search, token):
    # Acceso al servidor
    print('Buscando usuario ' + '\'' + data_search + '\' en el servidor...', end='')
    url = 'http://vega.ii.uam.es:8080/api/users/search'
    args = {'data_search': data_search}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, json=args, headers=headers)

    # Impresión de usuarios
    data = json.loads(response.text)
    print('OK')
    print(str(len(data)) + ' usuarios encontrados:')
    i = 1
    for user in data:
        if user['publicKey'] is not None:
            # [número] nombre, email, ID: id, Key: clave pública
            print('[' + str(i) + '] ' + user['nombre'] + ', ' + user['email'] + ', ID: ' + user['userID'] + ', Key: ' + user['publicKey'] + '\n')
            i += 1

"""
  FUNCIÓN: void delete_id(string userID, string token)
  ARGS_IN: userID - ID del usuario
           token - Token identificador de tu usuario
  DESCRIPCIÓN: Elimina el usuario con identificador userID 
               si el token es el pasado como argumento.
  ARGS_OUT: void
"""
def delete_id(userID, token):
    # Acceso al servidor
    print('Solicitando borrado de la identidad #' + userID + '...', end='')
    url = 'http://vega.ii.uam.es:8080/api/users/delete'
    args = {'userID': userID}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(url, json=args, headers=headers)

    #Impresión del resultado
    data = json.loads(response.text)
    if response.status_code != 200:
        print('ERROR')
        print(data['description'])
    else:
        print('OK')
        print('Identidad con ID#' + data['userID'] + ' borrada correctamente')
