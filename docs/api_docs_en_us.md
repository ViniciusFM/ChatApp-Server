# API Documentation (ver em [🇧🇷](api_docs.md))
This is the ChatApp Server API Documentation

# Pages Routes
Routes that return HTML pages.

## Index

Displays an about page.

```plain
Methods:
    GET
Route:
    /
Output:
    HTML
```

### Output
```plain
* returns a HTML page containing an about server.
```

## Channel Invitation

Displays a page that redirects to a chatapp:// URI, triggering a specific App Intent on Android. Before redirection, the service attempts to retrieve an existing Channel and returns a 404 error if none is found. Access to this route is protected by CAPTCHA verification.

```plain
Methods:
    GET, POST
Route:
    /invite/<string:uuid>
Input:
    URL Path: uuid string from channel
Output:
    HTML
Error Status:
    * 404, if channel not found (body: html)
```

### Output
```plain
* returns a page containing a CAPTCHA form, and then returns a page redirecting to Channel URI.
```

# Authorization Routes
Routes that enable authentication to the server.

## Google Login

Retrieves Users ID information from Google after receiving an `id_token`.

```plain
Methods:
    POST
Route:
    /auth/google
Input:
    JSON: id_token
Output:
    JSON: token + full user data + channels this user owns
Error Status:
    * 400, if id_token not in request body
    * 403, if Google account was restricted by this server.
    * 403, if server failed to auth in Google Auth Server
```

### Input
```json
{
    "id_token": "id token from google auth"
}
```

### Output
```json
{
	"token": "JWT token produced by this server",
	"user": {
		"channels": [],
		"email": "googleaccountexample@gmail.com",
		"id": 1,
		"name": "User Fullname",
		"uuid": "user uuid"
	}
}
```

## Auth Required

Every `auth_required` route needs to contain the a HTTP header like this:

```plain
Header:
    Authorization: Bearer this-should-be-the-token-returned-by-google-login-route
```

# API Routes
Routes that provides chat data transmission between Client and Server

## Get Channel ([auth_required](#auth-required))

Retrieves full `Channel` data containing messages and admin information.

```plain
Methods:
    GET
Route:
    /channels/<string:uuid>
Input:
    URL Path: uuid string from channel
Output:
    JSON: Channel data
Error Status:
    * 404, if channel does not exist
```

### Output

```json
{
	"admin": {
		"id": 1,
		"name": "Admin User Fullname"
	},
	"alias": "Channel Name",
	"id": 2,
	"img_res": "uuid to image resource",
	"messages": [
		{
			"channel_id": 2,
			"creation_ts": "Tue, 03 Jun 2025 18:19:48 GMT",
			"id": 1,
			"text": "Hello, World!!!",
			"user": {
				"id": 1,
				"name": "User That Send the Message"
			}
		}
	],
	"uuid": "uuid that identifies this channel"
}
```

## Get Image ([auth_required](#auth-required))

Returns a `JPEG` image resource identified by an `UUID`.

```plain
Methods:
    GET
Route:
    /img/<string:img_res>
Input:
    URL Path: uuid to image resource
Output:
    image/jpeg
Error Status:
    * 404, if image does not exist
```

## New Channel ([auth_required](#auth-required))

Adds a new `Channel` to database.

```plain
Methods:
    POST
Route:
    /channels/new
Input:
    JSON: Channel data [required: alias]
Output:
    JSON: Channel data
Error Status:
    * 400, if required data is not in json body
```

### Input
```json
{
    "alias": "Channel Name",
	"img_res": "Image binary but encoded as Base64. This field is not required."
}
```

### Output
```json
{
	"admin": {
		"id": 1,
		"name": "Admin User Fullname"
	},
	"alias": "Channel Name",
	"id": 3,
	"img_res": "uuid to image resource",
	"messages": [],
	"uuid": "this added channel uuid"
}
```

## New Message ([auth_required](#auth-required))

Adds a new `Message` to a `Channel`.

```plain
Methods:
    POST
Route:
    /messages/new
Input:
    JSON: Message data [required: text, channel_uuid]
Output:
    JSON: Message data
Error Status:
    * 400, if required data is not in json body
    * 404, if channel not found
```

## Input
```json
{
	"channel_uuid": "channel uuid you want to post your msg",
	"text": "Message text you sent"
}
```

## Output
```json
{
	"channel_id": 2,
	"creation_ts": "Tue, 03 Jun 2025 18:19:48 GMT",
	"id": 1,
	"text": "Message text you sent",
	"user": {
		"id": 1,
		"name": "User Fullname"
	}
}
```