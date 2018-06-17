import redis
from datetime import datetime, timedelta

song1 = '{"id": 1, "song": {"song_name": "adrenaline!!!", "artist_name": "TrySail", "artwork_url": "https://images-na.ssl-images-amazon.com/images/I/61jI%2BP82JVL.jpg", "time": 130, "music_url": "http://amachamusic.chagasi.com/mp3/kasumisou.mp3"}, "usename": "MMAtsushi"}'
song2 = '{"id": 2, "song": {"song_name": "adrenaline!!!", "artist_name": "TrySail", "artwork_url": "https://images-na.ssl-images-amazon.com/images/I/61jI%2BP82JVL.jpg", "time": 127, "music_url": "http://www.ne.jp/asahi/music/myuu/wave/asibue.mp3"}, "usename": "MMAtsushi"}'
r = redis.Redis(host='127.0.0.1')
r.set(datetime.today(), song1)
r.set(datetime.today() + timedelta(seconds=10), song2)