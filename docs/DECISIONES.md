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

<!-- GEOSTRATIX-20261116-84 -->

## Actualizacion de ADR-004

Fecha: 2026-11-16.
Estado: implementacion local validada.

La inicializacion de cuentas, el consumo
transaccional de creditos, la idempotencia
y el historial privado ya estan implementados.

Se reportaron 84 pruebas aprobadas.
La integracion con Flutter sigue pendiente.

## ADR-005 - Historial privado y gratuito

Fecha: 2026-11-16.
Estado: aceptada e implementada localmente.

Las clasificaciones se almacenan debajo
del UID del usuario autenticado.

La lista y la consulta individual
no consumen creditos.

Se utiliza paginacion mediante cursor.
La presentacion se ordena por fecha descendente.

La privacidad depende de comprobar
la identidad y restringir el acceso en backend.

## ADR-006 - Idempotencia de clasificaciones

Fecha: 2026-11-16.
Estado: aceptada e implementada localmente.

Cada nueva operacion utiliza
una cabecera Idempotency-Key.

Las operaciones existentes devuelven
su resultado sin descontar otro credito.

El guardado y el descuento se realizan
mediante una transaccion de Firestore.

La estrategia de retencion de registros
y el comportamiento bajo alta carga
requieren validacion adicional.

## ADR-007 - Separacion documental

Fecha: 2026-11-16.
Estado: aceptada.

docs/ contiene documentacion publicable.

privado/ contiene contexto interno del equipo
y esta excluida del seguimiento mediante Git.

No se almacenan secretos en ninguno
de los documentos.

Los respaldos locales no se deben subir
al repositorio publico.