from redis import Redis
import requests, json

redis = Redis()

# once this is on the server, we can just open these files directly.
data = {"recipes":   requests.get("http://melpa.milkbox.net/recipes.json").json,
        "archives":  requests.get("http://melpa.milkbox.net/archive.json").json,
        "dl_counts": requests.get("http://melpa.milkbox.net/download_counts.json").json}

total_dl_count = 0

for recipe_name, recipe in data['recipes'].iteritems():
    package = {}

    try:
        total_dl_count += int(data["dl_counts"][recipe_name])

        package["recipe"] = recipe
        package["archive"] = data["archives"][recipe_name]
        package["dl_count"] = int(data["dl_counts"][recipe_name])
    except KeyError:
        pass # less archives than recipes? extra dl_counts?

    redis.set("package:%s" % recipe_name, json.dumps(package))

redis.set("total_dl_count", total_dl_count)
