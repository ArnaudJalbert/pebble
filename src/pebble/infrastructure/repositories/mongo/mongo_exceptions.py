class MongoError(Exception):
    """
    Base class for all exceptions raised by the MongoDB repository.
    """


class MongoHabitExistsError(MongoError):
    """
    Exception raised when a habit already exists in the repository.
    """
