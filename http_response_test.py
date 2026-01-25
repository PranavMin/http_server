from http import HTTPStatus
from http_response_handler import HttpResponse


if __name__ == "__main__":
    http_response = (
        HttpResponse()
        .set_content("txt/html", "<html><h1>Header 1</h1></html>")
        .set_response_headers({"ResponseHeader1Key": "ResponseHeader1Value"})
        .set_status(HTTPStatus.FOUND)
        .set_protocol("HTTP 6.7")
    )
    print(http_response)
