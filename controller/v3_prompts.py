import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from service.demo_3_prompt  import DemoPromptService, ResponseLengthOptions, ResponseFormatOptions


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/video-3",
    tags=["Prompts Demo"],
    responses={404: {"description": "Not found"}},
)

prompt_service = DemoPromptService()


class SummarizeRequest(BaseModel):
    content: str
    responseLength: ResponseLengthOptions = ResponseLengthOptions.SHORT
    responseFormat: ResponseFormatOptions = ResponseFormatOptions.PLAIN_TEXT

    @field_validator('content')
    @classmethod
    def content_must_be_valid_length(cls, v):
        if len(v) == 0:
            raise ValueError('Content length must be greater than 0')
        if len(v) > 2000:
            raise ValueError('Content length must be less than 2000 characters')
        return v

@router.post("/summarize")
async def summarize_route(request: SummarizeRequest):
    content = request.content

    logger.info(f"summarize_route called with content: '{content[:50]}...'")

    try:
        result = prompt_service.getSummarizePrompt(
            max_length=request.responseLength,
            response_format=request.responseFormat,
            content=content,
        )
        logger.info("summarize_route successful.")
        return {
            "summary": result,
            "meta": {
                "model": "gpt-3.5-turbo"  # or whatever model is being used
            }
        }
    except ValueError as e:
        logger.error(f"ValueError in summarize_route: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Internal server error in summarize_route: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
