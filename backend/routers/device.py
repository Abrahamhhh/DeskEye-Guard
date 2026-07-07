from datetime import timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import DetectionEvent, Device, utc_now
from schemas import DeviceEventCreate, EventOut
from services.stats_service import apply_event_to_stats

router = APIRouter()
Database = Annotated[Session, Depends(get_db)]
DEFAULT_MESSAGES = {
    "normal": "坐姿正常", "away": "用户暂时离座", "head_down": "检测到低头",
    "lean_forward": "检测到身体前倾", "head_tilt": "检测到头部偏斜",
    "long_sitting": "检测到连续久坐", "phone_detected": "检测到使用手机",
}


@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_device_event(data: DeviceEventCreate, db: Database, x_device_key: Annotated[str, Header(alias="X-Device-Key")]) -> DetectionEvent:
    device = db.scalar(select(Device).where(Device.device_key == x_device_key))
    if device is None:
        raise HTTPException(status_code=401, detail="设备密钥无效")
    event_time = data.created_at or utc_now()
    if event_time.tzinfo is not None:
        event_time = event_time.astimezone(timezone.utc).replace(tzinfo=None)
    event = DetectionEvent(device_id=device.id, user_id=device.owner_id, event_type=data.event_type, is_present=data.is_present, risk_level=data.risk_level, face_area=data.face_area, head_angle=data.head_angle, message=data.message or DEFAULT_MESSAGES[data.event_type], created_at=event_time)
    device.status = "online"
    device.last_seen = utc_now()
    db.add(event)
    apply_event_to_stats(db, device.owner_id, event_time.date(), data.event_type, data.duration_minutes, data.risk_level)
    db.commit()
    db.refresh(event)
    return event
