## MRC API Documentation

Welcome to the API documentation for My Roblox Car. This API allows you to save/load savefiles from a game on Roblox made by me called My Roblox Car.

### Endpoints

Below is a list of the available endpoints for the API:

#### /load/[playername]
- Description: Returns a json with the player save data.
- HTTP Method: GET
- Parameters:
  - playername: Roblox ID Of player
- Example Request: https://api.nazev.eu/get/mazltus
- Example Response: 
  ```json
      "key": "mazltus"
      "value": {
      {
        "version": "dev-1.0",
        "lastplayed": [
            2022,
            12,
            1
        ],
        "weather": {
            "season": "summer",
            "day": 172,
            "hours": 12,
            "minutes": 0,
            "temperature": 10,
            "weather": "sunny"
        },
        "needs": {
            "health": 100,
            "hunger": 20,
            "thirst": 0,
            "stress": 0,
            "dirtiness": 0,
            "fatigue": 0,
            "urine": 0,
            "money": 3000
        },
        "events": {
            "teimo": true,
            "nappo": false,
            "teimohome": false,
            "housefire": false
        },
        "car": {
            "parts": {
                "piston1": {
                    "health": 100,
                    "mounted": false,
                    "position": [
                        0,
                        200,
                        10
                    ],
                    "screws": {
                        "1": 0,
                        "2": 0
                    }
                }
            },
            "oil": 78,
            "fuel": 0,
            "coolant": 20,
            "batterry": 100
        },
        "items": {
            "shoppingbag": {
                "postion": [
                    0,
                    100,
                    0
                ],
                "items": [
                    "beer",
                    "saussage"
                ]
            },
            "beer_empty": {
                "position": [
                    0,
                    120,
                    0
                ]
            }
        }
    }
  ```


#### /save/[playername]
- Description: Saves player data in a json format shown above. If player key doesnt exist in redis it creates a new one.
- HTTP Method: POST
- Parameters:
  - playername: Roblox ID Of player
- Example Request: https://api.nazev.eu/save/mazltus (Include json body with your data. It owerwrites the existing key so be sure to save everything.)
- Example Response: OK 200

### Authentication

I need to somehow do this.

### Errors

- `200 OK`: This code indicates that the request was successful and the requested information was returned.
- `400 Bad Request`: This code indicates that the server could not understand the request due to invalid syntax. This error is returned by the `Save` resource's `post` method if the request data is not valid JSON.
- `404 Not Found`: This code indicates that the requested resource could not be found. This error is returned by the `Load` resource's `get` method if the requested key is not found in the Redis database.


### Using
#### Development:
```
  python3 api.py
```

#### Production:
It is recomended to use a wsgi app for example gunicorn
```
  gunicorn --bind 0.0.0.0:5000 wsgi:app
```
