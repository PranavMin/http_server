from http import HTTPStatus
import re


class HttpResponse:
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
        responseString += (
            "\r\n".join(
                f"{key}: {value}" for key, value in self.response_headers.items()
            )
            + "\r\n"
        )

        if self.has_content:
            responseString += f"content-type: {self.content_type}\r\ncontent-length: {self.content_length}\r\n\r\n{self.content_body}"

        return responseString


class HTTPResponseHandler:
    """
    A class to handle HTTP responses.
    """

    def __init__(self, status_code: int, headers: dict[str, str], body: str = ""):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.body = body

    def build_response(self) -> str:
        status_line = f"HTTP/1.1 {self.status_code} {self._get_status_message()}\r\n"
        headers = "".join(
            [f"{key}: {value}\r\n" for key, value in self.headers.items()]
        )
        blank_line = "\r\n"
        return f"{status_line}{headers}{blank_line}{self.body}"

    def _get_status_message(self) -> str:
        status_messages = {
            200: "OK",
            404: "Not Found",
            500: "Internal Server Error",
            # Add more status codes and messages as needed
        }
        return status_messages.get(self.status_code, "Unknown Status")

    def __repr__(self) -> str:
        """
        Returns a developer-friendly str representation of the HTTPResponseHandler object.
        """
        return f"{self.__class__.__name__}(status_code={self.status_code}, headers={self.headers!r}, body={self.body!r})"

    def __str__(self) -> str:
        """
        Returns a human-readable str representation of the HTTP response.
        """
        headers_str = "\n".join([f"  {k}: {v}" for k, v in self.headers.items()])
        body_str = f"\nBody:\n{self.body}" if self.body else ""

        return f"Status Code: {self.status_code}\nHeaders:\n{headers_str}{body_str}"
