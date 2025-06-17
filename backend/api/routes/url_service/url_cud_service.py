import logging
from fastapi import (
    Form, HTTPException, APIRouter
)
import datetime
from backend.models.url import UrlCreate, UrlOut
from backend.logic.universal_controller_instance import universal_controller as controller

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/shorten", tags=["shorten"])

@app.post("/")
async def create_url(
    Url: str = Form(...),
):
    if Url.find("http://") == -1 and Url.find("https://") == -1:
        logger.warning(f"[POST /create] URL inválida: {Url}")
        raise HTTPException(400, detail="Invalid URL format. Must start with 'http://www.' or 'https://www.'")
    try:
        new_url = UrlCreate(
            UrlOriginal=Url,UpdateDate=datetime.datetime.now(), CreatedDate=datetime.datetime.now(),UrlShort=controller.generate_unique_code()
        )
        controller.add(new_url)

        logger.info(f"[POST /create] URL creada exitosamente: {new_url}")
        return UrlOut(**new_url.model_dump()).model_dump()
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.put("/{short_url}")
async def update_url(
    short_url: str,
    New_UrlShort: str = Form(...),
):
    try:
        logger.info(f"[PUT /{short_url}] Buscando URL existente para actualizar...")
        existing = controller.get_by_url_short(UrlOut, short_url)
        if existing is None:
            logger.warning(f"[PUT /{short_url}] URL no encontrada")
            raise HTTPException(404, detail="URL not found")

        updated_url = UrlCreate(
            ID=getattr(existing, "ID", None),
            UrlOriginal=getattr(existing, "UrlOriginal", None),
            UrlShort=New_UrlShort,
            CreatedDate=getattr(existing, "CreatedDate", None),
            UpdateDate=datetime.datetime.now()
        )
        controller.update(updated_url)

        logger.info(f"[PUT /{short_url}] URL actualizada exitosamente: {updated_url}")
        return UrlOut(**updated_url.model_dump()).model_dump()
    except ValueError as e:
        logger.warning(f"[PUT /{short_url}] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[PUT /{short_url}] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.delete("/",status_code=204)
async def delete_url(
    short_url: str = Form(...)
):
    try:
        existing = controller.get_by_url_short(UrlOut, short_url)
        if not existing:
            logger.warning(f"[POST /delete] URL no encontrada: url={short_url}")
            raise HTTPException(404, detail="URL not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] URL eliminada exitosamente: url={short_url}")
        return UrlOut(**existing.model_dump()).model_dump()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=str(e))