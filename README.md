# DeskEye Guard

DeskEye Guard 是一个基于 ESP32-S3 的桌面行为感知与坐姿纠正课程项目。当前版本已完成 Vue 前端与 FastAPI 后端联调，可用设备密钥上报模拟检测事件，并展示实时状态、提醒和历史统计。

## 技术栈

- 硬件：ESP32-S3（Arduino）
- 后端：Python、FastAPI、SQLite、SQLAlchemy
- 视觉分析：OpenCV、MediaPipe
- 前端：Vue 3、Vite（后续接入 ECharts）

## 目录结构

```text
backend/   FastAPI 接口、数据库及业务服务
frontend/  Vue 3 用户界面
esp32/     ESP32-S3 Arduino 示例
docs/      技术文档、分工说明与开发日志
```

## 启动后端

```powershell
cd backend
python -m venv .venv
```

激活虚拟环境：

```powershell
# Windows
.venv\Scripts\activate
```

```bash
# macOS / Linux
source .venv/bin/activate
```

安装依赖、初始化演示数据并启动：

```powershell
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```

访问 `http://127.0.0.1:8000/api/health` 检查服务状态，接口文档位于 `http://127.0.0.1:8000/docs`。

首次启动前建议复制环境变量模板并修改 JWT 密钥：

```powershell
Copy-Item .env.example .env
```

核心数据库与接口设计见 `docs/后端接口说明.md`。演示设备密钥为 `demo-device-key`。

演示账号为管理员 `admin/admin123` 和普通用户 `user/user123`。运行后端测试：

```powershell
cd backend
pytest -q
```

## 启动前端

```powershell
cd frontend
npm install
npm run dev
```

也可以使用 `pnpm install` 和 `pnpm run dev`。前端默认访问 `http://localhost:8000`，可通过 `VITE_API_BASE_URL` 修改。

## 联调测试

1. 启动后端和前端，使用 `user/user123` 登录。
2. 查看实时状态、今日统计、最近事件和七日坐姿趋势。
3. 模拟设备上报：

```powershell
Invoke-RestMethod -Method Post -Uri http://localhost:8000/api/device/events `
  -Headers @{ 'X-Device-Key' = 'demo-device-key' } `
  -ContentType 'application/json' `
  -Body '{"event_type":"head_down","risk_level":2,"head_angle":-18.5,"duration_minutes":5}'
```

4. 返回前端点击“刷新数据”，确认低头次数、提醒和健康评分发生变化。

开发服务器默认显示终端给出的本地访问地址，并将 `/api` 请求代理至后端的 8000 端口。

## 后续开发计划

1. 完成数据库表和登录权限。
2. 接入 ESP32-S3 摄像头图像流。
3. 实现坐姿识别、久坐判断和提醒策略。
4. 完成历史统计图表与管理员功能。
5. 开展接口、算法和系统验收测试。
