from environs import Env


class Config:

    def __init__(self):
        env = Env()

        self.SERVICE_NAME = 'Barbuc-api'
        self.LOGGER_LEVEL = env.str("LOGGER_LEVEL", "DEBUG")

        # FLASK
        self.FLASK_ENV = env.str('FLASK_ENV', 'dev')
        self.JSON_SORT_KEYS = True

        # FLASK JWT
        self.FLASK_JWT = env.str('FLASK_JWT', None)
        self.JWT_ACCESS_TOKEN_EXPIRES = env.int('JWT_ACCESS_TOKEN_EXPIRES', None)

        # MONGODB
        self.MONGODB_URI = env.str('MONGODB_URI', "mongodb://localhost:27017")
        self.MONGODB_DATABASE = env.str('MONGODB_DATABASE', "barbuc-api")
        self.MONGODB_CONNECT = False

        # PASSWORD CUSTOM SALT
        self.SECURITY_PASSWORD_SALT = env.str('SECURITY_PASSWORD_SALT', "123456")

        # OPENAPI
        self.API_TITLE = self.SERVICE_NAME
        self.API_VERSION = env.str('CI_COMMIT_REF_NAME', "dev")
        self.OPENAPI_VERSION = "3.0.2"


    @property
    def mongodb_settings(self):
        return {
            'host': f'{self.MONGODB_URI}/{self.MONGODB_DATABASE}',
            'db': self.MONGODB_DATABASE,
            'connect': self.MONGODB_CONNECT,
        }

    @property
    def logger_config(self):
        return {
            'version': 1,
            'formatters': {
                'color_formatter': {
                    '()': 'colorlog.ColoredFormatter',
                    'format': "%(log_color)s%(asctime)s | %(levelname)-8s | %(message)s"
                }
            },
            'handlers': {
                'console': {
                    'class': 'colorlog.StreamHandler',
                    'level': self.LOGGER_LEVEL,
                    'formatter': 'color_formatter'
                },
            },
            'loggers': {
                'console': {
                    'level': self.LOGGER_LEVEL,
                    'propagate': False,
                    'handlers': ['console']
                }
            }
        }

    @property
    def json(self):
        return {key: self.__getattribute__(key) for key in self.__dir__() if not key.startswith('_') and key.isupper()}

    def validate(self):
        if not self.MONGODB_URI:
            raise ValueError("Mongo URI is not defined")


config = Config()
