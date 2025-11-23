from fastapi import HTTPException
from api import app
from models.novel import Novel
from services.honeyfeed import HoneyFeed


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/novels/honeyfeed/{novel_id}", response_model=Novel)
async def get_honeyfeed_novel(novel_id: str) -> Novel:
    try:
        return HoneyFeed.scrape_novel(novel_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to scrape novel: {str(e)}")
