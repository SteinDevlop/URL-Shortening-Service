import logging
from fastapi import (
    HTTPException, APIRouter
)
from backend.models.url import UrlOut
from backend.logic.universal_controller_instance import universal_controller as controller
from fastapi import status
from fastapi.responses import RedirectResponse
# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(tags=["redirect"])

@app.get("/{short_url}")
async def redirect(short_url: str):
    """
    Recupera una URL larga por su url.
    """
    try:
        url = controller.get_by_url_short(UrlOut, short_url)
        logger.info(f"[GET /] Resultado de get_by_url_short: {url}")
    except ValueError as e:
        logger.warning(f"[GET /] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[GET /] Error interno: {str(e)}", exc_info=True)
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
    if url:
        logger.info(f"[GET /] URL encontrada: {getattr(url, 'ID', None)}, {getattr(url, 'UrlOriginal', None)} -> {getattr(url, 'UrlShort', None)}")
        try:
            redirect_url = f"{url.UrlOriginal}"
            controller.increment_access_db(short_url)
            return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND)
        except Exception as e:
            logger.error(f"[GET /] Error al serializar la respuesta: {str(e)}", exc_info=True)
            raise HTTPException(500, detail=f"Error serializando la respuesta: {str(e)}")
    else:
        logger.warning(f"[GET /] No se encontró URL ={short_url}")
        return {"detail": "URL not found"}