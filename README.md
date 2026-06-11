# Job Hunter IA

## Descripción

Job Hunter IA es una plataforma de automatización para búsqueda laboral enfocada en perfiles tecnológicos.

Su objetivo es recopilar ofertas laborales desde múltiples fuentes, almacenarlas en una base de datos centralizada y analizarlas en función del perfil profesional del usuario para identificar oportunidades relevantes y optimizar el proceso de postulación.

Además de ser una herramienta práctica, el proyecto sirve como laboratorio de aprendizaje y portafolio profesional en áreas como automatización, desarrollo backend, bases de datos, scraping, análisis de datos e inteligencia artificial.

---
## Estado del proyecto

Versión actual: 0.5.3
Backend funcional con persistencia en PostgreSQL
Integración real con GetOnBoard API 
Arquitectura modular Repository-Service-Provider implementada

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
* Ruff

### Futuras Integraciones

* OpenAI API
* Ollama
* Embeddings semánticos
* Automatización de postulaciones

---

## Arquitectura

```text
src/
└── job_hunter/
    ├── config/
    ├── models/
    ├── repositories/
    ├── services/
    └── main.py
```

---

## Estado Actual

Versión: **0.5.3**

### Completado

* [x] Estructura inicial del proyecto
* [x] Entorno virtual
* [x] Configuración Docker
* [x] PostgreSQL en contenedor Docker

* [x] Configuración SQLAlchemy
* [x] Conexión Python → PostgreSQL
* [x] Modelo Job
* [x] Persistencia básica

* [x] Repository Layer
* [x] Service Layer
* [x] CRUD básico de Jobs
* [x] Refactor de main.py

* [x] Arquitectura de Providers
* [x] BaseProvider
* [x] GetOnBoardProvider integrado con API oficial
* [x] Modelo RawJob (staging layer)
* [x] RawJobRepository + RawJobService

* [x] Descarga automática de vacantes por categoría
* [x] Persistencia de vacantes crudas en PostgreSQL
* [x] Prevención de duplicados por external_id
* [x] ProviderRegistry: register(), get_all(), get_by_name()

### Próximos Pasos

### Próximos Pasos
* [ ] FetchService como orquestador del pipeline
* [ ] main.py reducido a punto de entrada puro
* [ ] Estructura de tests base
* [ ] Normalización RawJob → Job

---

## Instalación

```bash
git clone <url-del-repositorio>

cd job-hunter-ia

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

docker compose up -d
```

---

## Roadmap

### v0.1.0 ✅
* Estructura base del proyecto

### v0.2.0 ✅
* Docker y PostgreSQL

### v0.3.0 ✅
* SQLAlchemy
* Modelo Job
* Conexión con PostgreSQL

### v0.4.0 ✅
* Repository Pattern
* Service Layer
* Persistencia desacoplada

### v0.4.1 ✅
* Arquitectura de Providers
* BaseProvider
* GetOnBoardProvider (stub)
* Limpieza de flujo de pruebas

### v0.5.0✅
* Integración real con GetOnBoard
* Descarga automática de vacantes
* Modelo RawJob como capa de staging
* RawJobRepository + RawJobService
* Persistencia automática con prevención de duplicados

### v0.5.1 ✅
* Limpieza de dependencias muertas (curl_cffi)
* DB_ECHO configurable via .env
* Deduplicación delegada completamente al service
* Correcciones menores en main.py

### v0.5.2✅
* BaseProvider con contrato robusto (source_name, source_version, is_active)
* parse_jobs() como método abstracto obligatorio
* GetOnBoardProvider actualizado al nuevo contrato

### v0.5.3✅
* ProviderRegistry: register(), get_all(), get_by_name()
* Providers desacoplados de main.py

### v0.5.4
* FetchService como orquestador del pipeline fetch → parse → save
* main.py reducido a punto de entrada puro (~10 líneas)

### v0.5.5
* Estructura tests/ establecida
* Tests de RawJobService con mock de repository
* Tests de parse_jobs() con payload fijo

### v0.6.0
* Normalización RawJob → Job
* JobNormalizer como clase independiente
* RawJob.processed = True tras normalización
* Relación FK entre Job y RawJob

### v0.7.0
* Segundo proveedor de vacantes
* Normalización agnóstica al proveedor
* Estandarización de datos entre fuentes

### v0.8.0
* API REST mínima con FastAPI
* GET /jobs, GET /jobs/{id}
* Reemplaza necesidad de cliente visual para observabilidad

### v0.9.0
* Sistema de filtros y búsqueda por tecnologías
* Scoring básico por relevancia
* Matching perfil ↔ vacantes

### v0.10.0
* Integración IA
* Embeddings semánticos
* Matching inteligente

### v1.0.0
* MVP funcional completo
* Automatización de postulaciones
* Notificaciones

---

## Autor

John Henriquez

Ingeniero en Ejecución en Computación e Informática
