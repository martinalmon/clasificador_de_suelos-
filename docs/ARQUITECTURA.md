
# GeoStratix — Arquitectura v1

**Última actualización:** 12 de noviembre de 2026  
**Estado:** Arquitectura objetivo aprobada para desarrollo.

## 1. Objetivo

GeoStratix es una aplicación Android dirigida principalmente a ingenieros civiles, geotecnistas y laboratorios.

El sistema permitirá clasificar muestras mediante el Sistema Unificado de Clasificación de Suelos (SUCS).

También contará con un modelo comercial basado en créditos digitales.

### Reglas comerciales

- 10 créditos gratuitos para usuarios nuevos.
- 1 crédito por clasificación nueva.
- 2 anuncios recompensados por 1 crédito.
- Compra de créditos mediante Google Play Billing.
- Consultas de clasificaciones anteriores gratuitas.
- Descargas repetidas de PDF gratuitas.
- Sin suscripciones automáticas durante v1.

## 2. Tecnologías

| Componente | Tecnología |
|---|---|
| Interfaz Android | Flutter / Dart |
| Motor SUCS | Python |
| API | FastAPI |
| Autenticación | Firebase Authentication |
| Inicio de sesión | Google Sign-In |
| Base de datos | Cloud Firestore |
| Compra de créditos | Google Play Billing |
| Publicidad recompensada | Google AdMob |
| Consentimiento publicitario | Google UMP, según mercado |
| Reportes | PDF |
| Control de versiones | Git / GitHub |

## 3. Arquitectura general

```text
GeoStratix Android
│
├── Flutter
│   ├── Inicio de sesión
│   ├── Formulario de muestras
│   ├── Borradores locales
│   ├── Billetera de créditos
│   ├── Compra de créditos
│   ├── Anuncios recompensados
│   ├── Historial de clasificaciones
│   └── Reportes PDF
│
├── Firebase Authentication
│   └── Google Sign-In
│
├── Google Play Billing
│   └── Compra de paquetes
│
├── AdMob
│   └── Rewarded Ads
│
└── HTTPS
    │
    ▼
FastAPI — Python
│
├── Verificación de Firebase ID Token
├── Validación de muestras
├── Clasificador SUCS unificado
├── Control de créditos
├── Verificación de compras
├── Verificación AdMob SSV
├── Control de acceso
└── Registro de transacciones
    │
    ▼
Cloud Firestore
│
├── Usuarios
├── Billeteras
├── Movimientos
├── Compras
├── Recompensas
├── Clasificaciones
└── Idempotencia
```

## 4. Principios arquitectónicos

### 4.1 Separación de responsabilidades

Flutter será responsable de:

- Presentación.
- Captura de información.
- Navegación.
- Formularios.
- Visualización de resultados.
- Interacción con sistemas de pago y anuncios.

Python será responsable de:

- Validaciones geotécnicas.
- Cálculos.
- Clasificación SUCS.
- Generación del resultado técnico.

FastAPI será responsable de:

- Exponer servicios HTTP.
- Verificar usuarios.
- Autorizar clasificaciones.
- Administrar operaciones de créditos.
- Procesar verificaciones de compras.
- Recibir verificaciones de anuncios.

Firestore será responsable de persistir la información necesaria.

### 4.2 Motor SUCS único

Las fórmulas geotécnicas estarán exclusivamente en:

backend/app/domain/

No duplicar algoritmos SUCS en Flutter.

### 4.3 Seguridad

El cliente no tendrá autorización para modificar directamente créditos, compras ni recompensas.

Todas las operaciones que cambien créditos serán controladas mediante el backend.

## 5. Estructura de Firestore

Estructura conceptual prevista:

```text
accounts/
    {uid}

wallets/
    {uid}

ledger/
    {operationId}

purchases/
    {purchaseKey}

adRewards/
    {transactionId}

classifications/
    {classificationId}

idempotency/
    {requestKey}
```

### accounts

Información mínima de la cuenta:

- UID.
- Referencia de autenticación.
- Fecha de registro.
- Estado de cuenta.
- Bonificación inicial asignada.

### wallets

- UID.
- Saldo disponible.
- Progreso de anuncios, si corresponde.

### ledger

Historial de movimientos:

- ID de operación.
- Usuario.
- Tipo.
- Cantidad de créditos.
- Fecha.
- Referencia externa única.

Tipos de movimientos:

- Bonificación inicial.
- Compra.
- Recompensa de publicidad.
- Clasificación.
- Reembolso.
- Ajuste autorizado.

### purchases

- Identificador único de compra.
- Usuario.
- Producto.
- Estado de verificación.
- Créditos otorgados.
- Estado de consumo o reembolso.

### adRewards

- Identificador SSV.
- Usuario.
- Anuncio validado.
- Fecha.
- Progreso de recompensa.

### classifications

- Identificador de clasificación.
- Usuario propietario.
- Datos utilizados.
- Símbolo SUCS.
- Descripción.
- Advertencias.
- Fecha.
- Versión del motor.

### idempotency

- Usuario.
- Identificador de solicitud.
- Operación asociada.
- Estado y resultado.

## 6. Registro de usuarios

Se utilizará Google Sign-In mediante Firebase Authentication.

El backend verificará los tokens de autenticación.

Durante el registro se deberá:

1. Validar la identidad.
2. Aplicar restricciones de edad.
3. Crear la cuenta.
4. Crear la billetera.
5. Asignar 10 créditos iniciales.
6. Registrar la bonificación en el historial.

La bonificación no deberá repetirse durante reinstalaciones o nuevos inicios de sesión.

## 7. Sistema de clasificaciones

Flujo:

1. El usuario captura una muestra.
2. Flutter envía los datos y un ID de operación.
3. FastAPI verifica identidad y solicitud.
4. Se validan los datos.
5. Se ejecuta el motor SUCS.
6. Se verifica el saldo.
7. Una transacción atómica registra el resultado y descuenta un crédito.
8. Se devuelve el resultado.

Si una solicitud se repite con el mismo identificador de operación, deberá recuperarse el resultado anterior sin descontar otra vez.

## 8. Créditos por anuncios

Regla inicial:

**2 anuncios recompensados válidos = 1 crédito.**

Flujo:

1. Usuario selecciona Ganar créditos.
2. Flutter explica la recompensa.
3. Usuario acepta voluntariamente ver un anuncio.
4. AdMob muestra el anuncio.
5. Google envía verificación SSV al backend.
6. El backend verifica firma y transacción.
7. Firestore registra progreso.
8. Al completar dos anuncios válidos se acredita un crédito.

El cliente no puede acreditar recompensas directamente.

No se otorgarán recompensas por clics.

## 9. Compras con Google Play

Las compras serán productos digitales consumibles.

Flujo:

1. Usuario selecciona un paquete.
2. Google Play procesa el pago.
3. Flutter informa del token de compra.
4. FastAPI comprueba su validez.
5. El backend registra la compra.
6. Se acreditan créditos mediante transacción segura.
7. Se procesa correctamente el consumo o reconocimiento.

El sistema deberá prevenir créditos duplicados y atender reembolsos.

## 10. Reportes PDF

Cada clasificación pagada permitirá:

- Consultar resultado.
- Descargar PDF.
- Descargar nuevamente sin pagar.
- Recuperar información desde otro dispositivo autenticado.

El reporte incluirá:

- Datos de laboratorio.
- Clasificación SUCS.
- Símbolo.
- Descripción.
- Advertencias.
- Fecha.
- Versión del algoritmo.
- Limitaciones técnicas.

No se presentará como certificación ASTM.

## 11. Funcionamiento sin conexión

En v1 se permitirá:

- Capturar borradores.
- Guardar muestras localmente.
- Consultar resultados descargados.
- Abrir PDF locales.

Requerirán conexión:

- Inicio de sesión inicial.
- Compra de créditos.
- Visualización de anuncios.
- Clasificaciones nuevas.
- Sincronización de saldos.

El funcionamiento completamente offline se evaluará para versiones futuras.

## 12. Privacidad

Medidas previstas:

- HTTPS.
- Tokens verificados.
- Reglas de acceso en Firestore.
- Minimización de datos.
- Fuentes locales.
- Sin grabación de sesiones.
- Sin micrófono.
- Sin analítica conductual adicional por defecto.
- Control de consentimiento publicitario cuando corresponda.
- Eliminación de cuentas y datos según requisitos legales.

## 13. Estructura de código prevista

```text
mobile/
└── lib/
    └── features/
        ├── auth/
        ├── classification/
        ├── wallet/
        ├── rewards/
        └── reports/

backend/
├── app/
│   ├── api/
│   ├── domain/
│   └── services/
└── tests/

docs/
├── ARQUITECTURA.md
├── CONTEXTO_IA.md
├── CRITERIOS_NORMATIVOS.md
├── DECISIONES.md
├── ESTADO.md
├── GIT_FLUJO.md
└── LEGAL.md
```

## 14. Restricciones económicas

Firebase Spark ofrece cuotas gratuitas, pero no garantiza que toda la infraestructura sea gratuita.

Se deberá evaluar:

- Costo del hosting FastAPI.
- Cuotas de Firestore.
- Límite de operaciones.
- Almacenamiento.
- Tráfico de red.
- Verificación SSV.
- Costos de mantenimiento.

El sistema deberá permitir ampliar su infraestructura conforme aumenten los usuarios y los ingresos.

## 15. Pendientes técnicos

- [ ] Crear proyecto Firebase.
- [ ] Configurar Google Sign-In.
- [ ] Implementar autenticación.
- [ ] Crear colecciones Firestore.
- [ ] Implementar reglas de seguridad.
- [ ] Implementar bonificación inicial.
- [ ] Implementar billetera.
- [ ] Crear API de clasificación.
- [ ] Integrar Google Play Billing.
- [ ] Integrar anuncios AdMob.
- [ ] Implementar verificación SSV.
- [ ] Generar reportes PDF.
- [ ] Implementar eliminación de cuenta.
- [ ] Ejecutar pruebas de seguridad.
- [ ] Verificar cuotas y costos.
- [ ] Preparar publicación en Google Play.

## 16. Referencias

Firebase:
https://firebase.google.com/pricing

Firestore:
https://firebase.google.com/docs/firestore/quotas

Google Play Billing:
https://developer.android.com/google/play/billing

AdMob:
https://developers.google.com/admob/flutter/rewarded

Server-Side Verification:
https://developers.google.com/admob/flutter/ssv

Google Play User Data:
https://support.google.com/googleplay/android-developer/answer/10144311
