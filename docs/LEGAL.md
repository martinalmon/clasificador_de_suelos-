
# GeoStratix — Matriz legal, privacidad y publicación

**Fecha de revisión:** 12 de noviembre de 2026  
**Estado:** Borrador interno de cumplimiento.

> IMPORTANTE: Este documento no es una política de privacidad pública ni un dictamen jurídico. Debe validarse contra las leyes vigentes y la implementación real antes del lanzamiento.

## 1. Identidad, alcance y modelo de negocio

### Desarrollador y titular

- Desarrollador y operador comercial previsto: José Martín Álvarez.
- Tipo de actividad: persona física.
- Cuenta de Google Play Console: personal, con intención de comercializar aplicaciones.
- Marca en desarrollo: Axomai.
- Producto: GeoStratix.
- Axomai todavía no está constituida como sociedad mercantil.
- Verificar los derechos de propiedad intelectual, contratos y licencias antes de publicar.

### Descripción de GeoStratix

GeoStratix es una aplicación Android desarrollada con Flutter y Python, dirigida a ingenieros civiles, geotecnistas y laboratorios.

Su finalidad es clasificar muestras de suelo mediante el Sistema Unificado de Clasificación de Suelos (SUCS), utilizando resultados de laboratorio introducidos por el usuario.

El motor de clasificación está desarrollado mediante reglas deterministas en Python.

### Público objetivo

La aplicación está dirigida exclusivamente a personas mayores de 18 años.

No está destinada a menores de edad.

### Monetización

El modelo comercial inicial será:

1. Cada usuario nuevo recibe 10 créditos gratuitos.
2. Cada clasificación nueva cuesta 1 crédito.
3. Consultar resultados anteriores es gratuito.
4. Descargar nuevamente un PDF previamente pagado es gratuito.
5. Los usuarios pueden comprar paquetes de créditos mediante Google Play Billing.
6. Los usuarios pueden ganar 1 crédito por completar 2 anuncios recompensados de Google AdMob.
7. No existirán suscripciones ni renovaciones automáticas en la primera versión.

Los créditos:

- Solo pueden utilizarse dentro de GeoStratix.
- No son transferibles entre usuarios.
- No pueden cambiarse por dinero.
- No representan una moneda de curso legal.

Las condiciones de uso, reembolsos y posibles vencimientos deberán definirse antes del lanzamiento.

### Distribución internacional

GeoStratix tiene vocación internacional.

Los países donde se publicará todavía están pendientes de decisión.

La utilización internacional de ASTM D2487 no implica que esta norma sustituya automáticamente las regulaciones nacionales.

---

## 2. Propiedad intelectual y normas técnicas

### 2.1 Titularidad del software

Se declara a José Martín Álvarez como desarrollador y presunto titular original de GeoStratix.

Antes de comercializar se deberán revisar:

- Contratos o acuerdos con colaboradores.
- Aportaciones de código de terceros.
- Licencias de bibliotecas utilizadas.
- Derechos sobre imágenes, tipografías y recursos.
- Uso de herramientas de IA durante el desarrollo.
- Posibles derechos relacionados con trabajos por encargo.

### 2.2 Normativa ASTM

El motor SUCS utiliza como referencia ASTM D2487.

Antes de su comercialización deben verificarse:

- Edición normativa utilizada.
- Licencias aplicables al uso comercial.
- Permisos para reproducir tablas, figuras o textos.
- Restricciones de marcas y logotipos ASTM.
- Validación de reglas y casos especiales.

No debe afirmarse que GeoStratix está certificada, autorizada o avalada por ASTM sin contar con pruebas y permisos correspondientes.

### 2.3 Responsabilidad profesional

GeoStratix es una herramienta de apoyo a la clasificación de suelos.

No constituye:

- Dictamen geotécnico.
- Diseño de cimentaciones.
- Certificación de laboratorio.
- Autorización estructural.
- Sustituto del criterio profesional de un ingeniero.

Cada resultado deberá incluir:

- Identificador de muestra.
- Datos empleados.
- Símbolo SUCS.
- Descripción.
- Advertencias.
- Fecha.
- Versión del motor de clasificación.

El reporte PDF deberá incluir una advertencia técnica visible.

Los avisos legales no eliminan responsabilidades legales obligatorias.

### Fuentes

- ASTM: https://store.astm.org/d2487-17r25.html
- Permisos ASTM: https://store.astm.org/restricted_copyright-and-permissions
- Ley Federal del Derecho de Autor: https://www.diputados.gob.mx/LeyesBiblio/pdf/LFDA.pdf

---

## 3. Protección de menores y registro

### 3.1 COPPA — Estados Unidos

COPPA protege la privacidad de los menores de 13 años en determinadas actividades digitales.

La aplicación estará dirigida a adultos mayores de 18 años.

Medidas previstas:

- Declarar correctamente la audiencia en Google Play.
- Implementar comprobación proporcional de mayoría de edad.
- No recopilar deliberadamente datos personales de menores.
- No considerar que una simple casilla garantiza el cumplimiento legal.
- Revisar requisitos específicos de los mercados donde se publique.

### 3.2 Registro mediante Google

Se utilizará:

- Google Sign-In.
- Firebase Authentication.
- Verificación de identidad mediante tokens.
- Identificador único para cada cuenta.

GeoStratix no almacenará las contraseñas de Google.

Google Sign-In no verifica automáticamente que una persona sea mayor de edad.

### Fuente

FTC: https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy

---

## 4. Protección de datos personales

Antes del lanzamiento se deberá publicar una política de privacidad accesible desde:

1. Google Play Store.
2. Pantalla de registro.
3. Configuración de GeoStratix.
4. Una dirección web pública.

La política definitiva debe coincidir con los datos que realmente procesen la aplicación, sus SDK y sus proveedores.

### 4.1 Inventario preliminar de datos

| Dato | Finalidad |
|---|---|
| ID de Firebase | Identificar al usuario |
| Correo electrónico | Inicio de sesión y recuperación |
| Nombre visible, si se usa | Identificación en la interfaz |
| Estado de mayoría de edad | Control de acceso |
| Saldo de créditos | Control de la billetera |
| Movimientos de créditos | Auditoría y prevención de fraude |
| Identificadores de compras | Verificar Google Play Billing |
| Identificadores de recompensas | Verificar anuncios de AdMob |
| Datos de clasificaciones pagadas | Recuperar resultados |
| Borradores de laboratorio | Trabajo local |
| Dirección IP y registros técnicos mínimos | Comunicación y seguridad |
| Identificadores publicitarios | Funcionamiento de AdMob, según configuración |
| Preferencias publicitarias | Consentimiento y configuración de anuncios |

No se almacenarán:

- Contraseñas de Google.
- Números completos de tarjetas bancarias.
- Códigos de seguridad de tarjetas.

### 4.2 Derechos del usuario

Implementar mecanismos para:

- Consultar información personal.
- Corregir datos cuando proceda.
- Solicitar eliminación de cuenta.
- Solicitar eliminación de información.
- Ejercer derechos ARCO y otros derechos aplicables.
- Obtener información sobre tratamiento de datos.

La eliminación de cuentas deberá solicitarse desde la app y mediante un enlace web externo, conforme a Google Play.

Algunos registros de transacciones podrán requerir conservación por obligaciones legales; deberán definirse sus fundamentos y plazos.

### 4.3 Transferencias internacionales

Firebase, Google Play y AdMob pueden procesar información mediante infraestructura internacional.

Debemos identificar:

- Proveedores utilizados.
- Países o regiones de tratamiento.
- Datos compartidos.
- Finalidades.
- Bases jurídicas.
- Plazos de conservación.

### Fuentes

México:
https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPDPPP.pdf

Unión Europea:
https://eur-lex.europa.eu/eli/reg/2016/679/oj

Google Play:
https://support.google.com/googleplay/android-developer/answer/10144311

---

## 5. Recursos externos, analítica y privacidad

### 5.1 Fuentes e imágenes

Las fuentes tipográficas se incluirán preferentemente dentro del paquete Flutter.

Evitar cargar recursos externos innecesariamente.

Revisar:

- Licencias de fuentes.
- Licencias de imágenes.
- Solicitudes de red.
- SDK de terceros.
- Identificadores transmitidos.
- Datos enviados a proveedores.

Una conexión con un servidor externo puede revelar la IP del dispositivo a ese proveedor.

### 5.2 Analítica

GeoStratix no utilizará inicialmente:

- Grabación de sesiones.
- Captura de pulsaciones.
- Grabación del micrófono.
- Grabación de pantalla.
- Seguimiento publicitario adicional innecesario.

Se permitirá evaluar registros mínimos de errores y estadísticas operativas, previa revisión de privacidad.

### 5.3 Publicidad

Se utilizará Google AdMob con anuncios recompensados.

Los anuncios serán voluntarios.

El usuario deberá conocer la recompensa antes de visualizar el anuncio.

No se incentivarán clics en anuncios.

Durante desarrollo se utilizarán identificadores y anuncios de prueba.

### 5.4 Consentimientos

Cuando corresponda, implementar Google UMP u otra plataforma de gestión de consentimiento adecuada.

Para usuarios europeos deberán revisarse los requisitos RGPD, ePrivacy y las políticas publicitarias de Google.

El rechazo de anuncios no deberá impedir consultar resultados que ya fueron pagados.

### Fuentes

https://developers.google.com/admob/flutter/rewarded

https://developers.google.com/admob/flutter/privacy

https://developers.google.com/admob/flutter/privacy/gdpr

---

## 6. Sistema de créditos

### 6.1 Créditos de bienvenida

Cada cuenta nueva recibirá 10 créditos gratuitos.

Reglas:

- Bonificación una sola vez por cuenta.
- El backend será responsable de acreditar los créditos.
- El usuario no podrá modificar directamente su saldo.
- Se implementarán medidas proporcionadas contra cuentas fraudulentas.

Google Sign-In no impide por sí solo que una persona cree varias cuentas.

### 6.2 Clasificaciones

Cada clasificación nueva válida costará 1 crédito.

No se cobrará nuevamente por:

- Consultar el mismo resultado.
- Abrir el historial.
- Descargar nuevamente el mismo PDF.

Una clasificación nueva solicitada tras modificar los datos podrá generar un cargo adicional informado al usuario.

Los errores internos y las solicitudes duplicadas no deberán provocar cargos repetidos.

### 6.3 Anuncios recompensados

La equivalencia inicial será:

**2 anuncios recompensados válidos = 1 crédito.**

El servidor deberá:

1. Recibir la verificación de AdMob.
2. Validar la firma criptográfica.
3. Identificar al usuario.
4. Evitar transacciones duplicadas.
5. Registrar el progreso.
6. Acreditar 1 crédito al completar dos eventos válidos.

Se utilizará Server-Side Verification (SSV).

La disponibilidad de anuncios no está garantizada en todos los momentos ni países.

El límite diario de recompensas queda pendiente de decisión.

### 6.4 Compras de créditos

Se utilizará Google Play Billing.

Las compras serán consumibles y no recurrentes.

El backend deberá:

- Verificar compras.
- Registrar transacciones.
- Evitar acreditaciones duplicadas.
- Gestionar compras pendientes.
- Procesar correctamente las compras.
- Atender reembolsos y revocaciones.

No se implementará Stripe ni suscripciones en v1.

### Fuentes

https://developer.android.com/google/play/billing

https://support.google.com/googleplay/android-developer/answer/9858738

https://developers.google.com/admob/flutter/ssv

---

## 7. Firebase y seguridad

GeoStratix utilizará inicialmente:

- Firebase Authentication.
- Cloud Firestore.
- Google Sign-In.

Se utilizará el plan gratuito Spark mientras sus cuotas y servicios disponibles resulten suficientes.

Esto no garantiza que el alojamiento FastAPI sea gratuito.

### Medidas obligatorias de diseño

- Comunicación mediante HTTPS.
- Verificación de tokens.
- Reglas de seguridad Firestore.
- Validación de entrada.
- Control de acceso por usuario.
- Transacciones atómicas.
- Protección contra solicitudes duplicadas.
- Almacenamiento mínimo de información.
- Gestión segura de credenciales del servidor.
- Registro de operaciones económicas virtuales.

El cliente Flutter nunca deberá poder incrementar directamente sus créditos.

---

## 8. Obligaciones comerciales y fiscales

### Cuenta personal

La cuenta personal de Google Play puede utilizarse para monetización, con las obligaciones correspondientes.

Se debe revisar qué información del comerciante será pública:

- Nombre legal.
- Dirección.
- Teléfono.
- Correo de contacto.

No utilizar datos falsos para ocultar información personal.

### Fiscalidad

Revisar con un contador:

- RFC.
- Régimen de persona física.
- ISR.
- IVA.
- Comprobantes fiscales.
- Ingresos publicitarios.
- Ingresos por créditos.
- Comisiones de Google.
- Retenciones y obligaciones internacionales.

### Marca

Revisar disponibilidad y posible registro de:

- Axomai.
- GeoStratix.

Autoridad mexicana: IMPI.

https://www.gob.mx/impi

---

## 9. Inteligencia artificial

El uso de ChatGPT, Claude u otras herramientas para apoyar el desarrollo no genera automáticamente una obligación universal de declarar que GeoStratix utiliza IA.

El motor SUCS actual es determinista.

No deberá describirse como un motor predictivo de inteligencia artificial.

Si posteriormente se implementan:

- Redes neuronales.
- Modelos predictivos.
- Chatbots.
- Generación automática de contenido mediante IA.

Se revisarán nuevamente los requisitos legales aplicables.

Fuente:
https://eur-lex.europa.eu/eli/reg/2024/1689/oj

---

## 10. Documentos obligatorios o necesarios antes de publicar

- [ ] Política de privacidad pública.
- [ ] Aviso de privacidad mexicano.
- [ ] Términos de Uso.
- [ ] Condiciones de créditos y recompensas.
- [ ] Política de compras, cancelaciones y reembolsos.
- [ ] Mecanismo de eliminación de cuenta.
- [ ] Declaración Data Safety de Google Play.
- [ ] Declaración de audiencia y anuncios.
- [ ] Avisos técnicos para resultados y PDF.
- [ ] Revisión de licencias ASTM.
- [ ] Revisión de marca e identidad comercial.
- [ ] Verificación de obligaciones fiscales.
- [ ] Auditoría de privacidad y seguridad.
- [ ] Revisión de mercados internacionales habilitados.

## 11. Pendientes de implementación

- [ ] Configurar Firebase Authentication.
- [ ] Configurar Cloud Firestore y reglas de seguridad.
- [ ] Implementar 10 créditos iniciales.
- [ ] Implementar billetera de créditos.
- [ ] Implementar Google Play Billing.
- [ ] Implementar AdMob Rewarded Ads.
- [ ] Implementar SSV de AdMob.
- [ ] Implementar descuentos atómicos.
- [ ] Implementar recuperación de resultados.
- [ ] Implementar PDFs con advertencias.
- [ ] Implementar eliminación de cuentas.
- [ ] Auditar SDK y conexiones externas.
- [ ] Definir almacenamiento y retención.
- [ ] Elegir países de lanzamiento.
- [ ] Verificar costos de alojamiento y cuotas gratuitas.

## 12. Referencias adicionales

- Firebase: https://firebase.google.com/pricing
- Firestore: https://firebase.google.com/docs/firestore/quotas
- COPPA: https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy
- Directiva europea de responsabilidad por productos: https://eur-lex.europa.eu/eli/dir/2024/2853/oj
- Google Play: https://support.google.com/googleplay/android-developer/

---

**Nota final:** Esta documentación es una matriz de cumplimiento y planificación, no un certificado legal. La política de privacidad pública deberá redactarse una vez identificados los datos realmente recopilados y los proveedores utilizados.
