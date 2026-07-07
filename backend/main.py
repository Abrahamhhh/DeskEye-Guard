"""DeskEye Guard FastAPI 服务入口。"""

from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from database import Base, engine  # noqa: E402
import models  # noqa: E402, F401
from routers import admin, auth, device, events, stats  # noqa: E402


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="DeskEye Guard API", version="0.3.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(stats.router, prefix="/api/stats", tags=["统计"])
app.include_router(events.router, prefix="/api/events", tags=["检测事件"])
app.include_router(device.router, prefix="/api/device", tags=["设备上报"])
app.include_router(admin.router, prefix="/api/admin", tags=["管理员"])


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "project": "DeskEye Guard"}
