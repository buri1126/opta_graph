from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class HealthResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    
class ScrapingResponse(BaseModel):
    status: str
    message: str

class ScrapingRequest(BaseModel):
    url: str
    selector: Optional[str] = None
    wait_time: Optional[int] = 3

class ScrapingResult(BaseModel):
    success: bool
    title: Optional[str]
    url: str
    content: Optional[str] = None
    elements: Optional[List[Dict[str, Any]]] = None
    count: Optional[int] = 0
    error: Optional[str] = None