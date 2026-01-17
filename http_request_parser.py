class HTTPRequestParser:
    def __init__(self, raw_request: str):
        self.raw_request = raw_request
        self.method = ""
        self.path = ""
        self.http_version = ""
        self.methodpathversion = ""
        self.headers = {}
        self.body = ""
        self.parse_request()

    def parse_request(self):
        if not self.raw_request:
            # An empty raw request is not a valid HTTP request.
            # Given main.py now checks for empty raw_data, this might be redundant but good for robustness.
            return

        request_lines = self.raw_request.split("\r\n")

        if not request_lines or not request_lines[0]:
            # This handles cases like an empty string, or a request starting with "\r\n"
            # which would make the first line empty.
            raise ValueError("Empty or missing HTTP request line.")

        request_line = request_lines[0]
        parts = request_line.split(" ")

        if len(parts) != 3:
            # Malformed request line, e.g., "GET /" or just "GET"
            # Raise an error to indicate a parsing failure.
            raise ValueError(f"Malformed HTTP request line: '{request_line}'. Expected 3 parts (method, path, version). Got {len(parts)}.")

        self.method, self.path, self.http_version = parts
        # self.methodpathversion = request_line

        header_lines = []
        body_lines = []
        is_body = False

        for line in request_lines[1:]:
            if line == "":
                is_body = True
                continue
            if is_body:
                body_lines.append(line)
            else:
                # Ensure header lines contain a colon to be valid
                if ":" not in line:
                    print(f"Warning: Skipping malformed header line: '{line}'")
                    continue # Skip this line as it's not a valid header
                header_lines.append(line)

        for header in header_lines:
            # Use split(":", 1) to handle cases where header values might contain colons
            key, value = header.split(":", 1) 
            self.headers[key.strip().lower()] = value.strip() # Convert header keys to lowercase for consistency

        self.body = "\r\n".join(body_lines)

    def get_method(self) -> str:
        return self.method

    def get_path(self) -> str:
        return self.path

    def get_http_version(self) -> str:
        return self.http_version

    def get_headers(self) -> dict:
        return self.headers

    def get_body(self) -> str:
        return self.body

    def __repr__(self) -> str:
        """
        Returns a developer-friendly string representation of the HTTPRequestParser object.
        """
        return f"{self.__class__.__name__}(raw_request={self.raw_request!r})"

    def __str__(self) -> str:
        """
        Returns a human-readable string representation of the parsed HTTP request.
        """
        headers_str = "\n".join([f"  {k}: {v}" for k, v in self.headers.items()])
        body_str = f"\nBody:\n{self.body}" if self.body else ""

        return (
            f"Method: {self.method}\n"
            f"Path: {self.path}\n"
            f"HTTP Version: {self.http_version}\n"
            # f"methodpathversion: {self.methodpathversion}\n"
            f"Headers:\n{headers_str}{body_str}"
        )