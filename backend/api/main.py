import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.middlewares import add_middlewares
from backend.logic.universal_controller_instance import universal_controller
from backend.api.routes.url_service import (url_cud_service, url_query_service)
from backend.api.routes.urlaccess_service import (urlaccess_cud_service, urlaccess_query_service)
from backend.api.routes.redirect import redirect_service
# Inicializar la aplicación FastAPI
app = FastAPI(title=settings.PROJECT_NAME)

# Añadir middlewares globales
add_middlewares(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:49607",  # solo si aún pruebas en local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eventos de inicio y apagado
@app.on_event("startup")
async def startup_event():
    print("Conexión establecida con la base de datos")

@app.on_event("shutdown")
async def shutdown_event():
    if universal_controller.conn:
        universal_controller.conn.close()
        print("Conexión cerrada correctamente")

# Incluir rutas de los microservicios
app.include_router(url_cud_service.app)
app.include_router(urlaccess_cud_service.app)
app.include_router(url_query_service.app)
app.include_router(urlaccess_query_service.app)
app.include_router(redirect_service.app)