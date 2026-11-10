# Estado de desarrollo

- [x] Arquitectura v1 seleccionada: Flutter + Python FastAPI.
- [x] Scaffold UI de bienvenida.
- [x] Endpoint `/health` y prueba básica (código preparado; ejecución pendiente de dependencias).
- [ ] Proyecto generado con Flutter SDK local y `flutter run` validado.
- [ ] Contrato de muestra.
- [ ] Validación de muestra.
- [ ] Motor SUCS y tests completos.
- [ ] Pantalla captura.
- [ ] Integración HTTP y manejo de errores.
- [ ] Historial de muestras (decidir necesidad antes de añadir).

Última entrega: inicial, sin clasificación.



## Etapa 1 — Modelo de datos y validaciones de muestras de suelo

**Rama de desarrollo:** `feature/modelo-muestras`  
**Componente:** Backend Python  
**Estado:** Implementado y probado

### 1. Objetivo

Desarrollar la estructura de datos necesaria para representar una muestra de suelo y validar los resultados de laboratorio antes de utilizarlos en el motor de clasificación SUCS.

Se implementó una clase `MuestraSuelo` utilizando programación orientada a objetos y `dataclass`.

### 2. Archivos implementados

**Modelo de datos:**
`backend/app/domain/muestra_suelo.py`

**Pruebas unitarias:**
`backend/tests/test_muestra_suelo.py`

### 3. Funcionalidades implementadas

- Registro de identificador de muestra.
- Registro de límite líquido (LL).
- Registro de límite plástico (LP).
- Registro de porcentajes pasantes de las mallas N.º 4, 40 y 200.
- Registro de diámetros granulométricos D10, D30 y D60.
- Validación de porcentajes dentro del intervalo 0–100 %.
- Validación de coherencia granulométrica: P4 ≥ P40 ≥ P200.
- Validación de límites de Atterberg: LP ≤ LL.
- Validación de diámetros: 0 < D10 ≤ D30 ≤ D60.
- Rechazo de valores no numéricos, infinitos o NaN.
- Posibilidad de registrar muestras con información incompleta.
- Uso de `frozen=True` para evitar modificaciones accidentales de los atributos después de crear una muestra.

### 4. Cálculos implementados

**Índice de plasticidad:**

IP = LL − LP

**Línea A:**

IP_A = 0.73 × (LL − 20)

**Línea U:**

IP_U = 0.90 × (LL − 8)

**Coeficiente de uniformidad:**

Cu = D60 / D10

**Coeficiente de curvatura:**

Cc = D30² / (D10 × D60)

Los resultados calculados se obtienen mediante propiedades (`@property`) de la clase `MuestraSuelo`.

### 5. Pruebas realizadas

Se utiliza `pytest` para verificar los cálculos y las validaciones.

**Resultado confirmado:**

- 10 pruebas ejecutadas.
- 10 pruebas aprobadas.
- 0 pruebas fallidas.
- 1 advertencia de dependencia relacionada con Starlette y `httpx`.
- Tiempo de ejecución registrado: 0.66 segundos.

La advertencia no impidió el funcionamiento del código y queda pendiente para revisión futura.

### 6. Decisiones técnicas

- Separar los datos y cálculos de las funciones de clasificación.
- No aceptar valores físicamente inconsistentes.
- Permitir valores opcionales cuando todavía no existan resultados de laboratorio.
- Utilizar excepciones `ValueError` para comunicar errores de entrada.
- Mantener pruebas automáticas antes de integrar el código con Flutter.
- Desarrollar módulos independientes para facilitar su mantenimiento.

---

## Etapa 2 — Clasificador SUCS para suelos finos inorgánicos

**Rama de desarrollo:** `feature/modelo-muestras`  
**Componente:** Backend Python  
**Estado:** Código proporcionado para implementación; pruebas pendientes de confirmación

### 1. Objetivo

Implementar la primera etapa del motor de clasificación de suelos conforme a la lógica de la carta de plasticidad utilizada en el Sistema Unificado de Clasificación de Suelos (SUCS), tomando como referencia ASTM D2487.

Esta etapa se limita a suelos finos inorgánicos. No constituye todavía una implementación completa de la norma.

### 2. Archivos de esta etapa

**Clasificador:**
`backend/app/domain/clasificador_sucs.py`

**Pruebas:**
`backend/tests/test_clasificador_sucs.py`

### 3. Clasificaciones contempladas

| Símbolo | Descripción |
|---|---|
| CL | Arcilla inorgánica de baja plasticidad |
| CH | Arcilla inorgánica de alta plasticidad |
| ML | Limo inorgánico de baja plasticidad |
| MH | Limo inorgánico de alta plasticidad |
| CL-ML | Arcilla limosa inorgánica de baja plasticidad |

### 4. Requisitos para clasificar

El módulo requiere:

- Porcentaje pasante de malla N.º 200 igual o superior al 50 %.
- Límite líquido disponible.
- Límite plástico disponible.
- Confirmación de que el material es inorgánico.

Si falta información indispensable, el clasificador debe rechazar la operación mediante `ValueError`.

### 5. Lógica de clasificación

Se calcula el índice de plasticidad y se compara con la línea A.

Para LL ≥ 50:

- CH: punto sobre o en la línea A.
- MH: punto bajo la línea A.

Para LL < 50:

- CL-ML: índice de plasticidad entre 4 y 7, con el punto sobre o en la línea A.
- CL: índice de plasticidad mayor que 7, con el punto sobre o en la línea A.
- ML: restantes casos de baja plasticidad.

Estas condiciones representan el alcance inicial del algoritmo. Se deberá revisar el tratamiento detallado de fronteras, puntos especiales y criterios complementarios contra la edición normativa aplicable.

### 6. Advertencia de línea U

El programa identifica cuando el punto de plasticidad queda por encima de la línea U.

En ese caso añade una advertencia para revisar los resultados de laboratorio, sin modificar automáticamente la clasificación.

### 7. Estructura del resultado

Se definió la clase `ResultadoSUCS`, que contiene:

- `simbolo`: clasificación obtenida.
- `descripcion`: nombre descriptivo del suelo.
- `indice_plasticidad`: IP calculado.
- `linea_a`: valor correspondiente a la línea A.
- `advertencias`: mensajes adicionales sobre el resultado.

### 8. Pruebas previstas

Se prepararon diez pruebas adicionales para comprobar:

1. Clasificación CH.
2. Clasificación CL.
3. Clasificación ML.
4. Clasificación MH.
5. Clasificación CL-ML.
6. Frontera de límite líquido LL = 50.
7. Rechazo de un suelo grueso.
8. Confirmación obligatoria de material inorgánico.
9. Rechazo de muestras sin límites de Atterberg.
10. Advertencia cuando el punto supera la línea U.

**Resultado esperado:** 20 pruebas aprobadas en total, contando las diez ya verificadas en la primera etapa.

**Importante:** Este resultado todavía no está confirmado. Se debe ejecutar nuevamente `python -m pytest -v` antes de marcar la etapa como probada.

---

## Estado general del proyecto GeoStratix v1

### Componentes disponibles

| Componente | Estado |
|---|---|
| Proyecto Flutter en Android Studio | Funcional en emulador |
| Estructura del backend FastAPI | Creada |
| Endpoint básico de salud | Probado |
| Repositorio Git y rama de desarrollo | Configurados |
| Modelo `MuestraSuelo` | Implementado y probado |
| Validaciones de laboratorio | Implementadas y probadas |
| Cálculos IP, línea A, línea U, Cu y Cc | Implementados y probados |
| Clasificación de suelos finos inorgánicos | Pendiente de verificar mediante pruebas |
| Clasificación de suelos gruesos | Pendiente |
| Clasificación de suelos orgánicos | Pendiente |
| Conexión Flutter–FastAPI | Pendiente |
| Reportes técnicos en PDF | Pendiente |
| Interfaz definitiva de clasificación | Pendiente |

### Consideraciones técnicas

El backend se desarrolla en Python 3.12 y utiliza FastAPI y pytest.

La aplicación móvil se desarrolla en Flutter 3.47.5 con Dart 3.13.4.

Android Studio presenta algunas advertencias visuales sobre importaciones Python debido a la configuración o reconocimiento de su intérprete. Sin embargo, las pruebas ejecutadas en terminal confirmaron el funcionamiento de los módulos de la primera etapa.

Las advertencias del editor no deben ignorarse indefinidamente; se revisarán conforme avance el desarrollo.

### Próximas actividades

1. Ejecutar las pruebas del clasificador SUCS de suelos finos.
2. Corregir cualquier fallo detectado.
3. Registrar el commit de la segunda etapa.
4. Ampliar el motor a suelos gruesos.
5. Implementar los símbolos dobles y casos especiales.
6. Validar las reglas contra los criterios normativos correspondientes.
7. Crear un endpoint FastAPI para recibir muestras y devolver resultados.
8. Conectar el formulario Flutter con el backend.
9. Diseñar la carta de plasticidad y el sistema de reportes PDF.

### Criterio de calidad

Una funcionalidad se considerará terminada cuando:

- Su código esté implementado.
- Sus datos se validen correctamente.
- Existan pruebas unitarias relevantes.
- Las pruebas se ejecuten satisfactoriamente.
- La documentación esté actualizada.
- Los cambios se registren mediante Git.

**Restricción normativa:** GeoStratix se encuentra en desarrollo. Los resultados actuales son preliminares y no deben presentarse como certificaciones de cumplimiento integral con ASTM D2487.


## Etapa 3 — Clasificación SUCS de suelos gruesos

**Rama:** `feature/clasificacion-suelos-gruesos`  
**Estado:** Implementado y probado  
**Fecha:** 9 de noviembre de 2026

### Objetivo

Implementar la clasificación preliminar de gravas y arenas mediante los criterios del Sistema Unificado de Clasificación de Suelos (SUCS).

### Archivos implementados

- `backend/app/domain/clasificador_suelos_gruesos.py`
- `backend/tests/test_clasificador_suelos_gruesos.py`

### Funcionalidades desarrolladas

- Identificación de gravas y arenas mediante los porcentajes pasantes de las mallas N.º 4 y N.º 200.
- Clasificación de suelos gruesos con menos de 5 % de finos.
- Clasificación de suelos con 5 % a 12 % de finos mediante símbolos dobles.
- Clasificación de suelos con más de 12 % de finos.
- Cálculo y utilización de Cu y Cc.
- Evaluación de la plasticidad de los finos.
- Clasificación mediante símbolos GW, GP, GM, GC, SW, SP, SM y SC.
- Manejo inicial de símbolos dobles y casos fronterizos.
- Advertencias cuando los resultados superan la línea U.
- Corrección de errores de precisión decimal mediante `math.isclose()`.

### Pruebas automatizadas

- 20 pruebas de etapas anteriores.
- 18 pruebas nuevas de suelos gruesos.
- **38 pruebas aprobadas en total**, según la ejecución confirmada por el desarrollador.

### Consideraciones técnicas

El clasificador está separado del modelo de datos `MuestraSuelo`.

Se emplean funciones auxiliares para determinar el tipo de suelo, su graduación y la naturaleza de sus finos.

Las pruebas comprueban los casos implementados, pero no demuestran todavía el cumplimiento integral de ASTM D2487.

### Pendiente

- Validar exhaustivamente casos fronterizos y criterios normativos.
- Integrar el clasificador de suelos finos y gruesos.
- Implementar clasificación de suelos orgánicos y turbas.
- Crear el endpoint de clasificación en FastAPI.
- Conectar el backend con Flutter.
- Incorporar carta de plasticidad y reportes PDF.

### Próxima etapa

Desarrollar un servicio unificado que seleccione automáticamente el clasificador correspondiente a partir de los datos de laboratorio.



