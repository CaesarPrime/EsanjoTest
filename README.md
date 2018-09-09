# Esanjo Python Assignment

This sample app has been designed with the aid of python's flask framework. The main reason for using this had been it's lightweightness.

The details regarding the deployment on development server are as follows. For Production environment the FLASK_ENV variable can be set to production and the deployment can begin.The App can be deployed within an app service from a given cloud solutions provider.

References:- For the Auth Services Design https://github.com/miguelgrinberg/REST-auth this repository had been used.

## Installation - Development
In this repository I have configured a python3 virtual environment. Therefore it would have all it's dependencies.

What you would all need to do is download the repository using 
```
$ git clone https://github.com/CaesarPrime/EsanjoTest.git
```
Now get in to the EsanjoTest folder using cd command and activate the virtual environment using 

```
$ . venv/bin/activate 
```
if you are using a linux based or MacOS Operating system

once done setup the environment variables needed within the virtual environement. As the task would be done within the development environemnt it is essential to mention that as well.

```
$ export FLASK_APP=Organizer.py
$ export FLASK_ENV=development
$ flask run
```

Once done the server would listen on http://localhost:5000

## Task 1

Use http://localhost:5000/task1 to access the task. Data needed for the processing were imported from the json 

## Task 2

Use http://localhost:5000/task2 to access the task. 

For Registering a user,

```$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"Pasan","password":"toor"}' http://127.0.0.1:5000/api/users```

In order to receive the token

```$ curl -u Pasan:toor -i -X GET http://127.0.0.1:5000/api/token```

To Access the restricted api with the token. Here x would be just an arbitary variable where password is set.

```$ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:x -i -X GET http://127.0.0.1:5000/task2 ```

## Acknowledgements
1. [Miguel Grinberg's] (https://github.com/miguelgrinberg) [Flask authentication app repository](https://github.com/miguelgrinberg/REST-auth)
