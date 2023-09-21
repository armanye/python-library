import datetime
import socket

import tornado.web

from prometheus_client import generate_latest

from python_library.metrics import Metrics


class DebugHandler(tornado.web.RequestHandler):
    def initialize(self, app=None):
        self._app = app

    def get(self):
        Metrics.requests_total.labels(handler="Debug").inc()

        hostname = socket.gethostname()
        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror as e:
            ip = "unknown"

        self.write(
            {
                # Useful info for debugging, hostnames and IPs are
                # infinitely useful in a containerized world.
                "ts": datetime.datetime.utcnow().isoformat(),
                "hostname": hostname,
                "ip": ip,
                "app": self._app.debug(),
            }
        )


class MetricsHandler(tornado.web.RequestHandler):
    def get(self):
        Metrics.requests_total.labels(handler="Metrics").inc()

        self.set_header("Content-Type", "text/plain")
        self.write(generate_latest())
