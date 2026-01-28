from pathlib import Path
import socket
from http_request_parser import HTTPRequest
from http_response_handler import HTTPResponseHandler


def get_default_response(numcalls):
    return f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 118
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>Example Page</title>
</head>
<body>
    <h1>Hello, World! {numcalls}</h1>
</body>
</html>
"""


class Server:
    def __init__(self, host: str, port: int, servable_files: list[Path]):
        self.host = host
        self.port = port
        self.servable_files = servable_files
        self.http_response_handler = HTTPResponseHandler()
        print(f"Starting http-server on {self.host}:{self.port}")

    def start_server(self):
        numcalls = 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            while True:
                server_socket.listen()
                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected by {conn}, {addr}")
                    while True:
                        raw_data = conn.recv(1024)
                        if not raw_data:
                            break
                        data = raw_data.decode("utf-8", errors="ignore")

                        try:
                            # print("Raw Data: ")
                            # print(data)
                            # print("**********************************")
                            http_request = HTTPRequest(data)
                            # http_response_handler = HTTPResponseHandler(http_request)
                            print(f"Parsed HTTP Request: {http_request}")

                        except ValueError as e:
                            print(
                                f"Error parsing HTTP request from {addr}: {e}\nRaw data: {data!r}"
                            )
                            break
                        conn.sendall(get_default_response(numcalls).encode("utf-8"))
                        numcalls += 1
                    print("Connection closed.")
