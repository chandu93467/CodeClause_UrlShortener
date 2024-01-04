from flask import Flask, render_template, request, redirect
from flask_redis import FlaskRedis
import base62

app = Flask(__name__)
app.config['REDIS_URL'] = "redis://localhost:6379/0"
redis = FlaskRedis(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form['original_url']
    
    # Retrieve the current url_id_counter from Redis
    url_id = redis.incr('url_id_counter')
    
    # Encode the identifier using base62
    short_code = base62.encode(url_id)
    
    # Store the mapping in Redis
    redis.set('url:' + short_code, original_url)
    
    short_url = request.host_url + short_code
    return render_template('result.html', original_url=original_url, short_url=short_url)

@app.route('/<short_code>')
def redirect_to_original(short_code):
    # Retrieve the original URL from Redis
    original_url = redis.get('url:' + short_code)
    
    if original_url:
        return redirect(original_url)
    else:
        return render_template('not_found.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

