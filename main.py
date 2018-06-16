import toml
import watcher
import signal
import watcher
import requests
from argparse import ArgumentParser

parser = ArgumentParser(description="QueueWatchClient")
parser.add_argument("path_to_google_home", type=str, help="URL to Google Home")

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
        # res = requests.post(TARGET, data=data["song"]["music_url"])
        if res.status_code == requests.codes.ok:
            return
    raise TimeoutError

if __name__ == '__main__':
    conf = toml.load("config.toml")
    host = conf["redis"]["ip"]
    port = conf["redis"]["port"]
    password = conf["redis"]["password"]
    # host = conf["redis-local"]["ip"]
    # port = conf["redis-local"]["port"]
    # password = None

    args = parser.parse_args()
    TARGET = args.path_to_google_home

    w = watcher.PlayQueueWatcher(host, port, password=password, debug=True)
    w.start(callback, with_thread=False)