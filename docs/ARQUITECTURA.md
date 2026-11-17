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