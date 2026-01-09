from pydantic import BaseModel
from datetime import date
from typing import Dict, Optional

#---daily input model

class DailyLog(BaseModel):
    log_date: date
    raw_text: str
    journaled_text: Optional[str] = None

#---Task Model

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    planned: bool = True
    completed: bool = False

#---Stat Model

class StatSnapshot(BaseModel):
    strength: int
    intelligence: int
    lifestyle: int
    mental_health: int
    financial_health: int
    ovr: int

#---XP Model

class XPEvent(BaseModel):
    stat: str
    amount: float
    reason: str
    log_date: date

#---Report Model

class Report(BaseModel):
    period: str
    start_date: date
    end_date: date
    stats_summary: Dict[str, int]
    key_insights: list[str]
    suggested_adjustments: list[str] 