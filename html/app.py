from flask import Flask, render_template
from redis import Redis
import requests, json

app = Flask(__name__)
redis = Redis()

def _build_index():
    data = {"recipes": "http://melpa.milkbox.net/recipes.json",
            "archives": "http://melpa.milkbox.net/archive.json",
            "dl_counts": "http://melpa.milkbox.net/download_counts.json"}

    for datatype, url in data.iteritems():
        r = requests.get(url)

        # todo: pipelining in redis?
        if r.status_code == 200:
            for name, response in r.json.iteritems():
                redis.set("%s:%s" % (datatype, name), json.dumps(response))


@app.route('/')
def index():
    recipes = [(k, json.loads(redis.get(k))) for k in redis.keys("packages:*")]

    return render_template("/home/dan/src/melpa/html/templates/index.html", recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
