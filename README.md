# FastAPI Hybrid Boilerplate (Professional Skill Structure)

實作（SQLAlchemy 2.0 Async, Pydantic V2）與 **Professional Skill** 建議的 `Repository/Service` 分層架構的 FastAPI 樣板。

## 核心架構

本專案採用 **Clean Architecture** 分層模式，確保邏輯清晰、易於測試且具備高度擴展性：

```text
app/
├── main.py                 # 初始化 FastAPI 與中間件
├── api/                    # 路由處理 (只處理 Request/Response 膠水)
│   ├── v1/
│   │   ├── endpoints/      # 具體的業務路由 (如 health.py)
│   │   └── router.py       # 彙整所有路由
│   └── dependencies.py     # 全域依賴注入 (Auth, Get DB)
├── core/                   # 核心配置 (Pydantic Settings & Redis)
│   ├── config.py           # .env 讀取與設定
│   ├── security.py         # JWT 與加密
│   └── redis.py            # Redis Client 初始化與連線
├── db/                     # 資料庫核心
│   ├── base.py             # 基礎類別 (Base)，解決循環引用
│   ├── session.py          # 非同步連線 (Engine, SessionLocal, get_db)
│   └── __init__.py         # 暴露常用組件
├── models/                 # 資料庫模型 (SQLAlchemy 2.0 Async 模型)
├── schemas/                # 資料驗證模型 (Pydantic V2)
├── services/               # 業務邏輯層 (複雜業務邏輯)
├── repositories/           # 資料訪問層 (封裝所有 SQL/Redis 查詢)
alembic/                    # 獨立遷移資料夾
├── versions/               # 遷移版本腳本
└── env.py                  # Alembic 環境配置
alembic.ini                 # Alembic 設定檔
```

**職責分離**：將舊邏輯拆解為 `Service` 與 `Repository`，避免 `async def` 中混入同步阻塞代碼。

## 快速啟動

### 方式一：Docker 一鍵啟動 (推薦)

這會自動啟動 **API + MySQL 8.0 + Redis**：

1.  執行指令：
    ```bash
    docker-compose up --build
    ```
2.  驗證狀態：
    訪問 [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
    確認 `database` 與 `redis` 皆為 `connected`。

### 方式二：本地開發

1.  安裝依賴：
    ```bash
    pip install -r requirements.txt
    ```
2.  啟動開發伺服器：
    ```bash
    uvicorn app.main:app --reload
    ```

## 驗證與文件

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **健康檢查**: `/api/v1/health` (已內建 MySQL 與 Redis 連線測試)
- **測試**: 執行 `pytest` 進行基礎功能驗證。

---

## PHP to Python 遷移進度 (Migration Progress)

目前已完成從 PHP/Laravel 至 FastAPI 的核心架構遷移，主要包含：

-   **資料庫模型 (Models)**: 已遷移 Order, User, Bank, Gps 及大量對帳用金流財會資料表（BMS, Cathay, ICP, PayUni 等）。
-   **架構特點**:
    -   實作 **Soft Delete**Mixins 與事件監聽。
    -   **SQLAlchemy 2.0 Async** 非同步資料庫連線。
    -   **Alembic** 遷移系統對接現有資料庫架構。
-   **開發環境**: 整合 Docker Compose 固定網路名稱 (`payngo-admin-python_default`) 與統一的環境變數管理。

更多細節請見 [walkthrough](file:///C:/Users/P10359945/.gemini/antigravity/brain/4c309daa-9a3c-4615-822e-c2afef4f27b7/walkthrough.md) (僅限本地參考)。
