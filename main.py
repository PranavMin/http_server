import socket
from http_request_parser import HTTPRequestParser
HOST = "127.0.0.1"
PORT = 1339

default_response = """HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 118
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>Example Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
"""

def main():
    print(f"Starting http-server on {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {conn}, {addr}")
            while True:
                raw_data = conn.recv(1024)
                if not raw_data:
                    break
                data = raw_data.decode('utf-8', errors='ignore')
                
                try: 
                    my_http_request_parser = HTTPRequestParser(data)
                    print(f"Parsed HTTP Request: {my_http_request_parser}")
                except ValueError as e:
                    print(f"Error parsing HTTP request from {addr}: {e}\nRaw data: {data!r}")
                    break
                conn.sendall(default_response.encode('utf-8'))
            print("Connection closed.")


if __name__ == "__main__":
    main()
