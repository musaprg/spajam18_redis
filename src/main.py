import toml
import watcher
import signal

# w = None

def callback(data):
    """
    callback function
    :param data: parsed json data (dict)
    :return:
    """
    print(data)

# def handler():
#     global w
#     w.stop()

if __name__ == '__main__':
    conf = toml.load("../config.toml")
    # host = conf["redis"]["ip"]
    # port = conf["redis"]["port"]
    # password = conf["redis"]["password"]
    host = conf["redis-local"]["ip"]
    port = conf["redis-local"]["port"]
    password = None

    # signal.signal(signal.SIGTERM, handler)
    # signal.signal(signal.SIGKILL, handler)

    w = watcher.PlayQueueWatcher(host, port, "hoge", password=password, debug=True)
    w.start(callback, with_thread=False)