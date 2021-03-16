import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index, delete_req, update_req, update_return

CUR_DIR = Path(__file__).parent
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8008

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    route = extract_route(request)
    
    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request)
    elif route == 'delete':
        response = delete_req(request)  
    elif (route == 'update'):
        response = update_req(request)   
    elif (route == 'return'):
        response = update_return(request)             
    else:
        response = build_response()
    if response is not None:    
        client_connection.sendall(response)

    client_connection.close()

server_socket.close()