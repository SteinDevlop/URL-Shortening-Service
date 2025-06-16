import logging
from fastapi import (
    Form, HTTPException, APIRouter
)
from backend.models.urlacess import UrlacessCreate, UrlacessOut
from backend.logic.universal_controller_instance import universal_controller as controller

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/urlaccess", tags=["urlaccess"])

@app.post("/create")
async def create_urlaccess(
    UrlID: int = Form(...),
    TimesAccess: int = Form(...),
):
    try:
        new_urlaccess = UrlacessCreate(
            UrlID=UrlID,
            TimesAccess=TimesAccess,
        )
        controller.add(new_urlaccess)

        logger.info(f"[POST /create] urlaccess creada exitosamente: {new_urlaccess}")
        return {
            "operation": "create",
            "success": True,
            "data": UrlacessOut(**new_urlaccess.model_dump()).model_dump(),
            "message": "urlaccess created successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update")
async def update_urlaccess(
    AccessID: int = Form(...),
    UrlID: int = Form(...),
    TimesAccess: int = Form(...),
):
    try:
        existing = controller.get_by_id(UrlacessOut, AccessID)
        if existing is None:
            logger.warning(f"[POST /update] urlaccess no encontrada: AccessID={AccessID}")
            raise HTTPException(404, detail="urlaccess not found")

        updated_urlaccess = UrlacessCreate(
            AccessID=AccessID,
            UrlID=UrlID,
            TimesAccess=TimesAccess,
        )
        controller.update(updated_urlaccess)

        logger.info(f"[POST /update] urlaccess actualizada exitosamente: {updated_urlaccess}")
        return {
            "operation": "update",
            "success": True,
            "data": UrlacessOut(**updated_urlaccess.model_dump()).model_dump(),
            "message": f"urlaccess {AccessID} updated successfully."
        }
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /update] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/delete")
async def delete_urlaccess(
    AccessID: int = Form(...)
):
    try:
        existing = controller.get_by_id(UrlacessOut, AccessID)
        if not existing:
            logger.warning(f"[POST /delete] urlaccess no encontrada: AccessID={AccessID}")
            raise HTTPException(404, detail="urlaccess not found")

        controller.delete(existing)
        logger.info(f"[POST /delete] urlaccess eliminada exitosamente: AccessID={AccessID}")
        return {
            "operation": "delete",
            "success": True,
            "message": f"urlaccess {AccessID} deleted successfully."
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=str(e))