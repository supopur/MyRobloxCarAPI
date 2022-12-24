import redis, yaml, os
from pathlib import Path
from flask import Flask


#Get password from the yml file
def get_password():
    full_file_path = Path(__file__).parent.joinpath('credentials.yml')
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)
    return settings_data
creds = get_password()

mode = creds["mode"]
# redis
if mode == "userpass":
    redis_cache = redis.Redis(host=creds["host"], port=creds["port"], db=0, password=creds["password"], username=creds["user"])
elif mode == "nopass":
    redis_cache = redis.Redis(host=creds["host"], port=creds["port"], db=0, user=creds["user"])
else:
    print("No valid login method specified so now im not doing it!")
    os.exit()

# flask app
app = Flask(__name__)


# set
@app.route('/set/<string:key>/<string:value>')
def set(key, value):
	if redis_cache.exists(key):
		return f"{key} is already exists, please use `update` route to change the value!"
	else:
		redis_cache.set(key, value)
		return "OK"

# update
@app.route('/update/<string:key>/<string:value>')
def update(key, value):
	if redis_cache.exists(key):
		redis_cache.set(key, value)
		return "OK"
	else:
		return f"{key} is not exists"

# get
@app.route('/get/<string:key>')
def get(key):
    if redis_cache.exists(key):
        print(redis_cache.json().get(key))
        return redis_cache.json().get(key)
    else:
        return f"{key} is not exists"


if __name__ == "__main__":
	app.run("0.0.0.0", port="5000", debug=True)
