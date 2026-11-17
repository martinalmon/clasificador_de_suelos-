# Contexto técnico para colaboradores e IA

## Proyecto

Clasificador de suelos SUCS con Flutter para Android y backend
Python/FastAPI. Las reglas geotécnicas se encuentran en
backend/app/domain/.

## Punto de partida

El motor clasifica suelos finos inorgánicos y suelos gruesos.
La API exige autenticación para POST /classify.
Se incorporó Firestore local y POST /account/initialize.

La inicialización concede 10 créditos a una cuenta nueva y conserva
el saldo existente mediante una transacción.

El desarrollador reportó 58 pruebas aprobadas con Firestore local
activo. Tres verifican creación de cuenta, conservación del saldo
e inicializaciones concurrentes. Es necesario volver a ejecutar
las pruebas después de cambios relevantes.

## Próxima implementación

Guardar cada clasificación y descontar un crédito atómicamente.
Evitar cargos duplicados en reintentos y solicitudes concurrentes.
Vincular las operaciones al UID verificado.

Todas las descargas del PDF, incluida la primera, son gratuitas.
El PDF y el descuento todavía están pendientes.

## Cómo retomar

1. Revisar git status, rama actual y cambios locales.
2. Leer ARQUITECTURA.md, ESTADO.md, DECISIONES.md y
   CRITERIOS_NORMATIVOS.md dentro de docs/.
3. Contrastar la documentación con el código y las pruebas actuales.
4. Distinguir implementación local de configuración de producción.
5. Ejecutar pruebas antes de proponer integración de cambios.

El trabajo de cuentas se realizó en feature/creditos-clasificaciones.
Su commit, push y merge deben verificarse en Git.

## Criterios

Mantener un monorepo sencillo y reutilizar el motor existente.
Usar datos ficticios en pruebas.
No incluir secretos en el código.
Solicitar autorización antes de fusionar ramas.
No afirmar conformidad completa con ASTM sin validación oficial.
Los mapas y la predicción geológica quedan fuera de v1.