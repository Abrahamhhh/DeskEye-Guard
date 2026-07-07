"""HTTP API 的请求与响应结构。"""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EventType = Literal[
    "normal", "away", "head_down", "lean_forward", "head_tilt",
    "long_sitting", "phone_detected"
]


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=6, max_length=72)


class UserLogin(BaseModel):
    username: str
    password: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6, max_length=72)


class UserOut(ORMModel):
    id: int
    username: str
    role: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DeviceEventCreate(BaseModel):
    event_type: EventType
    is_present: bool = True
    risk_level: int = Field(default=0, ge=0, le=3)
    face_area: float | None = Field(default=None, ge=0)
    head_angle: float | None = None
    message: str | None = Field(default=None, max_length=255)
    duration_minutes: int = Field(default=1, ge=0, le=1440)
    created_at: datetime | None = None


class EventOut(ORMModel):
    id: int
    device_id: int
    user_id: int
    event_type: str
    is_present: bool
    risk_level: int
    face_area: float | None
    head_angle: float | None
    message: str
    created_at: datetime


class RecentEventOut(BaseModel):
    id: int
    alert_type: str
    message: str
    status: str
    created_at: datetime
    username: str | None = None


class TodayStatsOut(BaseModel):
    date: date
    normal_minutes: int
    bad_posture_minutes: int
    head_down_count: int
    lying_on_desk_count: int
    tilt_head_count: int
    too_close_count: int
    phone_detected_count: int
    screen_minutes: int
    break_count: int
    today_alerts_count: int
    health_score: int
    summary: str


class TrendOut(BaseModel):
    date: date
    normal_minutes: int
    bad_posture_minutes: int
    health_score: int
    screen_minutes: int
    break_count: int
