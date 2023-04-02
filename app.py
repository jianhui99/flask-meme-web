import requests
import json
from flask import Flask, render_template, request
from flask_caching import Cache

app = Flask(__name__)

# Flask-Caching configuration
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


api = "https://api.imgflip.com/get_memes"

@cache.cached(timeout=3600)
def get_memes():
    data = json.loads(requests.request("GET", api).text)
    memes = data['data']['memes']
    return memes

@app.route('/')
def index():
    q = request.args.get('q')
    if q:
        memes = [meme for meme in get_memes() if q.lower() in meme['name'].lower()]
    else:
        memes = get_memes()

    total = len(memes)

    return render_template('index.html', memes=memes, total=total)

if __name__ == '__main__':
    app.run(debug=True)