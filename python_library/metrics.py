from prometheus_client import Counter


class Metrics:
    requests_total = Counter(
        "python_library_http_requests_total",
        "HTTP Requests total",
        labelnames=["handler"],
    )
