from enum import Enum
from werkzeug.exceptions import Unauthorized as WerkzeugUnauthorized
from werkzeug.exceptions import Forbidden as WerkzeugForbidden
from werkzeug.exceptions import NotFound as WerkzeugNotFound
from werkzeug.exceptions import BadRequest as WerkzeugBadRequest


class Forbidden(WerkzeugForbidden):
    """ Forbidden error customized for default smorest error handler

    >>> err = Forbidden("An important message")
    >>> err.data
    {'message': 'An important message'}
    """
    def __init__(self, message: str = None) -> None:
        super().__init__()
        if message:
            self.data = {}
            self.data["message"] = message


class Unauthorized(WerkzeugUnauthorized):
    """ Unauthorized error customized for default smorest error handler

    >>> err = Unauthorized("An important message")
    >>> err.data
    {'message': 'An important message'}
    """
    def __init__(self, message: str = None) -> None:
        super().__init__()
        if message:
            self.data = {}
            self.data["message"] = message


class BadRequest(WerkzeugBadRequest):
    """ BadRequest error customized for default smorest error handler

    >>> err = BadRequest("An important message")
    >>> err.data
    {'message': 'An important message'}
    """
    def __init__(self, message: str = None) -> None:
        super().__init__()
        if message:
            self.data = {}
            self.data["message"] = message


class ReasonError(Enum):
    NOT_AUTHENTICATED = "You must be logged in to perform this action"
    AUTHENTICATION_FAILED = "Authentication failed"
    BAD_CREDENTIALS = "The email or password is incorrect"
    BAD_AUTH_TOKEN = "The token is present but incorrect"
    MISSING_AUTH_TOKEN = "The token is missing"
    WRONG_AUTH_TOKEN = "The token is present but invalid"
    UPDATE_USER_ERROR = "An error has occured during profil update, please try again"
    USER_NOT_FOUND = "The user does not exist"
    USER_ID_INVALID = "User ID is invalid"
    INVALID_PASSWORD = "Current password is incorrect"
    EMAIL_ALREADY_USED = "Unable to create this user, the email address is already in use"
    INVALID_EMAIL = "This email is invalid"
