# Changelog

## [v0.8.0] - 2026-06-11

### Added
- API REST con FastAPI
- GET /jobs/ con filtros: source, category, seniority, modality, page, per_page
- GET /jobs/{job_id} con detalle completo incluyendo description
- GET /stats/ con totales por fuente, categoría, seniority y modality
- GET /health con versión del sistema
- Documentación automática en /docs
- Estructura api/: app.py, server.py, dependencies.py, routers/

### Results
- 2086 vacantes consultables via API REST
- Swagger UI funcional en http://localhost:8000/docs

## [v0.7.0] - 2026-06-11

### Added
- CLI con argparse: comandos `fetch` y `stats`
- `fetch --provider {nombre}` para correr un provider específico
- `ArbeitnowProvider` con paginación y delay anti rate-limit
- `ArbeitnowNormalizer` con mapeo completo al modelo Job
- `get_normalizer()` en `BaseProvider` como parte del contrato
- Arquitectura multi-provider: cada provider lleva su propio normalizer

### Changed
- `BaseProvider` extendido con método abstracto `get_normalizer()`
- `GetOnBoardProvider` implementa `get_normalizer()`
- `FetchService` obtiene el normalizer desde el provider, no como dependencia externa
- `main.py` refactorizado con argparse y función `build_registry()`
- `external_id` en `RawJob` ampliado a VARCHAR(500)

### Fixed
- Rate limit 429 de Arbeitnow resuelto con delay de 2s entre páginas
- StringDataRightTruncation en external_id resuelto ampliando columna

### Results
- 2086 jobs totales: 1102 GetOnBoard + 984 Arbeitnow
- 0 fallos de normalización en ambos providers

## [v0.6.1] - 2026-06-10

### Added

- Interfaz CLI inicial para ejecutar Job Hunter IA desde terminal.
- Punto de entrada simplificado para operaciones de scraping y normalización.
- Mensajes de ejecución y resultados estandarizados para el usuario.
- Separación más clara entre bootstrap de aplicación y lógica de negocio.

### Changed

* Flujo principal reorganizado para soportar crecimiento futuro del CLI.

### Results

- Pipeline completo de ingesta, persistencia y normalización accesible desde CLI.
- Proyecto preparado para incorporación de nuevos providers sin modificar el punto de entrada principal.


## [v0.6.0] - 2026-06-10

### Added
- Carpeta `normalizers/` con `BaseNormalizer` y `GetOnBoardNormalizer`
- `GetOnBoardNormalizer` con cache lazy de companies (249 únicas)
- Lookup completo de seniorities y modalities al inicializar
- Campos `seniority`, `modality`, `category` en modelo `Job`
- Pipeline completo: RawJob → normalización → Job persistido
- `FetchService` actualizado para orquestar normalización post-fetch
- `JobService.create_job` actualizado con campos nuevos

### Changed
- `main.py` actualizado con `JobRepository` y `GetOnBoardNormalizer`
- `FetchService` recibe `job_repository` y `normalizer` como dependencias

### Results
- 1094 vacantes descargadas, normalizadas y persistidas
- 0 fallos de normalización

## [v0.5.5] - 2026-06-10

### Added
- Estructura `tests/` en raíz del proyecto
- `tests/test_raw_job_service.py`: 2 tests con mocks (nuevo y duplicado)
- `tests/test_getonboard_provider.py`: 4 tests de parse_jobs()
- pytest agregado a requirements.txt

### Fixed
- curl_cffi, cffi y pycparser eliminados definitivamente de requirements.txt

## [v0.5.4] - 2026-06-10

### Added
- `FetchService` como orquestador del pipeline fetch → parse → save
- `FetchService.run()` retorna dict con totales de guardados y duplicados

### Changed
- `main.py` reducido a punto de entrada puro (~15 líneas)
- Lógica de iteración, conteo y persistencia movida completamente a `FetchService`

## [v0.5.3] - 2026-06-10

### Added
- `ProviderRegistry` con métodos `register()`, `get_all()`, `get_by_name()`, `list_registered()`
- Registro automático omite providers inactivos (`is_active = False`)

### Changed
- `main.py` refactorizado para usar `ProviderRegistry`
- El loop principal itera sobre providers registrados, no instancias directas
- Conteo de guardados y duplicados por provider y resumen total

## [v0.5.2] - 2026-06-10

### Changed
- `BaseProvider` refactorizado con contrato robusto
- `source_name` y `source_version` como propiedades abstractas obligatorias
- `is_active` con valor por defecto `True` para desactivar providers sin eliminarlos
- `parse_jobs()` incorporado al contrato como método abstracto con firma tipada
- `GetOnBoardProvider` actualizado para cumplir el nuevo contrato
- Constante `SOURCE` reemplazada por propiedad `source_name`

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