from datetime import date, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import DailyStats
from schemas import TodayStatsOut, TrendOut
from services.auth_service import CurrentUser

router = APIRouter()
Database = Annotated[Session, Depends(get_db)]


def serialize_today(stats: DailyStats | None, day: date) -> TodayStatsOut:
    if stats is None:
        return TodayStatsOut(date=day, normal_minutes=0, bad_posture_minutes=0, head_down_count=0, lying_on_desk_count=0, tilt_head_count=0, too_close_count=0, phone_detected_count=0, screen_minutes=0, break_count=0, today_alerts_count=0, health_score=100, summary="今日暂无检测数据")
    summary = "坐姿状态良好，请继续保持" if stats.health_score >= 80 else "存在不良坐姿，请注意调整和休息"
    return TodayStatsOut(date=day, normal_minutes=stats.normal_minutes, bad_posture_minutes=stats.bad_posture_minutes, head_down_count=stats.head_down_count, lying_on_desk_count=stats.lean_forward_count, tilt_head_count=stats.head_tilt_count, too_close_count=0, phone_detected_count=stats.phone_detected_count, screen_minutes=stats.screen_minutes, break_count=stats.break_count, today_alerts_count=stats.alert_count, health_score=stats.health_score, summary=summary)


@router.get("/today", response_model=TodayStatsOut)
def today_stats(db: Database, current_user: CurrentUser) -> TodayStatsOut:
    today = date.today()
    stats = db.scalar(select(DailyStats).where(DailyStats.user_id == current_user.id, DailyStats.stat_date == today))
    return serialize_today(stats, today)


@router.get("/posture-trend", response_model=list[TrendOut])
def posture_trend(db: Database, current_user: CurrentUser, days: int = Query(7, ge=1, le=31)) -> list[TrendOut]:
    today = date.today()
    stored = db.scalars(select(DailyStats).where(DailyStats.user_id == current_user.id, DailyStats.stat_date >= today - timedelta(days=days - 1))).all()
    by_date = {row.stat_date: row for row in stored}
    result = []
    for days_ago in reversed(range(days)):
        day = today - timedelta(days=days_ago)
        row = by_date.get(day)
        result.append(TrendOut(date=day, normal_minutes=row.normal_minutes if row else 0, bad_posture_minutes=row.bad_posture_minutes if row else 0, health_score=row.health_score if row else 100, screen_minutes=row.screen_minutes if row else 0, break_count=row.break_count if row else 0))
    return result
