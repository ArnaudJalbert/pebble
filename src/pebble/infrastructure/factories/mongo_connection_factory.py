import dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()


class MongoConnectionError(Exception):
    """Custom exception for MongoDB connection errors."""


class MongoConnectionFactory:
    """
    MongoDB Connector class for connecting to a MongoDB database.
    """

    CONNECTION_URI: str = "mongodb+srv://arnojalbert:{password}@pebble.ihk2yd6.mongodb.net/?appName=pebble"
    MONGO_PASSWORD: str = dotenv.dotenv_values().get("MONGO_PASSWORD")
    SERVER_API_VERSION: str = "1"
    PING: str = "ping"

    @classmethod
    def get_mongo_client(cls) -> MongoClient:
        uri: str = cls.CONNECTION_URI.format(password=cls.MONGO_PASSWORD)

        # Create a new client and connect to the server
        client: MongoClient = MongoClient(
            uri, server_api=ServerApi(cls.SERVER_API_VERSION)
        )

        # Send a ping to confirm a successful connection
        try:
            client.admin.command(cls.PING)
        except Exception as e:
            raise MongoConnectionError(f"Failed to connect to MongoDB: {e}")

        return client
