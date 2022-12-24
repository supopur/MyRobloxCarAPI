#Base of this code was written by https://github.com/BaseMax Forked from https://github.com/BaseMax/FirstRedisPython
#Modified by https://github.com/supopur/
#I got permision. You can search for my issue on github on his repo.

import redis, yaml, os, json, pathlib, secrets, hashlib, threading, datetime
from flask import Flask
from flask import Flask, request
from flask_restful import Resource, Api
from redis.commands.json.path import Path


#Get password from the yml file
def get_password():
    full_file_path = pathlib.Path(__file__).parent.joinpath('credentials.yml')
    with open(full_file_path) as settings:
        settings_data = yaml.load(settings, Loader=yaml.Loader)
    return settings_data
creds = get_password()

mode = creds["mode"]
# redis
if mode == "userpass":
    r = redis.Redis(host=creds["host"], port=creds["port"], db=0, password=creds["password"], username=creds["user"])
elif mode == "nopass":
    r = redis.Redis(host=creds["host"], port=creds["port"], db=0, user=creds["user"])
else:
    print("No valid login method specified so now im not doing it!")
    os.exit()
app = Flask(__name__)
api = Api(app)

#Check if the value is a valid json format
def check_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True

#Make a client secret used for authenticating users
def generate_token():
    #Generates a random, secure token.
    return secrets.token_hex(50)

#Create a redis string key that expires after certain time in days
def create_expire_key(key, value, days):
    # Set the key with the value
    r.set(key, value)
    ttl_in_seconds = days * 24 * 60 * 60
    # Set the key's TTL to 1 week
    r.expire(key, ttl_in_seconds)

class Save(Resource):
    def post(self, player_name):
        data = request.data
        if not check_json(data):
            return {"error": "Invalid JSON format"}, 400
        data = json.loads(data)
        print(data)

        r.json().set(player_name, Path.root_path(), data["value"])
        return {"status": "success"}


class Load(Resource):
    def get(self, key):

        value = r.json().get(key)
        print(value)
        if value is None:
            return {"error": f"Key '{key}' not found"}, 404
        return {"key": key, "value": value}

class GenSecret(Resource):
    def get(self, player):
        if r.exists(f"{player}_secret"):
            return "Error token exists", 409
        elif not r.exists(f"{player}_secret"):
            secret = generate_token()
            create_expire_key(f"{player}_secret", secret, 7)
            return secret, 200
        else:
            return "Internal Server Error", 500

api.add_resource(GenSecret, "/gensecret/<string:player>")
api.add_resource(Save, "/save/<string:player_name>")
api.add_resource(Load, "/load/<string:key>")

if __name__ == "__main__":
    app.run("0.0.0.0", port="5000", debug=True)
