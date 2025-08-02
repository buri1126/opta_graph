from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

class ScrapingRequest(BaseModel):
    url: str
    selector: Optional[str] = None  # CSSセレクター
    wait_time: Optional[int] = 3    # 待機時間（秒）

class ScrapingResult(BaseModel):
    success: bool
    url: str
    title: Optional[str] = None
    data: List[Dict[str, Any]] = []
    timestamp: datetime
    error: Optional[str] = None

class PlayerStats(BaseModel):
    name: str
    apps: int
    mins: int
    goals: int
    xg: float
    goals_vs_xg: float
    shots: int
    sot: int
    conv_percent: str
    xg_per_shot: float

class TottenhamStatsResponse(BaseModel):
    success: bool
    team: str
    total_players: int
    players: List[PlayerStats]
    headers: List[str]
    error: Optional[str] = None

class ScrapingJob(BaseModel):
    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    url: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[ScrapingResult] = None