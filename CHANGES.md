# Changelog

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