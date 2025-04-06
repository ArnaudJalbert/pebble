import pytest

from pebble.infrastructure.factories import MongoConnectionError, MongoConnectionFactory


@pytest.fixture
def wrong_uri_connection() -> MongoConnectionFactory:
    """
    Test the MongoDB connection with an incorrect URI.
    """
    good_uri = MongoConnectionFactory.CONNECTION_URI
    MongoConnectionFactory.CONNECTION_URI = "mongodb://wrong_uri{password}"
    yield MongoConnectionFactory
    MongoConnectionFactory.CONNECTION_URI = good_uri


@pytest.fixture
def no_password_connection() -> MongoConnectionFactory:
    """
    Test the MongoDB connection with no password.
    """
    good_password = MongoConnectionFactory.MONGO_PASSWORD
    MongoConnectionFactory.MONGO_PASSWORD = None
    yield MongoConnectionFactory
    MongoConnectionFactory.MONGO_PASSWORD = good_password


def test_mongo_connection() -> None:
    """
    Test the MongoDB connection.
    """
    assert MongoConnectionFactory.CONNECTION_URI is not None
    assert MongoConnectionFactory.MONGO_PASSWORD is not None
    assert MongoConnectionFactory.SERVER_API_VERSION is not None
    assert MongoConnectionFactory.PING is not None
    assert MongoConnectionFactory.get_mongo_client is not None

    mongo_client = MongoConnectionFactory.get_mongo_client()
    assert mongo_client is not None
    assert mongo_client.server_info() is not None


def test_mongo_connection_error(wrong_uri_connection: MongoConnectionFactory) -> None:
    """
    Test the MongoDB connection error.
    """
    with pytest.raises(MongoConnectionError):
        wrong_uri_connection.get_mongo_client()


def test_mongo_connection_no_password(
    no_password_connection: MongoConnectionFactory,
) -> None:
    """
    Test the MongoDB connection with no password.
    """
    assert no_password_connection.MONGO_PASSWORD is None
    with pytest.raises(MongoConnectionError):
        no_password_connection.get_mongo_client()
