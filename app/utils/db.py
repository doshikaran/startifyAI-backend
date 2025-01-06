from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConfigurationError
import logging
from app.config import settings

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        self._connect()

    def _connect(self):
        """
        Establish a MongoDB connection using the provided settings.
        """
        try:
            self.client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
            
            # Use 'default_db' if no database name is specified in the connection string
            database_name = "default_db"
            self.db = self.client[database_name]
            
            # Test connection by attempting to ping the server
            self.client.admin.command('ping')
            logger.info(f"MongoDB connection established successfully with database '{database_name}'.")
        except (ServerSelectionTimeoutError, ConfigurationError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise e

    def get_collection(self, collection_name: str):
        """
        Retrieve a MongoDB collection.
        """
        if self.db is None:
            raise ServerSelectionTimeoutError("No active database connection.")
        return self.db[collection_name]

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")


# Singleton instance of MongoDB
mongodb = MongoDB()

# Explicitly define `get_collection`
def get_collection(collection_name: str):
    return mongodb.get_collection(collection_name)