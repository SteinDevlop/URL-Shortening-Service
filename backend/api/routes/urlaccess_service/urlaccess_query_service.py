import logging
from fastapi import Query, APIRouter,HTTPException
from backend.models.urlacess import UrlacessCreate, UrlacessOut
from backend.models.url import UrlOut
from backend.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create the router for card-related endpoints
app = APIRouter(prefix="/shorten", tags=["shorten"])

@app.get("/all")
async def get_urls():
    """
    Recupera y retorna todos los registros de URLs desde la base de datos.
    """
    urls = controller.read_all(UrlOut)
    logger.info(f"[GET /all] Número de URLs encontradas: {len(urls)}")
    # Convertir a dict para serializar correctamente
    return [u.to_dict() if hasattr(u, "to_dict") else dict(u) for u in urls]

@app.get("/get")
async def get_url(ID: int = Query(...)):
    """
    Recupera una URL por su ID.
    """
    url = controller.get_by_id(UrlOut, ID)
    if url:
        logger.info(f"[GET /get] URL encontrada: {url.ID}, {url.UrlOriginal} -> {url.UrlShort}")
        return url.to_dict() if hasattr(url, "to_dict") else dict(url)
    else:
        logger.warning(f"[GET /get] No se encontró URL con ID={ID}")
        return {"detail": "URL not found"}
@app.get("/{short_url}/stats")
async def get_url(short_url: str):
    """
    Entrega numero de entradas a la URL corta.
    """
    try:
        url = controller.get_by_url_short(UrlOut, short_url)
        urlaccess = controller.get_by_urlid(UrlacessOut, url.ID)
        logger.info(f"[GET /] Resultado de get_by_url_short: {url}")
        logger.info(f"[GET /] Resultado de get_by_url_access: {urlaccess} y {url.ID}")
    except ValueError as e:
        logger.warning(f"[GET /] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[GET /] Error interno: {str(e)}", exc_info=True)
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
    if url:
        logger.info(f"[GET /] URL encontrada: {getattr(url, 'ID', None)}, {getattr(url, 'UrlOriginal', None)} -> {getattr(url, 'UrlShort', None)}")
        try:
            result = url.to_dict() if hasattr(url, "to_dict") else dict(url)
            logger.info(f"[GET /] Respuesta serializada: {result}")
            return {**result, **urlaccess.to_dict()}
        except Exception as e:
            logger.error(f"[GET /] Error al serializar la respuesta: {str(e)}", exc_info=True)
            raise HTTPException(500, detail=f"Error serializando la respuesta: {str(e)}")
    else:
        logger.warning(f"[GET /] No se encontró URL ={short_url}")
        return {"detail": "URL not found"}