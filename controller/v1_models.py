import logging
from fastapi import APIRouter
from service.demo_1_models import DemoModel

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/video-1",
    tags=["Demo"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def demoChat(question: str):
    logger.info(f"demoChat endpoint called with question: {question}")
    try:
        result = DemoModel.chat(question)
        logger.info(f"demoChat endpoint returning with message: {result}")
        return {"message": result}
    except Exception as e:
        logger.error(f"Error in demoChat endpoint: {e}", exc_info=True)
        return {"error": str(e)}, 500

