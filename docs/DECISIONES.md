# Registro de decisiones

## ADR-001 — Flutter + Python
Fecha: 2026-11-08
Estado: aceptada
Razón: mantener la UI Flutter en Android Studio y lógica geotécnica Python reutilizable.
Consecuencia: si se usa FastAPI alojada remotamente la app necesita conexión. La variante offline requiere decisión futura, no está incluida.

## ADR-002 — Monorepo sencillo
Estado: aceptada
Un repositorio con `mobile`, `backend` y `docs`. Evita infraestructura y múltiples repositorios no justificados (KISS/YAGNI).

## ADR-003 — Sin predicción geológica en v1
Estado: aceptada
Se pospone el aprendizaje automático y las cartas geológicas para v2.
