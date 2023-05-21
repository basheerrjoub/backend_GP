
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
`POST api/login/`
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



### Register a new user 
`POST api/register/`
#### Request
```
POST /api/register/ HTTP/1.1
Content-Type: application/json
User-Agent: PostmanRuntime/7.32.2
Accept: */*
Postman-Token: 782c987c-7792-4822-bd11-f5123d6146e1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Content-Length: 166
 
{
"first_name": "Ahmad",
"last_name": "Mohammad",
"username": "ahmadmohammad",
"email": "ahmadmohammad@gmail.com",
"password": "ahmad1234"
}
 

```


### Response
```
HTTP/1.1 200 OK
Date: Sun, 21 May 2023 11:34:11 GMT
Server: WSGIServer/0.2 CPython/3.11.3
Content-Type: application/json
Vary: Accept
Allow: POST, OPTIONS
X-Frame-Options: DENY
Content-Length: 191
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
 
{"user":{"first_name":"Ahmad","last_name":"mohammad","username":"ahmadmohammad","email":"ahmadmohammad@gmail.com"},"message":"User Created Successfully. Now perform Login to get your token"}


```
Take care, that the email should be unique.



### View all Meals
`POST api/register/`
#### Request
```
GET /api/meals/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0Njc2OTQzLCJpYXQiOjE2ODQ2NzMzNDMsImp0aSI6IjYxN2M4OWU3YTZmNTRlMWQ5OTQ2ZDI1YzA4NzJhZGEzIiwidXNlcl9pZCI6MX0.vJdhT2ENXwJG40T0-zHq8r7I2rzv-Fq054yltIQsWS0
User-Agent: PostmanRuntime/7.32.2
Accept: */*
Postman-Token: 8884eadb-dab8-4d8a-bb9f-bb3b9f6b4481
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
 

```


### Response
```
HTTP/1.1 200 OK
Date: Sun, 21 May 2023 12:50:33 GMT
Server: WSGIServer/0.2 CPython/3.11.3
Content-Type: application/json
Vary: Accept
Allow: GET, POST, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 4886
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
 
[Body, Contains list of Meals]


```
Make sure the token is valid (for the current session), if not, re-Login.


### View The suggested meals for the current logged-in user
`GET api/suggestions/`
#### Request
```
GET /api/suggestions/ HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjg0Njc2OTQzLCJpYXQiOjE2ODQ2NzMzNDMsImp0aSI6IjYxN2M4OWU3YTZmNTRlMWQ5OTQ2ZDI1YzA4NzJhZGEzIiwidXNlcl9pZCI6MX0.vJdhT2ENXwJG40T0-zHq8r7I2rzv-Fq054yltIQsWS0
User-Agent: PostmanRuntime/7.32.2
Accept: */*
Postman-Token: 9505d38c-0bf7-431e-aea5-3adfeb47bced
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
 
 

```


### Response
```
HTTP/1.1 200 OK
Date: Sun, 21 May 2023 13:02:42 GMT
Server: WSGIServer/0.2 CPython/3.11.3
Content-Type: application/json
Vary: Accept
Allow: GET, HEAD, OPTIONS
X-Frame-Options: DENY
Content-Length: 875
X-Content-Type-Options: nosniff
Referrer-Policy: same-origin
Cross-Origin-Opener-Policy: same-origin
 
[{"meal_id":1,"meal_name":"سلطة قيصر مع الدجاج المشوي","meal_des":"None","snack":0,"breakfast":0,"lunch":1,"dinner":1,"warm":0,"hard":1,"salty":1,"sweety":0,"spicy":1},{"meal_id":2,"meal_name":"سلطة التونا بالباستا","meal_des":"ا","snack":0,"breakfast":0,"lunch":1,"dinner":1,"warm":0,"hard":1,"salty":1,"sweety":0,"spicy":1},{"meal_id":3,"meal_name":"حساء الخضار","meal_des":"ا","snack":0,"breakfast":0,"lunch":1,"dinner":1,"warm":1,"hard":0,"salty":1,"sweety":0,"spicy":0},{"meal_id":4,"meal_name":"حساء البطاطا والشمر","meal_des":"ا","snack":0,"breakfast":0,"lunch":1,"dinner":1,"warm":1,"hard":1,"salty":1,"sweety":0,"spicy":0},{"meal_id":5,"meal_name":"حساء الخضار باللحم","meal_des":"ا","snack":0,"breakfast":0,"lunch":1,"dinner":1,"warm":1,"hard":1,"salty":1,"sweety":0,"spicy":0}]


```
Make sure the token is valid (for the current session), if not, re-Login, also these suggested meals are given for the logged in user.