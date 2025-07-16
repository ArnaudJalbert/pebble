# Changelog

## 0.9.0 - TAS-536 - 15-07-2025
  - General use case to retrieve habits between two dates.

## 0.8.0 - TAS-532 - 20-06-2025
  - Add base API setup using FastAPI.
  - Add `FastAPI` dependency.
  - Add `TOML` dependency.
  - Add `uvicorn` dependency for running the FastAPI app.
  - Add `httpx` dependency for the FastAPI client.

## 0.7.0 - TAS-429 - 11-05-2025:
  - Concrete implementation of the MongoHabitRepository.
  - Add a serializers for the entities.
  - Tests for all the implementation of repository and serializer.
  - Renamed the `infrastructure` module to `interface_adapters`.

## 0.6.2 - TAS-428- 07-04-2025
  - Class definition for the MongoHabitRepository.
  - Add `mongomock` dependency.

## 0.6.1 - TAS-433 - 07-04-2025
  - Add annotations to general types.
  - Change datetime by date for the habit instance entity.

## 0.6.0 - TAS-427 - 06-04-2025
  - Factory to connect to Mongo and get a Mongo client.
  - Integration test for the Mongo connection.
  - Added loadenv and pymongo as dependencies.
  - Add `.env` file to the repository, for Mongo password, reflected in GitHub secrets.
  - Update CI to run unit tests and integration tests separately.

## 0.5.0 - TAS-407+TAS-411 - 06-04-2025
  - Add use case for creating a habit instances.
  - Make all imports in the entity module relative to the domain module.
  - Add tests for the new use case.
  - Ruff format + check on tests.

## 0.4.2 - TAS-423 - 02-04-2025:
  - Run tests only on pull request.

## 0.4.1 - TAS-422 - 02-04-2025:
  - Add basic README.

## 0.4.0 - TAS-406 - 01-04-2025:
  - Add use case for creating a habit collection.
  - Add tests for new use case.
  - Hash function for the habit entity.

## 0.3.0 - TAS-409 - 30-03-2025:
  - Add ruff to the project.
  - Add ruff check configuration.
  - Add ruff format configuration.
  - Add uv lock to the CI pipeline.
  - Add ruff check to the CI pipeline.
  - Add ruff format to the CI pipeline.
  - Add unit tests to the CI pipeline.
  - Add build to the CI pipeline.
  - Fix all ruff rules infringements.

## 0.2.0 - TAS-404 - 30-03-2025:
  - Adding use case to create a habit category.
  - Changing the `create_new_habit` use case name to `create_habit`.
  - Adding tests to validate the new use case.
  - Adding import of use case in the `use_cases` module.
  - Remove `isort` dependency from the project.