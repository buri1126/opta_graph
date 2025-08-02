from fastapi import APIRouter, HTTPException
from api.schemas.response import ScrapingResponse, ScrapingRequest, ScrapingResult
from api.schemas.scraping import TottenhamStatsResponse
from api.utils.webdriver import WebDriverHelper

router = APIRouter()

@router.get("/scraping", response_model=ScrapingResponse)
async def get_scraping():
    return {"status": "ok", "message": "Scraping endpoint is working"}

@router.post("/scraping/basic", response_model=ScrapingResult)
async def scrape_basic(request: ScrapingRequest):
    """基本的なスクレイピング（タイトル + テキスト）"""
    try:
        scraper = WebDriverHelper(headless=True)
        result = scraper.scrape_basic(
            url=request.url,
            wait_time=request.wait_time or 3
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.post("/scraping/elements", response_model=ScrapingResult)
async def scrape_elements(request: ScrapingRequest):
    """CSSセレクターで指定した要素をスクレイピング"""
    if not request.selector:
        raise HTTPException(status_code=400, detail="Selector is required for element scraping")
    
    try:
        scraper = WebDriverHelper(headless=True)
        result = scraper.scrape_elements(
            url=request.url,
            selector=request.selector,
            wait_time=request.wait_time or 3
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.get("/scraping/test")
async def test_scraping():
    """テスト用エンドポイント（Google.comをスクレイピング）"""
    try:
        scraper = WebDriverHelper(headless=True)
        result = scraper.scrape_basic("https://www.google.com", wait_time=3)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/scraping/theanalyst-tottenham")
async def scrape_theanalyst_tottenham():
    """theanalyst.comでTottenhamのデータをスクレイピング"""
    try:
        scraper = WebDriverHelper(headless=True)
        result = scraper.scrape_theanalyst_tottenham(wait_time=15)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

@router.post("/scraping/tottenham-formatted", response_model=TottenhamStatsResponse)
async def scrape_tottenham_formatted():
    """theanalyst.comでTottenhamのデータをスクレイピング（フロントエンド向け整形済み）"""
    try:
        scraper = WebDriverHelper(headless=True)
        result = scraper.scrape_theanalyst_tottenham(wait_time=15)
        
        if result["success"] and "formatted_data" in result:
            return result["formatted_data"]
        else:
            return TottenhamStatsResponse(
                success=False,
                team="tottenham",
                total_players=0,
                players=[],
                headers=[],
                error=result.get("error", "Unknown error occurred")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")