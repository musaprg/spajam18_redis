import toml
import watcher
import signal
import watcher
import requests
import os
from argparse import ArgumentParser

parser = ArgumentParser(description="QueueWatchClient")
parser.add_argument("path_to_google_home", type=str, help="URL to Google Home")
parser.add_argument("--local", action='store_true', help="Run with using local redis server")
parser.add_argument("--debug", action='store_true', help="Run with debug mode")
parser.add_argument("--wait", type=int, help="Wait time between songs [sec]")

# TODO: Implements multi target selection available
# TARGET = []
TARGET = None
TRYTIMES = 3

def callback(data):
    """
    callback function
    :param data: parsed json data (dict)
    :return:
    """
    for i in range(TRYTIMES):
        params = {"text":data["song"]["music_url"]}
        res = requests.get(TARGET, params=params)
        if res.status_code == requests.codes.ok:
            return
    raise TimeoutError

if __name__ == '__main__':
    args = parser.parse_args()
    TARGET = args.path_to_google_home

    conf = toml.load(os.path.join(os.path.dirname(__file__), "config.toml"))
    if args.local:
        host = conf["redis-local"]["ip"]
        port = conf["redis-local"]["port"]
        password = None
    else:
        host = conf["redis"]["ip"]
        port = conf["redis"]["port"]
        password = conf["redis"]["password"]

    w = watcher.PlayQueueWatcher(host, port, password=password, debug=args.debug, wait=args.wait)
    w.start(callback, with_thread=False)