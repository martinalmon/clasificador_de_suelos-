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


## ADR-004 - Cuentas y créditos con Firebase

Fecha: 2026-11-16.
Estado: arquitectura aceptada; implementación parcial.

Se incorpora Firebase Authentication y Firestore a v1.
Esto actualiza la exclusión de cuentas del contexto inicial.

La inicialización de cuenta concede 10 créditos mediante transacción.
Una cuenta existente conserva su saldo.

Se acuerda cobrar un crédito por clasificación nueva válida.
Todas las descargas de su PDF son gratuitas, incluida la primera.
El descuento y el guardado atómicos, la idempotencia, el historial
y los reportes PDF están pendientes.

El desarrollo actual utiliza emuladores con demo-sucs-local.
La producción requiere configuración y validación independientes.