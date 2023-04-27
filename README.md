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
    - Create a new container `docker run -d -p 27017:27017 -v redis_volume --name barbuc-redis redis`
    - You are good to go !

9. Setup environnements variable

10. Create a superadmin user

11. Launch the API

12. Deploy the API on Docker Container