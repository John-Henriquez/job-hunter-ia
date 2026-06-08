# Changelog

## [v0.4.1] - 2026-06-08

### Added

- Repository Layer para acceso a datos
- Service Layer para lógica de negocio
- Provider Layer para futuras fuentes de vacantes
- GetOnBoardProvider inicial
- Flujo completo Provider → Service → Repository → PostgreSQL

### Changed
- Refactor de main.py para utilizar la arquitectura modular
- Eliminación de inserciones directas a base de datos desde el punto de entrada
### Notes
- El sistema ya permite incorporar nuevas fuentes de vacantes sin modificar la capa de persistencia.
- La integración real con GetOnBoard queda planificada para la versión 0.5.0.

## [v0.4.0] 2026-06-08

### Added

- Repository Layer
- Service Layer
- JobRepository
- JobService
- CRUD básico para entidad Job
- Separación de responsabilidades entre acceso a datos y lógica de negocio
- Persistencia desacoplada mediante SQLAlchemy

### Changed

- Refactor de main.py
- Arquitectura modular consolidada

## [v0.3.0] 2026-06-08
### Added
- PostgreSQL integration via Docker
- SQLAlchemy ORM setup
- Job model
- Insert + query working
- Basic main execution flow

## [0.2.0] - 2026-06-08

### Added

- Estructura modular inicial
- Entorno virtual Python
- Docker Desktop
- Docker Compose
- PostgreSQL en contenedor Docker
- README inicial