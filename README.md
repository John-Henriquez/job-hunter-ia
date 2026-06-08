# Job Hunter IA

## Descripción

Job Hunter IA es una plataforma de automatización para búsqueda laboral enfocada en perfiles tecnológicos.

Su objetivo es recopilar ofertas laborales desde múltiples fuentes, almacenarlas en una base de datos centralizada y analizarlas en función del perfil profesional del usuario para identificar oportunidades relevantes y optimizar el proceso de postulación.

Además de ser una herramienta práctica, el proyecto sirve como laboratorio de aprendizaje y portafolio profesional en áreas como automatización, desarrollo backend, bases de datos, scraping, análisis de datos e inteligencia artificial.

---
## Estado del proyecto

Versión actual: 0.4.1
Backend funcional con persistencia en PostgreSQL
Arquitectura modular Repository-Service implementada
Preparado para integración de fuentes reales de vacantes

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

Versión: **0.4.1**

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

### Próximos Pasos
* [ ] Primer módulo de scraping
* [ ] Normalización de datos de vacantes
* [ ] Implementación de Providers
* [ ] Persistencia desacoplada de fuentes externas
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

### v0.5.0
* Integración real con GetOnBoard
* Descarga automática de vacantes
* Conversión a entidades Job
* Persistencia automática
* Prevención de duplicados

### v0.6.0
* Segundo proveedor de vacantes
* Normalización de datos entre fuentes

### v0.7.0
* Sistema de filtros
* Búsqueda por tecnologías
* Ranking inicial de vacantes

### v0.8.0
* Dashboard de estadísticas
* Métricas de búsqueda laboral

### v0.9.0
* Integración IA
* Matching perfil ↔ vacantes

### v1.0.0
* MVP funcional completo

---

## Autor

John Henriquez

Ingeniero en Ejecución en Computación e Informática
