# CONTEXTO IA — GeoStratix (documento principal)

## Alcance confirmado
- v1: SOLO clasificación SUCS de muestras, entrada manual de resultados de laboratorio.
- UI: Flutter/Dart, trabajo en Android Studio.
- Backend/lógica: Python, API FastAPI; no usar Kotlin para el motor.
- No incluir mapas, predicción litológica, redes neuronales, cuentas ni servidor de datos en v1.
- Referencias: resumen ASTM D2487-17(2025) y PDF ASTM D2487-06 facilitados por el usuario.
- **No afirmar conformidad completa con ASTM 2025 sin contrastar texto oficial completo.**

## Reglas de ingeniería
KISS, DRY, YAGNI, responsabilidad única, validación explícita, pruebas, documentación Markdown por cambio, commits atómicos y code review antes del merge.

## Estado actual
- Entregado scaffold Flutter y API de salud Python sin lógica SUCS.
- No verificado con Flutter/Android SDK en este entorno (no instalados).
- No configurado Git remoto (URL no proporcionada en el mensaje visible).

## Siguiente tarea
Definir contratos de entrada/salida de muestra y validador en `backend/app/domain`, pruebas unitarias con casos límite, documentar criterios con referencia por página. Después exponer `/classify` y conectar desde Flutter.

## Cómo continuar
En una nueva sesión, leer en este orden `docs/CONTEXTO_IA.md`, `docs/ESTADO.md`, `docs/DECISIONES.md`, `docs/CRITERIOS_NORMATIVOS.md` y el historial Git; no asumir tareas pendientes como terminadas.
