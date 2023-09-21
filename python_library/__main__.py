import argparse
import logging
import time

import tornado.ioloop
import tornado.web

from python_library.handlers import DebugHandler


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # ALWAYS LOG TIME IN UTC
    logging.Formatter.converter = time.gmtime

    formatter = logging.basicConfig(
        format="%(asctime)s.%(msecs)03dZ %(threadName)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=logging.INFO,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, help="port to listen on")

    args = parser.parse_args()

    port = args.port

    routes = [
        (r"/debugz", DebugHandler),
    ]

    settings = {
        "autoreload": True,
    }

    app = tornado.web.Application(routes, **settings)
    app.listen(port, "0.0.0.0")
    logger.info("Listening on: %s", port)

    tornado.ioloop.IOLoop.current().start()
