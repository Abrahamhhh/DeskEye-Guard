"""检测事件写入后的每日统计聚合。"""

from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import DailyStats

RISK_EVENTS = {"head_down", "lean_forward", "head_tilt", "long_sitting"}


def get_or_create_daily_stats(db: Session, user_id: int, day: date) -> DailyStats:
    stats = db.scalar(select(DailyStats).where(DailyStats.user_id == user_id, DailyStats.stat_date == day))
    if stats is None:
        stats = DailyStats(user_id=user_id, stat_date=day)
        db.add(stats)
        db.flush()
    return stats


def apply_event_to_stats(db: Session, user_id: int, day: date, event_type: str, duration: int, risk_level: int) -> DailyStats:
    stats = get_or_create_daily_stats(db, user_id, day)
    stats.total_events += 1
    if event_type == "normal":
        stats.normal_minutes += duration
    elif event_type == "away":
        stats.break_count += 1
    elif event_type == "phone_detected":
        stats.phone_detected_count += 1
    elif event_type in RISK_EVENTS:
        stats.bad_posture_minutes += duration
        setattr(stats, f"{event_type}_count", getattr(stats, f"{event_type}_count") + 1)
    if event_type != "away":
        stats.screen_minutes += duration
    if event_type in RISK_EVENTS and risk_level >= 2:
        stats.alert_count += 1
    penalty = stats.head_down_count * 2 + stats.lean_forward_count * 2 + stats.head_tilt_count + stats.long_sitting_count * 3
    stats.health_score = max(0, 100 - penalty)
    return stats
