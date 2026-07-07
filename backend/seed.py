"""初始化演示账号、设备和图表数据，可重复执行。"""

from datetime import date, timedelta
from sqlalchemy import select
from database import Base, SessionLocal, engine
from models import DailyStats, DetectionEvent, Device, User, utc_now
from services.auth_service import get_password_hash


def user(db, username: str, password: str, role: str) -> User:
    row = db.scalar(select(User).where(User.username == username))
    if row is None:
        row = User(username=username, password_hash=get_password_hash(password), role=role)
        db.add(row)
        db.flush()
    return row


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user(db, "admin", "admin123", "admin")
        demo_user = user(db, "user", "user123", "user")
        device = db.scalar(select(Device).where(Device.device_key == "demo-device-key"))
        if device is None:
            device = Device(device_name="DeskEye ESP32-S3", device_key="demo-device-key", owner_id=demo_user.id, status="online", last_seen=utc_now())
            db.add(device)
            db.flush()

        for days_ago in range(7):
            day = date.today() - timedelta(days=days_ago)
            exists = db.scalar(select(DailyStats.id).where(DailyStats.user_id == demo_user.id, DailyStats.stat_date == day))
            if exists is None:
                db.add(DailyStats(user_id=demo_user.id, stat_date=day, total_events=8 + days_ago, normal_minutes=70 - days_ago * 3, bad_posture_minutes=15 + days_ago * 2, head_down_count=2 + days_ago % 2, lean_forward_count=1, head_tilt_count=days_ago % 2, long_sitting_count=1, phone_detected_count=1, screen_minutes=90, break_count=3, alert_count=3, health_score=max(60, 91 - days_ago * 2)))

        if db.scalar(select(DetectionEvent.id).where(DetectionEvent.user_id == demo_user.id).limit(1)) is None:
            now = utc_now()
            db.add_all([
                DetectionEvent(device_id=device.id, user_id=demo_user.id, event_type="normal", risk_level=0, message="坐姿正常", created_at=now - timedelta(minutes=10)),
                DetectionEvent(device_id=device.id, user_id=demo_user.id, event_type="head_down", risk_level=2, head_angle=-18.5, message="检测到低头，请注意调整", created_at=now - timedelta(minutes=5)),
                DetectionEvent(device_id=device.id, user_id=demo_user.id, event_type="lean_forward", risk_level=2, message="检测到身体前倾", created_at=now),
            ])
        db.commit()
    print("演示数据初始化完成：admin/admin123，user/user123，设备密钥 demo-device-key")


if __name__ == "__main__":
    seed()
