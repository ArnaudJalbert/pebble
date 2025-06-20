class MongoError(Exception):
    """
    Base class for all exceptions raised by the MongoDB repository.
    """


class MongoHabitExistsError(MongoError):
    """
    Exception raised when a habit already exists in the repository.
    """


class MongoHabitNotFoundError(MongoError):
    """
    Exception raised when a habit is not found in the repository.
    """


class MongoHabitCategoryExistsError(MongoError):
    """
    Exception raised when a habit category already exists in the repository.
    """


class MongoHabitCollectionExistsError(MongoError):
    """
    Exception raised when a habit collection already exists in the repository.
    """


class MongoHabitCollectionNotFoundError(MongoError):
    """
    Exception raised when a habit collection is not found in the repository.
    """
