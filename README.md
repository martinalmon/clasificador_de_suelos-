# GeoStratix v1 — Flutter + Python

**Estado:** proyecto inicial de arquitectura; motor SUCS aún no implementado. Android Studio se utilizará para Flutter y Android SDK. Se necesita Flutter SDK instalado.

## Estructura

- `mobile/`: app Flutter/Dart (UI); no contiene fórmulas geotécnicas.
- `backend/`: servicio Python con FastAPI; futuros módulos ASTM D2487.
- `docs/`: documentación versionada para continuar con asistencia de IA.

## Preparación (Windows)

1. Instala Flutter SDK, Android Studio y Flutter/Dart plugins. Ejecuta `flutter doctor`.
2. Abre terminal en `mobile` y ejecuta `flutter create --platforms=android --project-name geostratix_mobile --org com.geostratix .` (crea los archivos Android/Gradle propios de tu Flutter SDK y mantiene los archivos Dart existentes). Si Flutter pregunta por sobrescribir archivos preexistentes, **no sobrescribas** `lib/`, `test/` ni `pubspec.yaml`; consulta `docs/INSTALACION.md`.
3. Ejecuta `flutter pub get` y `flutter run`.
4. Crea un entorno virtual Python en `backend`: `py -m venv .venv`, actívalo e instala `pip install -r requirements.txt`.
5. Arranca API desde `backend`: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
6. En emulador Android la dirección del host es `http://10.0.2.2:8000`; en escritorio es `http://127.0.0.1:8000`. La interfaz inicial no consume la API todavía.
7. Para pruebas: `pytest` en backend; `flutter test` en mobile.

**Importante:** un backend Python externo requiere conectividad cuando se clasifica. Para funcionar completamente offline habrá que elegir una solución distinta (p. ej. portar lógica a Dart o incorporar un runtime Python compatible), decisión todavía pendiente. No se incluye despliegue de producción ni credenciales.

## Git

Consultar `docs/GIT_FLUJO.md`. No se incluye `.git` para evitar interferir con un repositorio existente. No se ha configurado `origin` porque falta URL.
