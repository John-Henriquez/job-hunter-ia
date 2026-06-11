# Changelog

## [v0.5.1] - 2026-06-10

### Changed
- `echo=True` reemplazado por variable de entorno `DB_ECHO` en `database.py`
- Deduplicación de `main.py` delegada completamente a `RawJobService`
- Print de resultados movido fuera del loop en `main.py`

### Fixed
- Typo `reporsitory` → `repository` en `main.py`
- Typo `\Resultados` → `\nResultados` en `main.py`

### Removed
- `curl_cffi`, `cffi` y `pycparser` eliminados de `requirements.txt`

## [v0.5.0] - 2026-06-10

### Added
- GetOnBoardProvider integrado con API pública oficial 
- Descarga automática de vacantes iterando las categorías disponibles
- Modelo RawJob como capa de staging con campo JSONB para payload crudo
- RawJobRepository con métodos create, get_by_external_id, get_unprocessed
- RawJobService con lógica de deduplicación por external_id
- Persistencia de 1098+ vacantes en PostgreSQL en primera ejecución

### Changed
- main.py refactorizado para usar RawJobService en lugar de JobService
- getonboard_provider.py reemplazado: eliminado curl_cffi y cookies hardcodeadas
- database.py: dotenv_path explícito para resolver carga de variables de entorno
- requirements.txt actualizado con dependencias limpias

### Fixed
- Resolución de problema de autenticación PostgreSQL por carga incorrecta del .env
- Endpoint corregido de jobs.json (500) a /api/v0/categories/{id}/jobs

### Notes
- La API pública de GetOnBoard no requiere autenticación ni scraping
- RawJob almacena el payload completo en JSONB para normalización posterior

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