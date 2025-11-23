from fastapi import HTTPException
from api import app
from models.novel import Novel
from services.honeyfeed import HoneyFeedScraper


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/novels/honeyfeed/{novel_id}", response_model=Novel)
async def get_honeyfeed_novel(novel_id: str) -> Novel:
    """
    Scrape and return a novel from HoneyFeed by its ID.
    
    Args:
        novel_id: The HoneyFeed novel ID
        
    Returns:
        Novel object with title, chapters, and metadata
        
    Raises:
        HTTPException: If the novel cannot be found or scraped
    """
    try:
        scraper = HoneyFeedScraper(novel_id)
        novel = scraper.scrape_novel()
        return novel
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to scrape novel: {str(e)}")
