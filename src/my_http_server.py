import socket
from pathlib import Path

from http_request_parser import HTTPRequest
from http_response_handler import HttpResponse, http_response_handler

# from http_request_parser import HTTPRequest
# from http_response_handler import HTTPResponseHandler


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
    def __init__(
        self, host: str, port: int, servable_files: list[Path], directory: Path
    ):
        self.host = host
        self.port = port
        self.servable_files = servable_files
        self.root_dir = directory

        # self.http_response_handler = httpresponsehandler()
        print(f"starting http-server on {self.host}:{self.port}")

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            self.server_loop(server_socket)

    def server_loop(self, server_socket):
        while True:
            server_socket.listen()
            client_sock, client_addr = server_socket.accept()
            with client_sock:
                print(f"connected by {client_sock}, {client_addr}")
                data = ""
                while True:
                    raw_data = client_sock.recv(1024)
                    if not raw_data:
                        break
                    data = raw_data.decode("utf-8", errors="ignore")

                    print(f"got data: ********** \n {data}\n*************")
                    try:
                        http_request = HTTPRequest(data)
                        response = http_response_handler(
                            http_request, self.get_file_contents
                        )
                        print(f"trying to send {response}")
                        self.send(client_sock, str(response).encode("utf-8"))
                    except ValueError as e:
                        print(
                            f"error parsing http request from {client_addr}: {e}\nraw data: {data!r}"
                        )
                        break

                print("connection closed.")

    def send(self, client_sock, message):
        client_sock.sendall(message)

    def get_file_contents(self, relative_path: Path):
        absolute_path = Path(self.root_dir, relative_path)
        print(f"get_file_contents called with path: {absolute_path}")

        # Handle root request
        if relative_path == "" or relative_path == "/":
            return (self.root_dir / "index.html").read_text()

        # Handle other requests
        if absolute_path in self.servable_files and absolute_path.exists():
            return absolute_path.read_text()
        else:
            # This should mean 404
            raise FileNotFoundError
