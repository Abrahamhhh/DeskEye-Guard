from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import DetectionEvent
from schemas import RecentEventOut
from services.auth_service import CurrentUser

router = APIRouter()
Database = Annotated[Session, Depends(get_db)]


@router.get("/recent", response_model=list[RecentEventOut])
def recent_events(db: Database, current_user: CurrentUser, limit: int = Query(20, ge=1, le=100)) -> list[RecentEventOut]:
    query = select(DetectionEvent).where(DetectionEvent.user_id == current_user.id).order_by(DetectionEvent.created_at.desc()).limit(limit)
    rows = db.scalars(query).all()
    return [RecentEventOut(id=row.id, alert_type=row.event_type, message=row.message or "检测到姿态变化", status="pending" if row.risk_level >= 2 else "handled", created_at=row.created_at) for row in rows]
