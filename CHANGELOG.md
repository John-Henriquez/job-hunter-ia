# Changelog

## [v1.2.0] - 2026-06-24

### Added
- `JobRepository.search()`: filtros y paginación ejecutados en SQL (ilike, offset, limit)
- Parámetro `search` y `work_mode` en GET /jobs/ para búsqueda y filtro adicional
- Banner de error visible en frontend para fallos de red o HTTP
- Debounce de 350ms en búsqueda de texto del frontend

### Changed
- Frontend ya no carga todos los jobs en memoria — cada filtro/página dispara una request
- apiFetch() extrae el campo `detail` de errores JSON de FastAPI
- updateApplicationStatus() recarga desde el servidor en vez de mutar estado local

### Results
- Paginación y filtros escalan más allá de los ~2000 registros actuales
- Errores de conexión o HTTP visibles para el usuario en vez de fallar en silencio

## [v1.1.0] - 2026-06-24

### Added
- Alembic configurado para migraciones de esquema futuras
- env.py de Alembic integrado con DATABASE_URL del proyecto y target_metadata de los modelos
- Migración inicial (baseline) registrada con `alembic stamp head`

### Fixed
- `load_dotenv()` en database.py ahora usa path explícito a la raíz del proyecto
- Conflicto de puerto 5432 resuelto deteniendo servicios nativos de PostgreSQL en Windows

## [v1.0.1] - 2026-06-17

### Fixed
- Raw job deduplication now uses `source` + `external_id` to avoid collisions between providers.
- Existing unprocessed raw jobs are retried instead of being skipped forever.
- Raw jobs are marked as processed only after a normalized `Job` is created successfully.
- `/health` now reads `VERSION` using a stable project path instead of the current working directory.
- FastAPI app metadata now uses the same version source as `/health`.

### Added
- Tests for fetch retry/skip behavior around processed raw jobs.
- Tests for `/health` version consistency.

## [v1.0.0] - 2026-06-11

### Added
- Frontend completo en HTML/CSS/JS vanilla servido desde FastAPI
- Tabla paginada de vacantes con 25 por página
- Filtros por fuente, modalidad, work mode y seniority
- Búsqueda en tiempo real por título y empresa
- Vista detalle de cada vacante en modal
- Botones de refresh por provider y global
- Polling de estado del fetch con feedback en tiempo real
- Panel de estadísticas en sidebar
- Endpoints POST /fetch/ y POST /fetch/{provider}
- GET /fetch/status para polling del estado

### Changed
- app.py sirve archivos estáticos y redirige / al frontend
- version bumped a 1.0.0

### Results
- Sistema completo funcional: docker compose up → frontend en localhost:8000
- 2086 vacantes de 2 fuentes consultables con filtros
- Refresh de datos desde el propio frontend

## [v0.9.0] - 2026-06-11

### Fixed
- `published_at` corregido en todos los jobs (2086/2086)
- `work_mode` normalizado a 3 valores: remote, hybrid, on-site
- `published_at` agregado al flujo create_job en FetchService y JobService
- Normalizers corregidos para persistir published_at correctamente

### Changed
- `job_service.py` acepta `published_at` como parámetro
- `fetch_service.py` pasa `published_at` al crear Job
- Mapeo de work_mode: fully_remote/remote_local → remote, no_remote → on-site

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
