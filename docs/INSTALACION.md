# Instalación segura

Este ZIP es un **scaffold de código fuente**, no un proyecto Flutter nativo pre-generado: `flutter` no estaba disponible al crear el ZIP. En tu PC instala Flutter y Android Studio.

**Método más seguro**:
1. Copia el ZIP descomprimido a una ruta temporal.
2. Desde otra carpeta ejecuta: `flutter create --org com.geostratix --platforms android geostratix_mobile`.
3. Copia del ZIP sobre ese proyecto los archivos `mobile/lib`, `mobile/test`, `mobile/pubspec.yaml` y `mobile/analysis_options.yaml`.
4. Conserva `android/`, `gradle/`, y archivos generados por Flutter.
5. Ejecuta `flutter pub get`, `flutter analyze`, `flutter test`, `flutter run`.
6. Abre la carpeta `geostratix_mobile` con Android Studio.
7. Mantén el repositorio monorepo con esa carpeta renombrada a `mobile` y el `backend`/`docs` al mismo nivel.

### Backend (Windows PowerShell)
```
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Consulta `http://localhost:8000/health` en el navegador. Si se conecta desde el emulador Android: `http://10.0.2.2:8000/health`.
