# MRC API Documentation

Welcome to the API documentation for My Roblox Car. This API allows you to save/load savefiles from a game on Roblox made by me called My Roblox Car.

# API Reference

## Endpoints

### `/gensecret/[playerid]`

#### Method

`GET`

#### Description

Generates a new token for the player specified by `playerid`. This endpoint can only be called if the player doesn't already have a token.

#### Parameters

- `playerid` (string): The ID of the player for whom to generate a new token.

#### Returns

- A token (string).

#### Errors

- `409`: Token for the user already exists.

### `/save/[playerid]?token=[token]`

#### Method

`POST`

#### Description

Saves the current game for the player specified by `playerid`, using the provided `token` to authenticate the request. This endpoint can only be called if the player has a valid token.

#### Parameters

- `playerid` (string): The ID of the player for whom to save the game.
- `token` (string): The token to use for authentication.

#### Returns

- `200`: If the game was successfully saved.

#### Errors

- `400`: Invalid player ID (player doesn't exist).
- `400`: Missing token (no token was provided as a parameter).
- `401`: Token doesn't match DB (wrong token provided).
- `401`: You don't have a token, make a token with the `/gensecret` path (the player's token has expired).
- `400`: Invalid token (token is not 100 characters long).
- `400`: Invalid JSON format (provided body format is invalid).
- `500`: Failed to write to DB, is your JSON formatted correctly? (body is not in JSON format).

### `/load/[playerid]`

#### Method

`GET`

#### Description

Loads the saved game for the player specified by `playerid`.

#### Parameters

- `playerid` (string): The ID of the player for whom to load the saved game.

#### Returns

- A JSON object containing the saved game data.

#### Errors

- `404`: Error, key `[key]` is not found (save game doesn't exist).

### `/resettoken/[playerid]`

#### Method

`GET`

#### Description

Resets the token for the player specified by `playerid`. This endpoint can be used if the token transfer failed, and a new token needs to be generated. Can only be used in a 5 second range after a token was generated.

#### Parameters

- `playerid` (string): The ID of the player for whom to reset the token.

#### Returns

- `200`: If the token was successfully reset.
- `403`: error Forbiden
- `403`: Client not is not reset viable

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
