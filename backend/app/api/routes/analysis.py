from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import AnalysisResponse
from app.services.analysis import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])

_service = AnalysisService()

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/tiff", "image/jpg"}


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    """
    Upload a petri dish image and receive a bacterial colony count
    along with an annotated result image (base64 PNG).
    """
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: {ALLOWED_CONTENT_TYPES}",
        )

    image_bytes = await file.read()

    try:
        result = _service.analyze(image_bytes)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    return result
