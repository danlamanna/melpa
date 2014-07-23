from flask import Flask, render_template
from redis import Redis
import requests, json

app = Flask(__name__)
redis = Redis()

@app.route('/')
def index():
    table_data = []
    recipes = redis.keys("recipes:*")

    recipes = sorted(recipes)

    for recipe in recipes:
        r = redis.get(recipe)

        if r:
            r = json.loads(r)

        recipe  = recipe.replace("recipes:", "")
        archive = redis.get("archives:%s" % recipe)
        dls     = redis.get("dl_counts:%s" % recipe)

        if archive:
            archive = json.loads(archive)

        table_data.append([recipe,
                           archive['desc'] if archive else None,
                           ".".join(map(str, archive['ver'])) if archive else None,
                           "https://github.com/milkypostman/melpa/blob/master/recipes/" + recipe,
                           r['fetcher'] if 'fetcher' in r else None,
                           dls if dls else None])


    return render_template("index.html", recipes=table_data)

if __name__ == '__main__':
    app.run(debug=True)
