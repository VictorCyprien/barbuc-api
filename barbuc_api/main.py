from environs import Env

Env.read_env()

from .config import config

# Validate the conf
config.validate()

# Initialize flask app
from .app import create_flask_app
app = create_flask_app(config)
