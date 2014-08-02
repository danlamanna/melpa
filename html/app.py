from flask import Flask, render_template
from flask.ext.cache import Cache
from redis import Redis
import json, re

application = Flask(__name__)
redis = Redis()
cache = Cache(app, config={'CACHE_TYPE': 'redis'})


def source_url(package_name):
    package = json.loads(redis.get("package:%s" % package_name))

    if "recipe" not in package:
        return None

    if package["recipe"]['fetcher'] == "github":
        if "repo" in package["recipe"]:
            return "https://github.com/" + package["recipe"]["repo"]
        else:
            return "https://gist.github.com/" + package["recipe"]["repo"]
    elif package["recipe"]["fetcher"] == "wiki" and "files" not in package["recipe"]:
        return "http://www.emacswiki.org/emacs/%s.el" % package_name
    elif "url" in package["recipe"]:
        def url_match(regex, prefix=""):
            m = re.match(regex, package["recipe"]["url"])
            return prefix + m.groups()[0] if m is not None else ""

        return (url_match(r"(bitbucket\.org\/[^\/]+\/[^\/\?]+)", "https://") or
                url_match(r"(gitorious\.org\/[^\/]+\/[^.]+)", "https://") or
                url_match(r"\Alp:(.*)", "https://launchpad.net/") or
                url_match(r"\A(https?:\/\/code\.google\.com\/p\/[^\/]+\/)") or
                url_match(r"\A(https?:\/\/[^.]+\.googlecode\.com\/)"))

    return None

def package_needed_by(pkg_name):
    package = json.loads(redis.get("package:%s" % pkg_name))

    needed_by = set()

    packages = sorted(redis.keys("package:*"))

    for package_name in packages:
        package = json.loads(redis.get(package_name))
        package_name = package_name.replace("package:", "")

        try:
            if pkg_name in package['archive']['deps'].keys():
                needed_by.add(package_name)
        except (KeyError, AttributeError):
            pass

    return list(needed_by)

@application.route('/')
@cache.cached(timeout=60*60*24)
def index():
    table_data = []
    packages = sorted(redis.keys("package:*"))

    for package_name in packages:
        package = json.loads(redis.get(package_name))
        package_name = package_name.replace("package:", "")

        table_data.append({"package": package_name,
                           "desc": package["archive"]['desc'] if "archive" in package and "desc" in package["archive"] else "",
                           "ver": ".".join(map(str, package["archive"]['ver'])) if "archive" in package and "ver" in package["archive"] else "",
                           "recipe": "https://github.com/milkypostman/melpa/blob/master/recipes/" + package_name,
                           "source": {"fetcher": package["recipe"]['fetcher'] if "recipe" in package and "fetcher" in package["recipe"] else "",
                                      "url": source_url(package_name)},
                           "dls": package["dl_count"] if "dl_count" in package else ""})

    return render_template("index.html", recipes=table_data,
                           total_dl_count=redis.get("total_dl_count"),
                           body_attrs='ng-controller=MyCtrl')

@application.route('/<package_name>')
def package(package_name):
    return render_template("package.html", package_name=package_name, recipe_url=source_url(package_name), needed_by=package_needed_by(package_name), package=json.loads(redis.get("package:%s" % package_name)))

@application.route('/original')
def original():
    return render_template("origin.html")


if __name__ == '__main__':
    application.run(debug=True)
