from redis import Redis
import requests, json

redis = Redis()

# once this is on the server, we can just open these files directly.
data = {"recipes": "http://melpa.milkbox.net/recipes.json",
        "archives": "http://melpa.milkbox.net/archive.json",
        "dl_counts": "http://melpa.milkbox.net/download_counts.json"}

for datatype, url in data.iteritems():
    r = requests.get(url)

    # todo: pipelining in redis?
    if r.status_code == 200:
        for name, response in r.json().iteritems():
            redis.set("%s:%s" % (datatype, name), json.dumps(response))
