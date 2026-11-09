# Arquitectura

```
mobile/lib/features/classification/presentation  → Flutter widgets
mobile/lib/features/classification/data          → cliente HTTP (futuro)
mobile/lib/features/classification/domain        → modelos Dart para intercambio (futuro)
backend/app/api                                  → FastAPI rutas
backend/app/domain                               → reglas geotécnicas Python puras (futuro)
```

Las fórmulas de clasificación aparecen SOLO en `backend/app/domain`. La UI no clasifica ni duplica reglas. No añadir repositorios genéricos, microservicios ni módulos sin necesidad. Durante desarrollo la API corre en PC; producción requiere desplegarla y HTTPS.
