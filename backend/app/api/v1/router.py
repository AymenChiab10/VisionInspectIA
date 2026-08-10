"""
Routeur principal de la version v1 de l'API.

Agrege l'ensemble des routeurs de app/api/v1/endpoints/ et les enregistre
chacun avec son prefixe et son tag Swagger.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    predictions,
    history,
    dashboard,
    reports,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(predictions.router, prefix="/predictions", tags=["Predictions"])
api_router.include_router(history.router, prefix="/history", tags=["History"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
