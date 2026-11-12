
# GeoStratix — Nuevas decisiones de arquitectura

**Fecha:** 12 de noviembre de 2026  
**Estado:** Documentación de decisiones nuevas para integrar al registro principal.

## ADR-004 — Titularidad y marca

**Estado:** Declarada; verificación jurídica pendiente.

José Martín Álvarez desarrolla GeoStratix por iniciativa propia y pretende comercializarla como persona física.

Axomai es una marca comercial en desarrollo y todavía no está constituida como sociedad.

Pendiente:

- Verificar contratos y derechos de terceros.
- Revisar licencias del código.
- Revisar disponibilidad de marcas.
- Evaluar registro ante IMPI.

## ADR-005 — Comercialización internacional

**Estado:** Pendiente de alcance geográfico.

GeoStratix está dirigida a profesionales de ingeniería civil y laboratorios.

Se contempla su comercialización internacional.

Antes de habilitar nuevos países deberán revisarse:

- Protección de datos.
- Leyes de consumidores.
- Obligaciones fiscales.
- Normas técnicas locales.
- Responsabilidad por software.
- Políticas de plataformas digitales.

## ADR-006 — Clasificación online en v1

**Estado:** Aceptada.

El uso principal será en oficinas y laboratorios.

Se conserva Python/FastAPI como motor de clasificación.

Las clasificaciones nuevas requieren conexión al backend.

Flutter podrá almacenar borradores y documentos descargados localmente.

Se estudiará un modo de clasificación offline para versiones posteriores.

## ADR-007 — Créditos por clasificación

**Estado:** Aceptada.

Se implementa el siguiente modelo:

- 10 créditos gratuitos para cada cuenta nueva.
- 1 crédito por clasificación nueva válida.
- Consultas de resultados anteriores gratuitas.
- Descargas repetidas de PDF gratuitas.

La bonificación inicial se otorga una sola vez por cuenta.

El backend administra los créditos mediante operaciones verificables e idempotentes.

## ADR-008 — Firebase Authentication y Firestore

**Estado:** Aceptada como selección de plataforma.

Se utilizará:

- Google Sign-In.
- Firebase Authentication.
- Cloud Firestore.
- Python/FastAPI para operaciones del servidor.

El plan inicial será Firebase Spark, sujeto a sus cuotas gratuitas.

El alojamiento FastAPI y otros servicios pueden generar costos adicionales.

## ADR-009 — Monetización híbrida

**Estado:** Aceptada.

GeoStratix tendrá dos métodos para obtener créditos:

### Compra

Paquetes de créditos mediante Google Play Billing.

### Publicidad recompensada

Dos anuncios válidos de AdMob otorgarán un crédito.

Los créditos:

- Solo pueden utilizarse en GeoStratix.
- No se transfieren entre usuarios.
- No pueden canjearse por dinero.

En v1 no se implementarán:

- Stripe.
- Suscripciones.
- Renovaciones automáticas.

Las promociones podrán revisarse para futuras ofertas, comunicando previamente las condiciones.

## ADR-010 — Privacidad y audiencia

**Estado:** Controles de diseño propuestos.

GeoStratix estará dirigida a usuarios mayores de 18 años.

Se implementarán:

- Política de privacidad.
- Registro con Google.
- Minimización de datos.
- Solicitud de eliminación de cuentas.
- Fuentes locales.
- Consentimiento publicitario cuando corresponda.

No se implementarán por defecto:

- Grabación de sesiones.
- Grabación de micrófono.
- Captura de pantalla.
- Analítica conductual innecesaria.

## ADR-011 — Verificación de compras y anuncios

**Estado:** Requisito técnico aceptado.

FastAPI será la autoridad sobre los créditos.

Las compras Google Play deberán verificarse desde el backend.

Las recompensas AdMob deberán validarse mediante Server-Side Verification.

Se utilizarán identificadores únicos para prevenir:

- Recompensas duplicadas.
- Compras acreditadas varias veces.
- Clasificaciones cobradas más de una vez.
- Manipulación del saldo desde Flutter.

Las modificaciones de créditos se realizarán mediante transacciones seguras.

## ADR-012 — Trazabilidad normativa y reportes

**Estado:** Propuesta técnica.

Cada clasificación pagada deberá conservar:

- Identificador.
- Usuario propietario.
- Datos de entrada.
- Fecha.
- Versión del motor.
- Símbolo SUCS.
- Descripción.
- Advertencias.
- Derecho de consulta y descarga posterior.

Los documentos generados no se presentarán como dictámenes profesionales ni como certificaciones ASTM.

Los casos no soportados deberán comunicarse expresamente.

## Próximas actividades

1. Integrar documentación legal.
2. Actualizar arquitectura.
3. Configurar Firebase.
4. Implementar Google Sign-In.
5. Crear API de clasificación.
6. Implementar créditos de bienvenida.
7. Implementar transacciones.
8. Incorporar compras y anuncios.
9. Crear reportes PDF.
10. Ejecutar validación técnica, de seguridad y legal antes del lanzamiento.
