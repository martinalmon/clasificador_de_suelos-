<!-- GEOSTRATIX-20261116-84 -->
# Arquitectura de GeoStratix

## Arquitectura v1

Flutter / Android
    |
    | HTTPS en produccion
    v
FastAPI / Python
    |
    +-- Autenticacion Firebase
    +-- Motor SUCS
    +-- Transacciones Firestore
    +-- Historial de resultados

La app Flutter sera cliente del backend.
Las reglas geotecnicas y el cobro de creditos
permanecen en el servidor.

## Estructura

- mobile/: aplicacion Flutter.
- backend/app/api/: endpoints HTTP.
- backend/app/domain/: validaciones y motor SUCS.
- backend/app/clasificaciones_guardadas.py:
  persistencia transaccional y descuento.
- backend/app/base_datos.py:
  conexion local a Firestore.
- backend/tests/: pruebas automatizadas.
- docs/: documentacion publica.

## Modelo de datos

Coleccion usuarios:

usuarios/{uid}

Campos principales:
- creditos
- bienvenida_otorgada
- creado_en

Subcoleccion:

usuarios/{uid}/clasificaciones/{id}

Campos principales:
- entrada
- resultado
- creditos_consumidos
- creado_en

El identificador de clasificacion se obtiene
mediante SHA-256 de la clave de operacion.

La ruta incorpora el UID autenticado.

## Consumo de creditos

POST /classify:

1. Comprueba la identidad del usuario.
2. Valida la muestra.
3. Calcula la clasificacion SUCS.
4. Consulta el registro de la operacion.
5. Si ya existe con la misma entrada,
   devuelve el resultado sin otro cobro.
6. Si es nueva, comprueba el saldo.
7. Crea el resultado y descuenta un credito
   dentro de una transaccion Firestore.

Una clave reutilizada con otros datos
produce HTTP 409.

Sin creditos disponibles se devuelve HTTP 403.

## Historial

GET /classifications:
- Requiere autenticacion.
- Devuelve solamente registros propios.
- No descuenta creditos.
- Permite paginacion mediante cursor.
- Ordena por fecha descendente.
- Limite entre 1 y 50 registros.

GET /classifications/{clasificacion_id}:
- Requiere autenticacion.
- Consulta solamente datos del UID verificado.
- No consume creditos.
- Devuelve HTTP 404 si el registro no existe.

## Seguridad

No confiar en un UID proporcionado por el cliente.

El backend utiliza el UID obtenido del token
Firebase verificado.

Las reglas Firestore actuales restringen
el acceso directo de los clientes.
Los SDK de servidor deben aplicar autorizacion
en cada operacion.

La configuracion actual esta preparada
para emuladores, NO para produccion.

No publicar credenciales de servidor,
tokens, claves privadas ni cuentas reales.

La clave de Firebase incluida en un cliente
no debe tratarse como secreto de servidor.
Se requieren reglas y controles adecuados.

## Pruebas

Ultimo resultado reportado:
84 pruebas aprobadas.

Incluyen clasificadores, muestras, cuentas,
creditos, idempotencia, historial, paginacion
y prueba inicial de concurrencia.

Pendiente revisar alta concurrencia,
integridad operacional y escalabilidad.

## Pendientes arquitectonicos

- Conexion Flutter con FastAPI.
- Generacion de PDF.
- Descarga gratuita de PDF.
- Google Play Billing y AdMob.
- Registro de movimientos de creditos.
- Configuracion de produccion.
- Estrategia de despliegue y observabilidad.
- Auditoria de seguridad.
- Politicas de retencion de datos.
- Validacion normativa completa.

---

## Registro documental anterior

> El contenido siguiente es historico. El resumen vigente es el de arriba.

# Arquitectura

## Componentes

- Flutter/Dart en mobile/ para la aplicación Android.
- FastAPI en backend/app/api/ para las rutas HTTP.
- Motor SUCS y validaciones en backend/app/domain/.
- Firebase Authentication para identificar usuarios.
- Firestore para cuentas y, en la siguiente etapa, clasificaciones.

Las fórmulas permanecen en el backend. La integración Flutter-API
y el despliegue de producción siguen pendientes.

## Implementación local actual

- GET /health permite comprobar el servicio.
- GET /auth/me devuelve el UID del token verificado.
- POST /classify exige autenticación y devuelve el resultado SUCS.
- POST /account/initialize crea usuarios/{uid} con 10 créditos
  mediante una transacción y conserva el saldo si la cuenta existe.
- El documento contiene creditos, bienvenida_otorgada y creado_en.
- app/base_datos.py proporciona la conexión local a Firestore.

Se utiliza el proyecto demo-sucs-local y las siguientes direcciones.

| Servicio | Dirección |
|---|---|
| Authentication | 127.0.0.1:9099 |
| Firestore | 127.0.0.1:8080 |
| Panel de emuladores | 127.0.0.1:4000 |
| FastAPI | 127.0.0.1:8000 |

## Seguridad

La identidad procede del token verificado. Los clientes no eligen
el UID de la cuenta que se inicializa.

firestore.rules bloquea lecturas y escrituras directas de clientes.
Los SDK de servidor omiten esas reglas. Cada operación del backend
debe comprobar la identidad y la propiedad de los datos.

La autenticación actual admite tokens del emulador y está preparada
para desarrollo local. La configuración de producción queda pendiente.
Las credenciales privadas y los datos personales deben quedar fuera
del repositorio, los ejemplos y los registros de depuración.

## Reglas acordadas y trabajo pendiente

Una clasificación nueva válida consume un crédito.
Todas las descargas de su PDF son gratuitas, incluida la primera.
La reconsulta de un resultado guardado es gratuita.

Queda por implementar el guardado del resultado y el descuento en una
misma transacción, junto con una clave de idempotencia por usuario
y solicitud. Reintentar una operación completada debe devolver su
resultado sin un segundo cargo. Reutilizar la clave con otros datos
debe rechazarse.

También quedan pendientes el historial privado, los reportes PDF,
compras, anuncios, integración móvil y controles de producción.

## Alcance normativo

La validación integral frente al texto oficial de ASTM D2487 está
pendiente. Las pruebas aprobadas respaldan los casos implementados.