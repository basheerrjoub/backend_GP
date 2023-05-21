
# AI-Based Diabetes Management System (Backend)

This is the API's Documentation.

## Installing and configuring the repository
* Clone this repository.
* Python has to be installed on your device.
* In the root directory execute the following prompt `python -m venv env`
* Enter to the virtual enviroment by executing the following command in the base directory `.\env\Scripts\activate`
* Install the packages by executing the following command `pip install -r requirements.txt`

## REST API's Docummentaion

### Login a registered user 
`POST api/token/`
#### Request
```
POST /api/token/ HTTP/1.1
Content-Type: application/json
User-Agent: PostmanRuntime/7.32.2
Accept: */*
Postman-Token: 45369843-a05c-4061-bbae-14675a00f985
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 66
 
{
"email": "admin@gmail.com",
"password": "admin1234"
}

```


### Response
```
HTTP/1.1 200 OK
Date: Sun, 21 May 2023 09:42:21 GMT
Server: WSGIServer/0.2 CPython/3.11.3
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 483
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
 
{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4NDc0ODU0MSwiaWF0IjoxNjg0NjYyMTQxLCJqdGkiOiJlNjg2Mjg3NDNhZjU0MjI4OWQ0MzY4OTZjZGI2OTIyOSIsInVzZXJfaWQiOjF9.SVYbm39j733bOL5Hqg4lu1X8g1ErU5kKnDzFsmmeCsk","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0NjY1NzQxLCJpYXQiOjE2ODQ2NjIxNDEsImp0aSI6IjgwY2U1NWUxOTM5OTQ1ZDJhNjJlYmVmMTE2ZTNhOTgzIiwidXNlcl9pZCI6MX0.zxc6KKZZEOJIxZtpyPOpWWMpPurWbeed89O_DoUov84"}

```
If the user is verified, then a token is generated for this user, and has to send it in the following requests, so that accessing within this token the parts which user has authorization.

