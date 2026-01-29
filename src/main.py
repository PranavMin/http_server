from my_http_server import Server
import sys
from pathlib import Path

HOST = "127.0.0.1"
PORT = 1338


def main():
    directory = Path(sys.argv[1])
    servable_files = list(directory.glob("**/*.html"))

    server = Server(HOST, PORT, servable_files, directory)
    server.start_server()


if __name__ == "__main__":
    main()
