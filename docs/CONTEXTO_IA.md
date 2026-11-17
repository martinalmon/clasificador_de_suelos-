<!-- GEOSTRATIX-20261116-84 -->
# Contexto tecnico para colaboradores e IA

## Objetivo

Desarrollar una aplicacion Android para
clasificacion geotecnica SUCS.

## Arquitectura

- Flutter/Dart para Android.
- FastAPI/Python para el backend.
- Firebase Authentication.
- Cloud Firestore.
- Pruebas con pytest.
- Monorepo con mobile/, backend/ y docs/.

## Estado

Ultima ejecucion reportada:
84 pruebas aprobadas.

El backend implementa:
- Clasificacion SUCS.
- Autenticacion local.
- Cuentas con 10 creditos iniciales.
- Descuento transaccional.
- Guardado de clasificaciones.
- Idempotencia.
- Historial privado.
- Consulta gratuita.
- Paginacion cronologica.
- Prueba inicial de concurrencia.

Los endpoints y contratos se describen
en ARQUITECTURA.md.

## Reglas de negocio

- Cuenta nueva: 10 creditos.
- Clasificacion nueva valida: 1 credito.
- Reintento de la misma operacion: gratis.
- Consulta del historial: gratis.
- Descargas de PDF: gratuitas, incluida
  la primera; implementacion pendiente.
- Publicidad recompensada prevista:
  2 anuncios por 1 credito.
- Compras pendientes mediante Play Billing.

## Limitaciones

- Autenticacion de produccion pendiente.
- Flutter aun no integrado con el backend.
- Reportes PDF pendientes.
- Compras y anuncios pendientes.
- Conformidad ASTM integral no verificada.
- Mapas y prediccion geologica fuera de v1.

## Instrucciones para continuar

1. Consultar ESTADO.md y ARQUITECTURA.md.
2. Revisar DECISIONES.md.
3. Revisar CRITERIOS_NORMATIVOS.md.
4. Consultar GIT_FLUJO.md.
5. Comprobar rama y git status.
6. Inspeccionar el codigo actual.
7. Ejecutar pruebas.
8. Evitar cambios que rompan el motor SUCS.
9. No introducir secretos al repositorio.
10. No realizar merges sin autorizacion.

La documentacion describe el ultimo estado
reportado; verificar la implementacion real
antes de introducir nuevos cambios.

---

## Registro documental anterior

> El contenido siguiente es historico. El resumen vigente es el de arriba.

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