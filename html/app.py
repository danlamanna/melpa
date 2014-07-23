from flask import Flask, render_template
from redis import Redis
import json

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

        table_data.append({"package": recipe,
                           "desc": archive['desc'] if archive and "desc" in archive else "",
                           "version": ".".join(map(str, archive['ver'])) if archive and "ver" in archive else "",
                           "recipe":"https://github.com/milkypostman/melpa/blob/master/recipes/" + recipe,
                           "source":r['fetcher'] if r and "fetcher" in r else "",
                           "dls": dls if dls else ""})


    return render_template("index.html", recipes=table_data, body_attrs='ng-controller=MyCtrl')

if __name__ == '__main__':
    app.run(debug=True)
