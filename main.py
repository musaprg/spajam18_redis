import redis
import toml
from pprint import pprint

def connect(host, port):
    pool = redis.ConnectionPool(host=host, port=port, db=0)
    r = redis.StrictRedis(connection_pool=pool)
    return r

if __name__ == '__main__':
    conf = toml.load('./config.toml')
    r = connect(conf['redis']['ip'], conf['redis']['port'])


