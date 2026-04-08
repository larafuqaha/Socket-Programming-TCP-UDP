# Lara Foqaha 1220071 / Fadi Bassous 1221005 / Veronica Wakileh 1220245
import socket
import threading
import os

MAX_CONNECTION_NUM = 20 # maximum number of connections

def get_content_type(file_name):
    #determine the content type based on the file extension
    if file_name.endswith(".html"):
        return "text/html"
    elif file_name.endswith(".css"):
        return "text/css"
    elif file_name.endswith(".png"):
        return "image/png"
    elif file_name.endswith(".jpg"):
        return "image/jpeg"
    elif file_name.endswith(".mp4"):
        return "video/mp4"
    return "application/octet-stream" # default


def handle_request(client_socket, client_address):
    client_ip = client_address[0]  # client IP 
    client_port = client_address[1]  # client port
    request = client_socket.recv(1024) # Receiving a message from client socket with maximum size = 1024 bytes 
    request = request.decode('utf-8') # Decode request message 
    print("Received Request:")
    print(request)

    request_lines = request.split("\r\n")
    request_line = request_lines[0] # the first line contains method and path
    method, path, _ = request_line.split(" ",2) # saving the first part in method and the second in path

    if (path == "/" or path == "/en" or path == "/main_en.html" or path == "/index.html"): 
        path = "main_en.html"
    elif (path == "/ar" or path == "/main_ar.html"):
        path = "main_ar.html"
    elif "file-name=" in path:
        temp,path = path.split("=",2)
    else:
        path = path.lstrip("/")

    
    if os.path.exists(path):
        file = open(path, "rb")
        content = file.read()
        file.close()
        response_header = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {get_content_type(path)}\r\n"
                f"Content-Length: {len(content)}\r\n\r\n"
            )
        response = response_header.encode() + content
    else:
        if path.endswith((".jpg",".png")):
            name = path.split(".", 1)[0]  # extract file name without extension
            redirect_url = f"https://www.google.com/search?q={name}&udm=2"
            response_header = (
                "HTTP/1.1 307 Temporary Redirect\r\n"
                f"Location: {redirect_url}\r\n\r\n"
            )
            response = response_header.encode()
            
        elif path.endswith(".mp4"):
            name = path.split(".", 1)[0]  # extract file name without extension
            redirect_url = f"https://www.youtube.com/results?search_query={name}"
            response_header = (
                "HTTP/1.1 307 Temporary Redirect\r\n"
                f"Location: {redirect_url}\r\n\r\n"
            )
            response = response_header.encode()
        
        else:
            path = "Error_404.html"
            file = open(path,"rb")
            content = file.read()
            file.close()
            content = content.replace(b"{CLIENT_IP}", client_ip.encode())
            content = content.replace(b"{CLIENT_PORT}", str(client_port).encode())
            response_header = (
                    "HTTP/1.1 404 Not Found\r\n"
                    f"Content-Type: {get_content_type(path)}\r\n"
                    f"Content-Length: {len(content)}\r\n\r\n"
                )
            response = response_header.encode() + content

    client_socket.sendall(response)
    client_socket.close()
    

port = 5698
host_ip_client_addressess = socket.gethostbyname(socket.gethostname())   # Getting the current device's IP client_addressess
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initiating a TCP server socket

server_socket.bind((host_ip_client_addressess, port))  #Bindong the socket with the IP and port Number
server_socket.listen(MAX_CONNECTION_NUM)  # here maximum number of connections = 20
print(f"Server running on {host_ip_client_addressess}:{port}\n")

try:   
    while True:
        client_socket, client_address = server_socket.accept() # Handle the TCP connection request from Upcoming Clients
        client_thread = threading.Thread(target=handle_request, args=(client_socket, client_address)) # each client has a different thread
        client_thread.start() 
except KeyboardInterrupt:
    print("Shutting down the server...")
    server_socket.close()