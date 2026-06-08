# Job Hunter IA

## Descripción

Job Hunter IA es una plataforma de automatización para búsqueda laboral enfocada en perfiles tecnológicos.

Su objetivo es recopilar ofertas laborales desde múltiples fuentes, almacenarlas en una base de datos centralizada y analizarlas en función del perfil profesional del usuario para identificar oportunidades relevantes y optimizar el proceso de postulación.

Además de ser una herramienta práctica, el proyecto sirve como laboratorio de aprendizaje y portafolio profesional en áreas como automatización, desarrollo backend, bases de datos, scraping, análisis de datos e inteligencia artificial.

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
    ├── core/
    ├── models/
    ├── providers/
    ├── repositories/
    ├── services/
    ├── utils/
    └── main.py
```

---

## Estado Actual

Versión: **0.2.0**

### Completado

* [x] Estructura inicial del proyecto
* [x] Entorno virtual
* [x] Configuración Docker
* [x] PostgreSQL en contenedor Docker

### Próximos Pasos

* [ ] Configuración SQLAlchemy
* [ ] Conexión Python → PostgreSQL
* [ ] Modelo Job
* [ ] Persistencia básica

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

### v0.1.0

* Estructura base del proyecto

### v0.2.0

* Docker y PostgreSQL

### v0.3.0

* Conexión SQLAlchemy
* Entidades principales

### v0.4.0

* Persistencia de datos

### v0.5.0

* Primer proveedor de vacantes

### v1.0.0

* MVP funcional

---

## Autor

John Henriquez

Ingeniero en Ejecución en Computación e Informática
