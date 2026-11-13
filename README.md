# Clasificador de suelos SUCS

Proyecto de ingeniería geotécnica que clasifica muestras de suelo a partir de resultados de laboratorio. El motor está escrito en Python y utiliza el Sistema Unificado de Clasificación de Suelos (SUCS). La aplicación móvil se desarrolla con Flutter para Android.

## Qué hace el motor

El clasificador recibe el identificador de la muestra y los datos de laboratorio disponibles: porcentajes que pasan por los tamices, límites de Atterberg y diámetros característicos.

A partir del porcentaje que pasa la malla N.º 200, selecciona el procedimiento para suelos finos o gruesos. El resultado incluye el símbolo SUCS, la descripción, el porcentaje de finos, el índice de plasticidad cuando puede calcularse y las advertencias que correspondan.

## Estado del desarrollo

- El motor unificado para suelos finos inorgánicos, gravas y arenas está integrado en `main` y `develop`.
- La rama `feature/api-clasificacion` expone el motor mediante `POST /classify` con FastAPI. En esa rama se ejecutaron 53 pruebas satisfactoriamente y se comprobó el endpoint desde Swagger UI.
- La conexión del formulario Flutter con la API está pendiente. Los suelos orgánicos y las turbas quedan fuera del alcance actual del motor.

## Ejemplo de clasificación

Para una muestra confirmada como inorgánica:

| Dato de laboratorio | Valor |
|---|---:|
| Límite líquido | 250 |
| Límite plástico | 45 |
| Pasa la malla N.º 4 | 100 % |
| Pasa la malla N.º 40 | 80 % |
| Pasa la malla N.º 200 | 70 % |

El motor devuelve **CH** e **índice de plasticidad 205**. Este caso forma parte de las pruebas de la API.

## Estructura del repositorio

| Directorio | Contenido |
|---|---|
| `backend/app/domain/` | Modelo de muestra, validaciones y clasificación SUCS en Python |
| `backend/app/api/` | Rutas HTTP de FastAPI |
| `backend/tests/` | Pruebas automatizadas con pytest |
| `mobile/` | Aplicación Flutter para Android |
| `docs/` | Arquitectura, decisiones técnicas, criterios normativos e historial de desarrollo |

## Ejecutar las pruebas del backend

Desde la raíz del repositorio, con Python 3.12 y un entorno virtual activo:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m pytest -q
```

## Probar la API de clasificación

El endpoint está disponible en `feature/api-clasificacion`. Desde la raíz del repositorio:

```powershell
git switch feature/api-clasificacion
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Abre `http://127.0.0.1:8000/docs` y selecciona `POST /classify` para enviar una muestra y consultar el resultado.

## Ejecutar la aplicación móvil

Con Flutter instalado y un emulador Android iniciado, ejecuta desde la raíz:

```powershell
cd mobile
flutter pub get
flutter run
```

## Alcance técnico

El proyecto sirve de apoyo a la clasificación de muestras. La validación integral frente a la edición oficial de ASTM D2487 sigue pendiente.