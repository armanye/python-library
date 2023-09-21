import argparse
import logging
import time

import tornado.ioloop
import tornado.web

from python_library import App
from python_library.handlers import DebugHandler, MetricsHandler


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # ALWAYS LOG TIME IN UTC
    logging.Formatter.converter = time.gmtime

    formatter = logging.basicConfig(
        format="%(asctime)s.%(msecs)03dZ %(threadName)s %(levelname)s:%(name)s:%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        level=logging.INFO,
    )

    # Silence tornado access logs since we have prometheus metrics
    logging.getLogger("tornado.access").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int, help="port to listen on")
    parser.add_argument(
        "--interval", default=60, type=int, help="number of seconds to run work loop on"
    )

    args = parser.parse_args()

    app = App(interval=args.interval)
    future_loop = app.loop()

    # raise exception in the loop if it fails
    future_loop.add_done_callback(lambda f: f.result())

    # stop main thread when loop is done
    future_loop.add_done_callback(lambda f: app._mainloop.stop())

    port = args.port

    opts = {
        "app": app,
    }

    routes = [
        (r"/debugz", DebugHandler, opts),
        (r"/metrics", MetricsHandler),
    ]

    settings = {
        "autoreload": True,
    }

    app = tornado.web.Application(routes, **settings)
    app.listen(port, "0.0.0.0")
    logger.info("Listening on: %s", port)

    tornado.ioloop.IOLoop.current().start()
