# Job Hunter IA

## Descripción

Job Hunter IA es una plataforma de automatización para búsqueda laboral enfocada en perfiles tecnológicos.

Recopila ofertas laborales desde múltiples fuentes, las almacena en una base de datos centralizada y las analiza en función del perfil profesional del usuario para identificar oportunidades relevantes y optimizar el proceso de postulación.

Además de ser una herramienta práctica, el proyecto sirve como laboratorio de aprendizaje y portafolio profesional en áreas como automatización, desarrollo backend, bases de datos, scraping, análisis de datos e inteligencia artificial.

> Versión actual: **0.9.0** — Datos limpios, calidad de normalización completa.

---

## Objetivos

* Centralizar vacantes provenientes de distintas plataformas.
* Estandarizar información de ofertas laborales.
* Gestionar postulaciones y seguimiento.
* Implementar sistemas de puntuación y compatibilidad.
* Automatizar tareas repetitivas de búsqueda laboral.
* Incorporar análisis inteligente mediante IA.

---

## Stack Tecnológico

### Backend

* Python 3.x
* PostgreSQL
* SQLAlchemy

### Infraestructura

* Docker
* Docker Compose

### Calidad

* Pytest

### Futuras Integraciones

* FastAPI
* OpenAI API / Ollama
* Embeddings semánticos

---

## Arquitectura

```text
job-hunter-ia/
├── src/
│   └── job_hunter/
│       ├── config/
│       ├── models/
│       ├── providers/
│       ├── repositories/
│       ├── services/
│       └── main.py
└── tests/
```

## Instalación

```bash
git clone https://github.com/John-Henriquez/job-hunter-ia.git
cd job-hunter-ia
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
docker compose up -d
cd src
python -m job_hunter.main
```

---

## Roadmap

### v0.1.0 ✅
* Estructura base del proyecto

### v0.2.0 ✅
* Docker y PostgreSQL

### v0.3.0 ✅
* SQLAlchemy, Modelo Job, conexión con PostgreSQL

### v0.4.0 ✅
* Repository Pattern, Service Layer, persistencia desacoplada

### v0.4.1 ✅
* Arquitectura de Providers, BaseProvider, GetOnBoardProvider (stub)

### v0.5.0 ✅
* Integración real con GetOnBoard
* Descarga automática de vacantes
* Modelo RawJob como capa de staging
* RawJobRepository + RawJobService
* Persistencia automática con prevención de duplicados

### v0.5.1 ✅
* Limpieza de dependencias muertas
* DB_ECHO configurable via .env
* Correcciones en main.py

### v0.5.2 ✅
* BaseProvider con contrato robusto
* source_name, source_version, is_active
* parse_jobs() abstracto y tipado

### v0.5.3 ✅
* ProviderRegistry: register(), get_all(), get_by_name()
* Providers desacoplados de main.py

### v0.5.4 ✅
* FetchService como orquestador del pipeline
* main.py reducido a punto de entrada puro

### v0.5.5 ✅
* Estructura tests/ establecida
* 6 tests pasando (RawJobService + parse_jobs)
* requirements.txt limpio

### v0.6.0 ✅
* Normalización RawJob → Job
* GetOnBoardNormalizer con cache lazy de companies
* Lookup de seniorities y modalities
* Campos seniority, modality, category en modelo Job
* 1094 vacantes normalizadas, 0 fallos

### v0.6.1 ✅
* CLI inicial para ejecución del sistema
* Pipeline completo ejecutable desde terminal
* Refactor del punto de entrada principal
* Separación definitiva entre bootstrap y lógica de negocio

### v0.7.0✅
* ArbeitnowProvider + ArbeitnowNormalizer
* get_normalizer() en contrato BaseProvider
* 2086 jobs de dos fuentes, 0 fallos

### v0.8.0 ✅
* API REST con FastAPI
* GET /jobs/, GET /jobs/{id}, GET /stats/, GET /health
* Filtros por source, category, seniority, modality
* Swagger UI en /docs

### v0.9.0 ✅
* published_at corregido en 2086/2086 jobs
* work_mode normalizado a 3 valores: remote, hybrid, on-site
* Pipeline de normalización corregido para nuevos fetches

### v1.0.0 — Cierre de portafolio
* Frontend básico
* Tabla de vacantes paginada
* Filtros por fuente, categoría, seniority y modalidad
* Vista detalle de cada vacante
* docker compose up → sistema funcional completo sin configuración manual
* README profesional con capturas y ejemplos de uso

---

## Autor

John Henriquez

Ingeniero en Ejecución en Computación e Informática
