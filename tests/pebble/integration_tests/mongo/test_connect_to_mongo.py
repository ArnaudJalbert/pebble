from unittest.mock import MagicMock, patch

import pytest

from pebble.infrastructure.factories import MongoConnectionError, MongoConnectionFactory


def test_mongo_connection() -> None:
    """
    Test the MongoDB connection.
    """
    assert MongoConnectionFactory.CONNECTION_URI is not None
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
