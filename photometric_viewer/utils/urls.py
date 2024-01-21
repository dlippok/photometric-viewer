from urllib.parse import urlparse


def is_url(url):
    parse_result = urlparse(url)
    if parse_result.scheme not in {"http", "https"}:
        return False
    return bool(parse_result.netloc)
