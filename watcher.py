import redis
import time
import json
import threading
import logging
from pprint import pprint

class PlayQueueWatcher:
    def __init__(self, host, port, password=None, debug=False, wait=5):
        """

        :param host:
        :param port:
        :param password:
        :param debug:
        :param wait:
        """
        if debug:
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        self._stop_event = threading.Event()
        self._worker = None

        self._conn = self._connect(host, port, password)
        self._wait = wait

    def get_redis_conn(self):
        return self._conn

    def _connect(self, host, port, password):
        """
        Returns redis connection object
        """
        pool = redis.ConnectionPool(host=host, port=port, db=0, password=password)
        r = redis.StrictRedis(connection_pool=pool)
        r.client_list() # Health check
        logging.debug("Redis connection established.")
        return r

    def start(self, callback, with_thread=False):
        """
        Start worker
        :param callback: callback function (having arguments "data")
        :param with_thread: start worker with thread or not
        :return:
        """
        if with_thread:
            logging.debug("Worker status: thread mode")
            self._worker = threading.Thread(target=self._start_worker_with_thread, args=(callback,))
            self._worker.start()
        else:
            logging.debug("Worker status: normal mode")
            self._start_worker(callback)

    def stop(self):
        if self._worker:
            self._stop_event.set() # set stop flag
            self._worker.join() # wait until thread stopping

    def _start_worker(self, callback):
        """
        Start worker
        :param callback: callback function
        :return:
        """
        while True:
            for data in self._dequeue():
                if data:
                    logging.debug("Received data.")
                    logging.debug(data)
                    callback(data) # call callback function
                    time.sleep(int(data["song"]["time"]) + self._wait)  # Wait for time saved in queue
                else:
                    logging.debug("No data in queue.")

    def _start_worker_with_thread(self, callback):
        """
        Start worker
        :param callback: callback function
        :return:
        """
        while not self._stop_event.is_set():
            for data in self._dequeue():
                if data:
                    logging.debug("Received data.")
                    logging.debug(data)
                    callback(data) # call callback function
                    time.sleep(int(data["song"]["time"]) + self._wait)  # Wait for time saved in queue
                else:
                    logging.debug("No data in queue.")

    def _dequeue(self) -> dict:
        """
        Dequeue from queue in redis after waiting for a while.
        """
        while True:
            keys = self._conn.keys()
            if len(keys) == 0:
                yield None
                continue
            key = keys[0]
            data = self._conn.get(key)
            data = json.loads(data)
            yield data
            self._conn.delete(key)

    def __del__(self):
        self.stop()

