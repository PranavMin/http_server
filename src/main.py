from my_http_server import Server
import sys
from pathlib import Path

HOST = "127.0.0.1"
PORT = 1337


def main():
    directory = Path(sys.argv[1])
    if len(sys.argv) > 2:
        global PORT
        PORT = int(sys.argv[2])
    servable_files = list(directory.glob("**/*.html"))

    server = Server(HOST, PORT, servable_files, directory)
    server.start_server()


if __name__ == "__main__":
    main()
