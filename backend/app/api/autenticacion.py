"""Autenticación para pruebas con el emulador local de Firebase."""

import os
from typing import Annotated

import firebase_admin
from firebase_admin import auth
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


router = APIRouter(prefix="/auth", tags=["Autenticación"])
bearer = HTTPBearer(auto_error=False)

firebase_app = firebase_admin.initialize_app(
    options={"projectId": "demo-sucs-local"},
    name="sucs-auth-local",
)


def obtener_usuario_actual(
        credenciales: Annotated[
            HTTPAuthorizationCredentials | None,
            Depends(bearer),
        ],
) -> dict:
    """Verifica el token enviado en Authorization: Bearer."""
    if credenciales is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Debes iniciar sesión.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if os.environ.get("FIREBASE_AUTH_EMULATOR_HOST") != "127.0.0.1:9099":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Configura el emulador local de autenticación.",
        )

    try:
        return auth.verify_id_token(
            credenciales.credentials,
            app=firebase_app,
        )
    except (auth.InvalidIdTokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token es inválido o ha expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None


@router.get("/me")
def consultar_mi_usuario(
        usuario: Annotated[dict, Depends(obtener_usuario_actual)],
) -> dict[str, str]:
    """Devuelve la identidad obtenida del token verificado."""
    return {"uid": usuario["uid"]}