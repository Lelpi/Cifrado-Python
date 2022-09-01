"""
  FICHERO: main.py
  DESCRIPCIÓN: Fichero principal del programa
  AUTHORS: luis.lepore@estudiante.uam.es
           oriol.julian@estudiante.uam.es
"""
import argparse
from files import *
from users import *
from encode import *

TOKENFILE = 'token.txt'

"""
  FUNCIÓN: void parse_arguments(string token)
  ARGS_IN: token - Token identificador del usuario
  DESCRIPCIÓN: Parsing de los parámetros pasados en la ejecución
  ARGS_OUT: void
"""
def parse_arguments(token):
    parser = argparse.ArgumentParser()

    # Gestión de Usuarios
    parser.add_argument('--create_id', nargs=2)
    parser.add_argument('--search_id', nargs=1)
    parser.add_argument('--delete_id', nargs=1)

    # Ficheros
    parser.add_argument('--upload', nargs=1)
    parser.add_argument('--source_id', nargs=1)
    parser.add_argument('--dest_id', nargs=1)
    parser.add_argument('--list_files', action='store_true', default=None)
    parser.add_argument('--download', nargs=1)
    parser.add_argument('--delete_file', nargs=1)

    # Cifrado y Firma
    parser.add_argument('--encrypt', nargs=1)
    parser.add_argument('--sign', nargs=1)
    parser.add_argument('--enc_sign', nargs=1)

    args = parser.parse_args()

    if args.upload is not None:
        if args.dest_id is not None:
            upload(args.upload[0], args.dest_id[0], token)
        else:
            print('Se debe introducir un ID de destino')
            
    elif args.list_files is not None:
        list_files(token)
        
    elif args.download is not None:
        if args.source_id is not None:
            download(args.download[0], args.source_id[0], token)
        else:
            print('Se debe introducir un ID de origen')
            
    elif args.delete_file is not None:
        delete_file(args.delete_file[0], token)
        
    elif args.create_id is not None:
        create_id(args.create_id[0], args.create_id[1], token)
        
    elif args.search_id is not None:
        search_id(args.search_id[0], token)
        
    elif args.delete_id is not None:
        delete_id(args.delete_id[0], token)
        
    elif args.sign is not None:
        sign(args.sign[0])
        
    elif args.encrypt is not None:
        if args.dest_id is not None:
            encrypt(args.encrypt[0], args.dest_id[0], token)
        else:
            print('Se debe introducir un ID de destino')
            
    elif args.enc_sign is not None:
        if args.dest_id is not None:
            enc_sign(args.enc_sign[0], args.dest_id[0], token)
        else:
            print('Se debe introducir un ID de destino')
    
    return

def main():
    # Get token
    if not os.path.exists(TOKENFILE):
        token = input('Introduce tu token: ')
        file = open(TOKENFILE, 'w')
        file.write(token)
        file.close()
    else:
        file = open(TOKENFILE, 'r')
        token = file.read()
        file.close()

    parse_arguments(token)

if __name__ == "__main__":
    main()
