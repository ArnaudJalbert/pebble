from unittest.mock import MagicMock, patch

import pytest

from pebble.infrastructure.factories import MongoConnectionError, MongoConnectionFactory


@pytest.fixture
def wrong_uri_connection() -> MongoConnectionFactory:
    """
    Test the MongoDB connection with an incorrect URI.
    """
    good_uri = MongoConnectionFactory.CONNECTION_URI
    MongoConnectionFactory.CONNECTION_URI = "mongodb://wrong_uri"
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


@patch(
    "pebble.infrastructure.factories.mongo_connection_factory.MongoConnectionFactory.CONNECTION_URI"
)
def test_mongo_connection_error(uri_patch: MagicMock) -> None:
    """
    Test the MongoDB connection error.
    """
    uri_patch.return_value = "mongodb://wrong_uri"
    assert MongoConnectionFactory.CONNECTION_URI is uri_patch
    with pytest.raises(MongoConnectionError):
        MongoConnectionFactory.get_mongo_client()


@patch(
    "pebble.infrastructure.factories.mongo_connection_factory.MongoConnectionFactory.MONGO_PASSWORD"
)
def test_mongo_connection_no_password(password_patch: MagicMock) -> None:
    """
    Test the MongoDB connection with no password.
    """
    password_patch.return_value = None
    assert MongoConnectionFactory.MONGO_PASSWORD is password_patch
    with pytest.raises(MongoConnectionError):
        MongoConnectionFactory.get_mongo_client()
