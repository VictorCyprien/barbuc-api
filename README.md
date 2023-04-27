# Barbuc-Api

Barbuc-Api is a API REST which manage users and barbucue

## Requirements
- Windows or Linux
- Python (with pip)
- Docker

## How to install ?

1. Open a new terminal
2. Clone this repository
    
    - With HTTPS :
        - `git clone https://github.com/VictorCyprien/barbuc-api.git`

    - With SSH :
        - `git clone git@github.com:VictorCyprien/barbuc-api.git`

3. Move to the project
    - `cd /barbuc-api`


4. Create a new virtual environnement
    - `virtualenv venv`
    
    ___Note___ : To install virtualenv, please use `pip install virtualenv`

5. Activate your new virtual environnement
    - Windows : `source venv/Scripts/activate`

    - Linux : `source venv/bin/activate`

6. Install dependencies
    - `make install`
    
    ___Note___ : If your system can't execute the command `make`, do this instead :
        - `pip install -r requirements.txt`
        - `pip install -r requirements.dev.txt`
        - `pip install -e ./`

---WIP---

7. Setup MongoDB in Docker
    - Pull a mongo image `docker pull mongo`
    - Create a volume `docker volume create mongo_volume`
    - Create a new container `docker run -d -p 27017:27017 -v mongo_volume --name barbuc-db mongo`
    - You are good to go !

8. Setup Redis in Docker
    - Pull a redis image `docker pull redis`
    - Create a volume `docker volume create redis_volume`
    - Create a new container `docker run -d -p 6379:6379 -v redis_volume --name barbuc-redis redis`
    - You are good to go !

9. Setup environnements variable
You need to setup some environnements variables in order to make the API to work :

- MONGODB_URI : The URL of the MongoDB database (default is `"mongodb://localhost:27017"`)
- MONGODB_DATABASE : The name of the database (default is `"barbuc-api"`)
- SECURITY_PASSWORD_SALT : The salt used to encrypt user password (string)
- FLASK_JWT : The token used to generate access token (integer)
- JWT_ACCESS_TOKEN_EXPIRES : The number of seconds before a token expire (integer)
- REDIS_URI : The URL of Redis (default is `localhost`)
- REDIS_PORT : The port used for Redis (default is `6379`)

10. Create a superadmin user
When MongoDB is up, you can create a superadmin using this command :
    - `export FLASK_APP=run; flask user create_superadmin your_password`

This will create a superadmin user into the database and you will be able to login with these credentials :
    - Login : `admin.admin@admin.fr`
    - Password : `your_password`

__IMPORTANT__ : You will need to update the login of the admin and create other admin accounts to avoid some security issues

11. Launch the API
To launch the API, use this command :
    - `make run`
___Note___ : If your system can't execute the command `make`, do this instead :
    - `export FLASK_APP=run; export FLASK_ENV=development; flask run --host=0.0.0.0 --port=5000;`



12. Deploy the API on a Docker Container __(Optional)__
(WIP)


### Generate swagger
To generate the swagger, just enter this command :
- `make build_schemas`

This will generate the swagger in JSON and YAML
___Note___ : If your system can't execute the command `make`, do this instead :
- `export FLASK_APP=run; flask openapi write specs/barbuc-spec.json;`
- `export FLASK_APP=run; flask openapi write specs/barbuc-spec.yaml;`