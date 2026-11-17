"""Conexión a Firestore para desarrollo local."""

import os
from collections.abc import Generator

from fastapi import HTTPException
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore


def obtener_base_datos() -> Generator[firestore.Client, None, None]:
    if os.environ.get("FIRESTORE_EMULATOR_HOST") != "127.0.0.1:8080":
        raise HTTPException(
            status_code=503,
            detail="Configura el emulador local de Firestore.",
        )

    cliente = firestore.Client(
        project="demo-sucs-local",
        credentials=AnonymousCredentials(),
    )

    try:
        yield cliente
    finally:
        cliente.close()
        