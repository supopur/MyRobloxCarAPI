#Base of this code was written by https://github.com/BaseMax Forked from https://github.com/BaseMax/FirstRedisPython
#Modified by https://github.com/supopur/
#I got permision. You can search for my issue on github on his repo.
#Most security related code was wrote by chatgpt.

import redis, yaml, os, json, pathlib, secrets, hashlib, threading, datetime, time
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



# Dictionary to store the tokens, expiration times, and request times
ttl_dictionary = {}

def check_expirations():
    # Get the current time
    current_time = datetime.datetime.now().second

    # Iterate over the keys and values in the dictionary
    for key, value in ttl_dictionary.items():
        # Get the expiration time for the value
        expiration_time = value["expiration"]

        # If the expiration time has passed, remove the value from the dictionary
        if current_time > expiration_time:
            del ttl_dictionary[key]

# Schedule the check_expirations function to run every 5 seconds
threading.Timer(5, check_expirations).start()

class reset_token(Resource):

    def get(self, client_id):

        # Check if the client has already requested a token within the past 30 seconds
        if client_id in ttl_dictionary:
            request_time = ttl_dictionary[client_id]["request_time"]
            time_since_request = datetime.datetime.now().second - request_time

            if not time_since_request < 5:
                # Return a 403 error if the client has already requested a token within the past 30 seconds
                return {"error": "Forbidden"}, 403
            else:

                # Generate a random token string
                token = generate_token()

                return token
        else:
            return "Client not is not reset viable", 403



#Create a redis string key that expires after certain time in days
def create_expire_key(key, value, days):
    # Set the key with the value
    r.set(key, value)
    ttl_in_seconds = days * 24 * 60 * 60
    # Set the key's TTL to 1 week
    r.expire(key, ttl_in_seconds)


class Save(Resource):
    def post(self, player_name):
        token = request.args.get("token")
        if isinstance(token, type(None)): return "Missing token", 400
        if len(token) == 100:
            key_exists = r.exists(f"{player_name}_secret")
            if key_exists:
                #This should NOT work but leave it here if you know how to make this better make a issue on github
                if str(r.get(f"{player_name}_secret"))[2:-1] == str(token):
                    pass
                else: return "Token doesnt match the DB", 403
            else: return "You dont have a token make a toking with the gensecret path", 404
        else: return "Invalid token", 400

        data = request.data
        if not check_json(data):
            return "Invalid JSON format", 400
        data = json.loads(data)

        r.json().set(player_name, Path.root_path(), data["value"])
        return "OK", 200


class Load(Resource):

    def get(self, key):

        value = r.json().get(key)

        if value is None:
            return {"error": f"Key '{key}' not found"}, 404
        return value, 200

class GenSecret(Resource):

    def get(self, player):
        if r.exists(f"{player}_secret"):
            return "Error token exists", 409
        elif not r.exists(f"{player}_secret"):
            secret = generate_token()
            create_expire_key(f"{player}_secret", secret, 7)
            # Calculate the hash of the token string
            token_hash = hashlib.sha256(secret.encode()).hexdigest()

            # Calculate the expiration time for the token (1 week from now)
            expiration_time = datetime.datetime.now().second + 5
            if expiration_time > 50:
                time.sleep(12)
                expiration_time = datetime.datetime.now().second + 5

            # Store the token, expiration time, and request time in the dictionary
            ttl_dictionary[player] = {"token": token_hash, "expiration": expiration_time, "request_time": datetime.datetime.now().second}
            return json.dumps(list({secret, token_hash})), 200
        else:
            return "Internal Server Error", 500

api.add_resource(GenSecret, "/gensecret/<string:player>")
api.add_resource(Save, "/save/<string:player_name>")
api.add_resource(Load, "/load/<string:key>")
api.add_resource(reset_token, "/resettoken/<string:client_id>")

if __name__ == "__main__":
    app.run("0.0.0.0", port="5000", debug=True)
