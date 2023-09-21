import json
import logging
import multiprocessing
import time

from concurrent.futures import ThreadPoolExecutor

from tornado.concurrent import run_on_executor
from tornado.ioloop import IOLoop

from python_library.util import JSONEncoder

logger = logging.getLogger(__name__)


class App:
    _max_threads = multiprocessing.cpu_count() * 2
    _executor = ThreadPoolExecutor(max_workers=_max_threads, thread_name_prefix="app")

    def __init__(self, interval=None):
        logger.info(f"executor set max_workers to {self._max_threads}")
        self._interval = interval
        logger.info(f"interval set to {self._interval}")

        # This is the main loop that will be stopped when the work loop is done.
        self._mainloop = IOLoop.current()

        # Keep track if we hae to kill the loop
        self._running = True

    def debug(self):
        """Return all class variables.

        Useful for debugging.
        """
        return json.loads(json.dumps(self, cls=JSONEncoder))

    @run_on_executor(executor="_executor")
    def loop(self):
        """Run a blocking timing loop in a separate thread."""
        now = int(time.time())
        next_interval = (now // self._interval + 1) * self._interval
        sleep_delay = next_interval - now
        time.sleep(sleep_delay)

        while self._running:
            try:
                self.work()
            except Exception as e:
                logger.error(e)
                self._running = False

            if not self._running:
                break

            now = int(time.time())
            next_interval = (now // self._interval + 1) * self._interval
            sleep_delay = next_interval - now

            # Make sure we arent out of bounds, if we are, don't delay
            # and run the next interval immedaiately.
            if sleep_delay > 0:
                time.sleep(sleep_delay)
            else:
                logging.error("work() took longer than the interval time.")

    def work(self):
        logger.info("Working")
