import logging
from fastapi import APIRouter, HTTPException
from service.demo_2_embeddings import DemoEmbeddingsService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/video-2",
    tags=["Embeddings Demo"],
    responses={404: {"description": "Not found"}},
)

embeddings_service = DemoEmbeddingsService()


@router.post("/convert-to-embeddings")
async def convert_to_embeddings_route(text: str):
    logger.info(f"convert_to_embeddings_route called with text: {text[:50]}...") # Log first 50 chars
    try:
        result = embeddings_service.convertToEmbeddings(text)
        logger.info("convert_to_embeddings_route successful.")
        return {"embeddings": result}
    except ValueError as e:
        logger.error(f"ValueError in convert_to_embeddings_route: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error in convert_to_embeddings_route: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/from-documents")
async def get_embeddings_from_documents_route(documents: list[str]):
    logger.info(f"get_embeddings_from_documents_route called with {len(documents)} documents.")
    try:
        result = embeddings_service.getEmbeddingsFromDocuments(documents)
        logger.info("get_embeddings_from_documents_route successful.")
        return {"document_embeddings": result}
    except ValueError as e:
        logger.error(f"ValueError in get_embeddings_from_documents_route: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error in get_embeddings_from_documents_route: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@router.post("/search")
async def embeddings_search_route(query: str, documents: list[str]):
    logger.info(f"embeddings_search_route called with query: '{query}' and {len(documents)} documents.")
    try:
        month_facts = [
            # January
            "January is named after the Roman god Janus, the god of beginnings and endings",
            # February
            "February is the only month that can pass without a single full moon",
            # March
            "The expression 'Mad as a March Hare' comes from the hare's unusual behavior during its breeding season in March",
            # April
            "The diamond (April's birthstone) is one of the hardest natural substances on Earth",
            # May
            "The month of May is named for the Greek goddess Maia, who was the goddess of fertility",
            # June
            "June has the longest daylight hours of the year in the Northern Hemisphere (Summer Solstice)",
            # July
            "Before being named after Julius Caesar, July was called Quintilis, which is Latin for 'fifth'",
            # August
            "August was originally named Sextilis ('sixth') before being renamed for Augustus Caesar",
            # September
            "September comes from the Latin word septem, meaning 'seven', as it was the seventh month in the Roman calendar",
            # October
            "The first week of October is officially World Space Week",
            # November
            "Daylight Saving Time ends in November, giving everyone an 'extra' hour of sleep",
            # December
            "The Winter Solstice, the day with the shortest daylight in the Northern Hemisphere, occurs in December",
        ]
        question = "which month's old name is in latin that represents a number?"

        result = embeddings_service.embeddingsSearch(
            question if query == "" else query,
            documents if len(documents) > 0 else month_facts,
        )
        logger.info("embeddings_search_route successful.")
        return {"search_results": result}
    except ValueError as e:
        logger.error(f"ValueError in embeddings_search_route: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error in embeddings_search_route: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
