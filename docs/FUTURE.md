# Roadmap v2.0 - Job Hunter IA

Este documento organiza la evolucion posterior a v1.0.0. El foco es avanzar por
capas: primero confiabilidad y flujo personal, luego analitica, IA y producto.

## Estado Actual

### Completado
- [x] MVP funcional con API REST, frontend y pipeline multi-provider.
- [x] Dedupe de `RawJob` por `source` + `external_id`.
- [x] Reintento de raws no procesados.
- [x] `/health` estable y versionado desde `VERSION`.
- [x] Frontend: mitigacion XSS en datos externos y links seguros.

### Deuda Tecnica Antes de Escalar
- [x] Migraciones con Alembic para cambios de esquema. Nota: `application_status`
      requiere migracion o `ALTER TABLE` en bases existentes.
- [x] Filtros, busqueda y paginacion server-side en `/jobs/`.
- [x] Manejo consistente de errores HTTP en el frontend.
- [x] Responsive real para mobile/tablet.
- [x] Facets dinamicos para filtros.

## v1.1.0 - Seguimiento Personal

Objetivo: convertir el dashboard en una herramienta diaria de busqueda laboral.

- [x] Marcar estado de una vacante: guardada, postulada, en proceso, descartada.
- [ ] Persistir notas personales por vacante.
- [x] Filtros por estado personal.
- [ ] Estadisticas personales: postuladas, en proceso, descartadas, tasa de avance.
- [ ] Exportacion CSV/Excel del listado filtrado.

## v1.2.0 - Analitica de Mercado

Objetivo: descubrir patrones utiles en las ofertas recolectadas.

- [ ] Normalizar tecnologias/tags desde descripcion y categoria.
- [ ] Tendencias por periodo, fuente y modalidad.
- [ ] Ranking de tecnologias mas demandadas.
- [ ] Alertas de tecnologias en crecimiento.

## v1.3.0 - Matching Perfil/Vacante

Objetivo: priorizar oportunidades segun un perfil profesional real.

- [ ] Perfil base en JSON/YAML: skills, experiencia, preferencias y restricciones.
- [ ] Scoring explicable por vacante.
- [ ] Filtros por score minimo.
- [ ] Razones de match y gaps principales.

## v1.4.0 - CV Adaptativo

Objetivo: ayudar a postular mejor sin inventar informacion.

- [ ] CV base estructurado.
- [ ] Generacion de variantes orientadas a cada oferta.
- [ ] Reglas anti-alucinacion: solo reordenar, resumir y enfatizar informacion existente.
- [ ] Exportacion a PDF.

## v1.5.0 - Automatizacion

Objetivo: reducir tareas repetitivas y aumentar oportunidad de reaccion.

- [ ] Scheduler para fetch periodico.
- [ ] Notificaciones de nuevas ofertas relevantes.
- [ ] Watchlists por tecnologia, seniority, fuente y modalidad.
- [ ] Resumen diario/semanal.

## v2.0.0 - Producto

Objetivo: preparar una version usable por mas personas.

- [ ] Multiusuario.
- [ ] Autenticacion.
- [ ] Panel de administracion.
- [ ] Configuracion por usuario.
- [ ] Empaquetado/deploy reproducible.
