import redis, yaml, os, json, pathlib
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


def check_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True

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

api.add_resource(Save, "/save/<string:player_name>")
api.add_resource(Load, "/load/<string:key>")

if __name__ == "__main__":
    app.run("0.0.0.0", port="5000", debug=True)
