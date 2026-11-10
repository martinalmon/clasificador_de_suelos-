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


# GeoStratix — Guía de Git y GitHub

**Proyecto:** GeoStratix v1  
**Documento:** `docs/GIT_FLUJO.md`  
**Estado:** Guía de trabajo vigente  
**Última actualización:** 9 de noviembre de 2026

---

## 1. Objetivo

Establecer un procedimiento para administrar el código fuente de GeoStratix mediante Git y GitHub.

Esta guía debe ser consultada antes de iniciar una nueva funcionalidad, crear una rama, realizar un commit o integrar cambios.

El proyecto utiliza un flujo de trabajo con tres tipos de ramas:

- `main`: versión estable.
- `develop`: integración de funcionalidades terminadas.
- `feature/*`: desarrollo de funcionalidades individuales.

**Regla principal:** No desarrollar directamente en `main`.

## 2. Estructura del repositorio

```text
GeoStratix_Flutter_Python_Starter/
├── backend/
│   ├── app/
│   └── tests/
├── mobile/
│   ├── android/
│   ├── lib/
│   └── test/
├── docs/
│   ├── ARQUITECTURA.md
│   ├── CONTEXTO_IA.md
│   ├── CRITERIOS_NORMATIVOS.md
│   ├── DECISIONES.md
│   ├── ESTADO.md
│   ├── GIT_FLUJO.md
│   └── INSTALACION.md
└── README.md
```

El repositorio contiene tanto la aplicación móvil Flutter como el backend Python y su documentación.

## 3. Función de cada rama

### `main` — Versión estable

Contiene el código que se considera estable y adecuado para preparar una versión de distribución.

Reglas:

- No realizar cambios directamente.
- No utilizarla para experimentos.
- Integrar cambios después de validarlos en `develop`.
- Crear etiquetas de versión cuando corresponda.

### `develop` — Rama de integración

Recibe las funcionalidades terminadas y probadas.

Reglas:

- Las nuevas ramas `feature/*` deben crearse desde `develop`.
- Integrar únicamente funcionalidades que hayan superado sus pruebas.
- Verificar que los cambios no afecten otros módulos.
- Mantener la documentación actualizada.

### `feature/*` — Desarrollo de funcionalidades

Cada nueva funcionalidad debe desarrollarse en una rama independiente.

Ejemplos:

```text
feature/modelo-muestras
feature/clasificacion-suelos-gruesos
feature/api-clasificacion
feature/interfaz-captura
feature/reportes-pdf
```

Reglas:

- Crear la rama desde `develop`.
- Trabajar únicamente en la funcionalidad correspondiente.
- Hacer commits descriptivos.
- Ejecutar pruebas antes de integrar.
- No mezclar modificaciones ajenas a la funcionalidad.

## 4. Flujo general de desarrollo

```text
main
  │
  └── develop
        │
        ├── feature/modelo-muestras
        │       └── Implementación y pruebas
        │
        ├── feature/clasificacion-suelos-gruesos
        │       └── Implementación y pruebas
        │
        └── feature/reportes-pdf
                └── Implementación y pruebas
```

Las ramas `feature/*` salen de `develop` y regresan a `develop` cuando terminan.

Posteriormente, una versión validada de `develop` puede integrarse en `main`.

## 5. Procedimiento para iniciar una funcionalidad

**Paso 1. Verificar el estado del repositorio.**

```powershell
git status
git branch
```

Antes de cambiar de rama, asegurarse de que no existan modificaciones sin guardar que puedan provocar conflictos.

**Paso 2. Cambiar a `develop`.**

```powershell
git switch develop
```

**Paso 3. Descargar cambios recientes.**

```powershell
git pull origin develop
```

**Paso 4. Crear la nueva rama.**

Ejemplo:

```powershell
git switch -c feature/clasificacion-suelos-gruesos
```

**Paso 5. Publicar la rama en GitHub.**

```powershell
git push -u origin feature/clasificacion-suelos-gruesos
```

Después se puede comenzar a programar.

## 6. Procedimiento para guardar avances

**Paso 1. Revisar los cambios.**

```powershell
git status
```

**Paso 2. Ejecutar las pruebas correspondientes.**

Para el backend:

```powershell
cd backend
python -m pytest -v
cd ..
```

Para Flutter:

```powershell
cd mobile
flutter test
cd ..
```

Ejecutar las pruebas que correspondan a los componentes modificados.

**Paso 3. Agregar los archivos al área de preparación.**

Desde la raíz del repositorio:

```powershell
git add .
```

Alternativamente:

```powershell
git add -A
```

`git add -A` prepara todos los cambios del repositorio, independientemente de la subcarpeta desde donde se ejecute.

**Paso 4. Verificar qué se incluirá.**

```powershell
git status
git diff --cached --stat
```

No incluir archivos temporales, entornos virtuales, credenciales ni resultados de compilación.

**Paso 5. Crear el commit.**

```powershell
git commit -m "feat: agrega clasificacion de suelos gruesos"
```

**Paso 6. Subir a GitHub.**

```powershell
git push
```

Si la rama todavía no tiene seguimiento remoto:

```powershell
git push -u origin nombre-de-la-rama
```

## 7. Convenciones para mensajes de commit

Usar mensajes claros que describan el cambio realizado.

| Prefijo | Uso |
|---|---|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de errores |
| `docs:` | Cambios de documentación |
| `test:` | Incorporación o modificación de pruebas |
| `refactor:` | Reorganización de código sin cambiar su comportamiento previsto |
| `chore:` | Configuración y mantenimiento |
| `style:` | Cambios de formato sin modificar la lógica |

Ejemplos:

```text
feat: implementa clasificador SUCS de suelos finos
test: agrega pruebas de limites de Atterberg
fix: corrige validacion de porcentajes pasantes
docs: actualiza estado del desarrollo
refactor: separa validaciones granulometricas
chore: configura estructura inicial del proyecto
```

## 8. Integración de una funcionalidad en `develop`

Antes de integrar:

- Confirmar que la funcionalidad esté terminada.
- Ejecutar las pruebas correspondientes.
- Actualizar la documentación.
- Revisar que todos los cambios estén guardados en commits.
- Subir la rama a GitHub.

Procedimiento local:

```powershell
git switch develop
git pull origin develop
git merge --no-ff feature/nombre-funcionalidad
```

Si no existen conflictos y las pruebas siguen pasando:

```powershell
git push origin develop
```

**Alternativa recomendada:** Crear un Pull Request en GitHub desde la rama `feature/*` hacia `develop` para revisar los cambios antes de integrarlos.

No ejecutar `git push` después de un merge con conflictos sin resolver.

## 9. Integración de `develop` en `main`

La rama `main` debe actualizarse únicamente cuando se prepare una versión estable.

Antes de integrarla:

- Ejecutar pruebas generales del backend.
- Ejecutar pruebas Flutter.
- Confirmar que la aplicación Android compila.
- Verificar que la documentación corresponde con el código.
- Revisar los cambios importantes y las dependencias.

Una vez validado:

```powershell
git switch main
git pull origin main
git merge --no-ff develop
git push origin main
```

Para registrar una versión estable, por ejemplo:

```powershell
git tag -a v0.1.0 -m "GeoStratix version 0.1.0"
git push origin v0.1.0
```

No crear una etiqueta de lanzamiento hasta que exista una versión realmente validada.

## 10. Cómo consultar el estado de Git

Mostrar la rama actual:

```powershell
git branch
```

Mostrar los cambios pendientes:

```powershell
git status
```

Mostrar los commits recientes:

```powershell
git log --oneline -10
```

Mostrar el historial de ramas:

```powershell
git log --oneline --graph --decorate --all
```

Mostrar los repositorios remotos:

```powershell
git remote -v
```

Verificar qué archivos están preparados para un commit:

```powershell
git diff --cached --name-only
```

## 11. Errores comunes y soluciones

### `git add .` no incluye archivos de otras carpetas

Puede ocurrir cuando se ejecuta desde una subcarpeta.

Solución:

```powershell
git add -A
```

O regresar a la raíz del repositorio:

```powershell
cd ..
git add .
```

### `nothing to commit, working tree clean`

Significa que no hay modificaciones pendientes en el directorio de trabajo.

No es un error.

### `Everything up-to-date`

Significa que no existen commits locales pendientes de subir a esa rama remota.

### Git rechaza un `push`

Puede indicar que el repositorio remoto contiene cambios que aún no están integrados localmente.

Revisar primero:

```powershell
git status
git fetch origin
```

Analizar la diferencia antes de realizar nuevas operaciones.

No utilizar `git push --force` para resolverlo automáticamente.

### Conflictos durante un merge

Git indicará los archivos afectados.

Se deben revisar y resolver manualmente, ejecutar las pruebas y completar el merge.

No sobrescribir archivos sin comprender qué cambios se están descartando.

## 12. Archivos que no deben subirse

Evitar incluir:

```text
.env
.venv/
__pycache__/
.pytest_cache/
.dart_tool/
build/
*.pyc
```

Los secretos, claves de API, contraseñas y credenciales nunca deben guardarse en Git.

Revisar el archivo `.gitignore` y comprobar qué archivos se prepararon antes de hacer commit.

## 13. Historial de ramas de GeoStratix

| Rama | Funcionalidad | Estado registrado                            |
|---|---|----------------------------------------------|
| `main` | Base estable del proyecto | Creada                                       |
| `develop` | Integración de funcionalidades | Creada                                       |
| `feature/modelo-muestras` | Modelo de muestras y clasificador de suelos finos | 20 pruebas aprobadas; push realizado         |
| `feature/clasificacion-suelos-gruesos` | Clasificación de gravas y arenas | implementando; 38 pruebas totales aprobadas  |
| `feature/clasificador-unificado` | Clasificador SUCS automático para suelos finos y gruesos | Implementado; 46 pruebas totales aprobadas |

Actualizar esta tabla cuando se creen, integren o cierren ramas.

## 14. Reglas para asistentes de inteligencia artificial

Antes de modificar GeoStratix, cualquier asistente de IA debe:

1. Consultar `docs/CONTEXTO_IA.md`.
2. Consultar `docs/ESTADO.md`.
3. Consultar `docs/ARQUITECTURA.md`.
4. Consultar `docs/DECISIONES.md` y `docs/CRITERIOS_NORMATIVOS.md` cuando corresponda.
5. Consultar esta guía `docs/GIT_FLUJO.md`.
6. Identificar la rama activa.
7. Respetar la arquitectura y las decisiones documentadas.
8. Evitar cambios ajenos a la funcionalidad solicitada.
9. Proponer o implementar pruebas para cada nueva funcionalidad.
10. Actualizar la documentación pertinente.
11. No afirmar que una funcionalidad fue probada sin resultados de pruebas.
12. No hacer merge a `develop` o `main` sin autorización del desarrollador.

**Principio fundamental:** El historial de Git y la documentación deben permitir continuar el desarrollo sin depender de una conversación anterior.

---

## 15. Mantenimiento de esta guía

Este documento debe actualizarse cuando:

- Se adopte una nueva estrategia de ramas.
- Se cree una rama importante.
- Se integren funcionalidades.
- Cambie el procedimiento de pruebas.
- Se establezcan reglas de Pull Requests.
- Se prepare una versión estable.
- Se detecte un error frecuente y se documente su solución.

Los cambios exclusivos de documentación deben registrarse con mensajes como:

```text
docs: actualiza guia de ramas y flujo de Git
```

**Fin de la guía de Git y GitHub — GeoStratix.**