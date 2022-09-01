# Práctica 2 - REDES2
**Autores: Oriol Julián y Luis Lepore** <br />
## Instrucciones de ejecución

Al ejecutar el main.py se comprueba la existencia de un fichero "token.txt", si no existe se le pedirá al usuario que introduzca su token por teclado y se almacenará en el fichero correspondiente (para generar el token hay que ir a la URL: http://vega.ii.uam.es:8080).

argumentos: main.py [-h] [--create_id CREATE_ID CREATE_ID] [--search_id SEARCH_ID]<br />
                    [--delete_id DELETE_ID] [--upload UPLOAD]<br />
                    [--source_id SOURCE_ID] [--dest_id DEST_ID] [--list_files]<br />
                    [--download DOWNLOAD] [--delete_file DELETE_FILE]<br />
                    [--encrypt ENCRYPT] [--sign SIGN] [--enc_sign ENC_SIGN]<br />

Los comandos "upload", "encrypt" y "enc_sign" necesitarán que además especifique un ID a través de "dest_id".<br />
El comando "download" necesitará que se especifique un ID a través de "source_id".<br />
