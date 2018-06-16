import redis

string = '{"id": 1, "song": {"song_name": "adrenaline!!!", "artist_name": "TrySail", "artwork_url": "https://images-na.ssl-images-amazon.com/images/I/61jI%2BP82JVL.jpg", "time": 10, "music_url": "https://misw.jp"}, "usename": "MMAtsushi"}'
r = redis.Redis(host='localhost')
r.set("1", string)