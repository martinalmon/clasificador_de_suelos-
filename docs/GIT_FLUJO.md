# Git y revisiones

Ejecutar desde la raíz tras verificar el scaffold:

```bash
git init -b main
git add .
git commit -m "chore: inicia GeoStratix con Flutter y API Python"
git branch develop
git switch develop
git switch -c feature/modelo-muestras
```

Para repositorio remoto **existente**, NO ejecutar `git init` ni sobrescribir su historia: clonar el remoto y copiar dentro el proyecto (sin `.git`), luego commitear. Cuando se conozca URL: `git remote add origin <URL>` solo si aún no existe `origin`.

Flujo: feature → tests → docs → revisión → merge a develop. `main` solo para releases probadas. No hacer merge/push remotos automáticamente.
