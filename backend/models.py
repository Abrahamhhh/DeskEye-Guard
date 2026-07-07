"""DeskEye Guard 数据库模型。"""

from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(10), default="user", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)

    devices: Mapped[list["Device"]] = relationship(back_populates="owner")
    events: Mapped[list["DetectionEvent"]] = relationship(back_populates="user")
    daily_stats: Mapped[list["DailyStats"]] = relationship(back_populates="user")


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_name: Mapped[str] = mapped_column(String(100), nullable=False)
    device_key: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(10), default="offline", nullable=False)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, nullable=False)

    owner: Mapped[User] = relationship(back_populates="devices")
    events: Mapped[list["DetectionEvent"]] = relationship(back_populates="device")


class DetectionEvent(Base):
    __tablename__ = "detection_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    is_present: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    risk_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    face_area: Mapped[float | None] = mapped_column(Float, nullable=True)
    head_angle: Mapped[float | None] = mapped_column(Float, nullable=True)
    message: Mapped[str] = mapped_column(String(255), default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, index=True, nullable=False)

    device: Mapped[Device] = relationship(back_populates="events")
    user: Mapped[User] = relationship(back_populates="events")


class DailyStats(Base):
    __tablename__ = "daily_stats"
    __table_args__ = (UniqueConstraint("user_id", "stat_date", name="uq_daily_stats_user_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    stat_date: Mapped[date] = mapped_column(Date, index=True, nullable=False)
    total_events: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    normal_minutes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    bad_posture_minutes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    head_down_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    lean_forward_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    head_tilt_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    long_sitting_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    phone_detected_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    screen_minutes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    break_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    alert_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    health_score: Mapped[int] = mapped_column(Integer, default=100, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    user: Mapped[User] = relationship(back_populates="daily_stats")
