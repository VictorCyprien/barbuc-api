import pytest

def test_default_config():
    """ Test that default conf raise a value error, some var env are needed
    """
    from barbuc_api.config import config
    config.MONGODB_URI = None
    with pytest.raises(ValueError):
        config.validate()


def test_config():
    from barbuc_api.config import config
    config.MONGODB_URI = "mongomock://localhost"
    config.MONGODB_DATABASE = "BaseDeTest"
    config.validate()

    assert "DEBUG" == config.LOGGER_LEVEL
    assert "mongomock://localhost" == config.MONGODB_URI
    assert "BaseDeTest" == config.MONGODB_DATABASE
