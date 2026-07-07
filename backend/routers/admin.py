from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models import DailyStats, DetectionEvent, Device, User
from services.auth_service import AdminUser

router = APIRouter()
Database = Annotated[Session, Depends(get_db)]


@router.get("/devices")
def devices(db: Database, _: AdminUser) -> list[dict]:
    rows = db.scalars(select(Device).order_by(Device.created_at.desc())).all()
    result = []
    for device in rows:
        latest = db.scalar(select(DetectionEvent).where(DetectionEvent.device_id == device.id).order_by(DetectionEvent.created_at.desc()).limit(1))
        result.append({"id": device.id, "device_name": device.device_name, "username": device.owner.username, "status": device.status, "last_seen": device.last_seen, "last_posture": latest.event_type if latest else "unknown", "failed_recognition_count": 0})
    return result


@router.get("/events")
def all_events(db: Database, _: AdminUser, limit: int = Query(50, ge=1, le=200)) -> list[dict]:
    rows = db.scalars(select(DetectionEvent).order_by(DetectionEvent.created_at.desc()).limit(limit)).all()
    return [{"id": row.id, "username": row.user.username, "alert_type": row.event_type, "message": row.message, "status": "pending" if row.risk_level >= 2 else "handled", "created_at": row.created_at} for row in rows]


@router.get("/summary")
def summary(db: Database, _: AdminUser) -> dict[str, int]:
    count = lambda model: db.scalar(select(func.count(model.id))) or 0
    return {"total_users": count(User), "total_devices": count(Device), "online_devices": db.scalar(select(func.count(Device.id)).where(Device.status == "online")) or 0, "total_records": count(DetectionEvent), "today_records": db.scalar(select(func.coalesce(func.sum(DailyStats.total_events), 0)).where(DailyStats.stat_date == date.today())) or 0}
