"""前后端约定的核心接口端到端测试。"""

import os
import tempfile
from pathlib import Path

db_file = Path(tempfile.gettempdir()) / "deskeye_integration_test.db"
db_file.unlink(missing_ok=True)
os.environ["DATABASE_URL"] = f"sqlite:///{db_file.as_posix()}"
os.environ["SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402
from database import SessionLocal  # noqa: E402
from main import app  # noqa: E402
from models import Device, User  # noqa: E402
from services.auth_service import get_password_hash  # noqa: E402


def test_frontend_backend_flow() -> None:
    with TestClient(app) as client:
        with SessionLocal() as db:
            user = User(username="user", password_hash=get_password_hash("user123"), role="user")
            db.add(user)
            db.flush()
            db.add(Device(device_name="Test ESP32", device_key="test-device-key", owner_id=user.id))
            db.commit()

        login = client.post("/api/auth/login", json={"username": "user", "password": "user123"})
        assert login.status_code == 200
        headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
        event = client.post("/api/device/events", headers={"X-Device-Key": "test-device-key"}, json={"event_type": "head_down", "risk_level": 2, "head_angle": -18.5, "duration_minutes": 5})
        assert event.status_code == 201
        assert client.post("/api/device/events", headers={"X-Device-Key": "wrong"}, json={"event_type": "normal"}).status_code == 401
        assert client.get("/api/stats/today", headers=headers).json()["head_down_count"] == 1
        assert len(client.get("/api/events/recent", headers=headers).json()) == 1
        assert len(client.get("/api/stats/posture-trend", headers=headers).json()) == 7
