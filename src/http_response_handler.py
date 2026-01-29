from http import HTTPStatus
from pathlib import Path


class HttpResponse:
    """
    Builder for HTTPResponses
    """

    # message status line
    # <protocol> <status-code> <reason-phrase>
    protocol: str = "HTTP/1.1"
    status: HTTPStatus = HTTPStatus.OK
    status_code: int = status.value
    reason_phrase: str = status.phrase

    response_headers: dict[str, str] = {}

    has_content = False
    content_type: str = "text/html"
    content_length: int = 0
    content_body: str = ""

    def __init__(self):
        pass

    def set_protocol(self, protocol: str):
        self.protocol = protocol
        return self

    def set_status(self, status: HTTPStatus):
        self.status = status
        self.status_code = status.value
        self.reason_phrase = status.phrase
        return self

    def set_content(self, content_type: str, content_body: str):
        self.has_content = True
        self.content_type = content_type
        self.content_body = content_body
        self.content_length = len(content_body)
        return self

    def set_response_headers(self, response_headers: dict[str, str]):
        self.response_headers = response_headers
        return self

    def add_response_value(self, key: str, value: str):
        self.response_headers[key] = value
        return self

    def __str__(self) -> str:
        responseString = ""

        # Message status line
        responseString += f"{self.protocol} {self.status_code} {self.reason_phrase}\r\n"

        # Response Headers
        if len(self.response_headers) > 0:
            responseString += (
                "\r\n".join(
                    f"{key}: {value}" for key, value in self.response_headers.items()
                )
                + "\r\n"
            )

        if self.has_content:
            responseString += f"content-type: {self.content_type}\r\ncontent-length: {self.content_length}\r\n\r\n{self.content_body}"

        return responseString


supported_methods = {"GET", "HEAD"}
not_found_content = (
    "<!doctype html><head><title>404 not found</title><h1>404 not found</h1></head>"
)


def http_response_handler(http_request, get_file_contents):
    response = HttpResponse().set_protocol("HTTP/1.1")
    if http_request.method == "GET":
        path = http_request.path[1:]
        try:
            contents = get_file_contents(path)
        except FileNotFoundError:
            response.set_status(HTTPStatus.NOT_FOUND)
            response.set_content("text/html", not_found_content)
            return response
        response.set_status(HTTPStatus.OK)
        response.set_content("text/html", contents)
    elif http_request.method == "HEAD":
        pass
    else:
        response.set_status(HTTPStatus.METHOD_NOT_ALLOWED)
        response.set_response_headers({"Allow": "GET, HEAD"})
    return response
