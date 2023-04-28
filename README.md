# Barbuc-Api

Barbuc-Api is a API REST which manage users and barbecues

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

7. Setup Docker Network
    First, you need to create a network :
    - `docker network create barbuc-network`

    Then, you can create containers for MongoDB and Redis

8. Setup MongoDB in Docker
    - Pull a mongo image `docker pull mongo`
    - Create a volume `docker volume create mongodb_volume`
    - Create a new container `docker run -d -p 27017:27017 -v mongodb_volume:/data/db --name barbuc-db --network barbuc-network mongo`
    - You are good to go !

9. Setup Redis in Docker
    - Pull a redis image `docker pull redis`
    - Create a volume `docker volume create redis_volume`
    - Create a new container `docker run -d -p 6379:6379 -v redis_volume:/data --name barbuc-redis --network barbuc-network redis`
    - You are good to go !

10. Setup environnements variable
You need to setup some environnements variables in order to make the API to work :

- MONGODB_URI : The URL of the MongoDB database (default is `mongodb://localhost:27017`)
- MONGODB_DATABASE : The name of the database (default is `barbuc-api`)
- SECURITY_PASSWORD_SALT : The salt used to encrypt user password (string)
- FLASK_JWT : The token used to generate access token (integer)
- JWT_ACCESS_TOKEN_EXPIRES : The number of seconds before a token expire (integer)
- REDIS_URI : The URL of Redis (default is `localhost`)
- REDIS_PORT : The port used for Redis (default is `6379`)

11. Create a superadmin user
When MongoDB is up, you can create a superadmin using this command :
    - `export FLASK_APP=run; flask user create_superadmin your_password`

This will create a superadmin user into the database and you will be able to login with these credentials :
    - Login : `admin.admin@admin.fr`
    - Password : `your_password`

__IMPORTANT__ : You will need to update the login of the admin and create others admin accounts to avoid some security issues.

12. Launch the API
To launch the API, use this command :
    - `make run`
___Note___ : If your system can't execute the command `make`, do this instead :
    - `export FLASK_APP=run; export FLASK_ENV=development; flask run --host=0.0.0.0 --port=5000;`

### Test the API
To test the API, just type :
- `make tests`
___Note___ : If your system can't execute the command `make`, do this instead :
    - `pytest --cov=barbuc_api --cov-config=.coveragerc --cov-report=html:htmlcov --cov-report xml:cov.xml --cov-report=term \
		-vv --doctest-modules --ignore-glob=./main.py --log-level=DEBUG --junitxml=report.xml ./ ./tests`

This will execute integration testing for every route and give total coverage for this project.


### Deploy the API on a Docker Container __(Optional)__
First, you need to set some specific value for environnements variables :
- _MONGODB_URI_ : To access to the MongoDB container you need to type : `mongodb://barbuc-db:27017`
___Note___ : `barbuc-db` is the name of the containter
The port doesn't need to change, you can leave him at `27017`

- _REDIS_URI_ : To access to the Redis container you need to type : `barbuc-redis`
___Note___ : `barbuc-redis` is the name of the containter
The port doesn't need to change, you can leave him at `6379`

Then, build the docker image using this command :
- `make build_docker_image`
___Note___ : If your system can't execute the command `make`, do this instead :
    - `docker build -t barbuc-api .`
`barbuc-api` is the name of the image

__Warning__ : Be sure to set environnements variables like said as mentioned above before building the container !

Finally, build the container using this command :
- `make build_docker_container`
___Note___ : If your system can't execute the command `make`, do this instead :
    - `docker run -d -p 5000:5000 --env-file .env --name barbuc-api --network barbuc-network barbuc-api`
Here, we set the port to 5000 and use the env file to apply configuration

To access to the container, just type :
    - `localhost:5000`
    or
    - `YOUR_IP_ADDRESS:5000`

### Generate swagger
To generate the swagger, just enter this command :
- `make build_schemas`

This will generate the swagger in JSON and YAML
___Note___ : If your system can't execute the command `make`, do this instead :
- `export FLASK_APP=run; flask openapi write specs/barbuc-spec.json;`
- `export FLASK_APP=run; flask openapi write specs/barbuc-spec.yaml;`