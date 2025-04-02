# Pebble

Pebble is a minimalist tracking application designed with Clean Architecture principles. It provides a flexible core that can be implemented with multiple interfaces (CLI, Web, Mobile) and supports various data access methods (local storage, databases, cloud services). The goal of Pebble is to offer a lightweight yet extensible tracking solution adaptable to different use cases.

## Features
- Modular and maintainable codebase following Clean Architecture principles.
- Support for multiple user interfaces (CLI, Web, Mobile).
- Pluggable data storage options (file-based, relational DB, NoSQL, cloud storage).
- Minimalist design for simplicity and ease of use.
- Extensible domain logic to accommodate custom tracking needs.

## Architecture Overview
Pebble is structured around Clean Architecture, ensuring separation of concerns and flexibility. The application is divided into the following layers:

### 1. **Domain Layer** (Core Business Logic)
- Defines essential tracking entities and business rules.
- Independent of frameworks and external services.

### 2. **Application Layer** (Use Cases)
- Implements business logic as use cases.
- Acts as a bridge between the domain layer and external layers.

### 3. **Interface Adapters** (Presentation & Data Access)
- Includes UI implementations (CLI, Web, Mobile).
- Provides repositories for data access (file storage, databases, cloud APIs).

### 4. **Infrastructure Layer** (External Services & Frameworks)
- Handles concrete implementations of repositories.
- Manages external services (authentication, analytics, etc.).

## Contributing
Contributions are welcome! Please follow the established code architecture and ensure modularity when adding features.

1. Fork the repository.
2. Create a new branch for your feature/fix.
3. Commit and push your changes.
4. Submit a pull request.

## License
Pebble is licensed under the MIT License. See [LICENSE](LICENSE) for details.
