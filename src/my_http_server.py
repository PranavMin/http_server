from pathlib import Path
import socket
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
    def __init__(self, host: str, port: int, servable_files: list[Path]):
        self.host = host
        self.port = port
        self.servable_files = servable_files

        # self.http_response_handler = httpresponsehandler()
        print(f"starting http-server on {self.host}:{self.port}")

    def start_server(self):
        numcalls = 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            while True:
                server_socket.listen()
                client_sock, client_addr = server_socket.accept()
                with client_sock:
                    print(f"connected by {client_sock}, {client_addr}")
                    data = ""
                    while True:
                        print("before recv")
                        raw_data = client_sock.recv(1024)
                        print("after recv")
                        if not raw_data:
                            break
                        data += raw_data.decode("utf-8", errors="ignore")
                        print(f"data = {data}")

                    # try:
                    #     http_request = httprequest(data)
                    #     print(f"parsed http request: {http_request}")
                    #     # print("raw data: ")
                    #     # print(data)
                    #     # print("**********************************")
                    #     # http_response_handler = httpresponsehandler(http_request)
                    #
                    # except valueerror as e:
                    #     print(
                    #         f"error parsing http request from {addr}: {e}\nraw data: {data!r}"
                    #     )
                    #     break
                    self.send(
                        client_sock, get_default_response(numcalls).encode("utf-8")
                    )
                    numcalls += 1
                    print("connection closed.")

    def send(self, client_sock, message):
        client_sock.sendall(message)

    def get_file_contents(self, path: Path):
        if path == Path("/"):
            return self.get_file_contents(Path("/index.html"))

        if path in self.servable_files and path.exists():
            return path.read_text()
        else:
            raise FileNotFoundError
