class MongoError(Exception):
    """
    Base class for all exceptions raised by the MongoDB repository.
    """


class MongoHabitExistsError(MongoError):
    """
    Exception raised when a habit already exists in the repository.
    """


class MongoHabitCategoryExistsError(MongoError):
    """
    Exception raised when a habit category already exists in the repository.
    """


class MongoHabitCollectionExistsError(MongoError):
    """
    Exception raised when a habit collection already exists in the repository.
    """
