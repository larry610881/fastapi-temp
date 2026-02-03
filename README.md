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
├── core/                   # 核心配置
│   ├── config.py           # .env 讀取與設定 (Pydantic Settings)
│   ├── database.py         # SQLAlchemy Engine 與 Async Session 管理
│   └── redis.py            # Redis Client 初始化與連線
├── models/                 # 資料庫模型 (SQLAlchemy 2.0 Async 模型)
├── schemas/                # 資料驗證模型 (Pydantic V2)
├── services/               # 業務邏輯層 (橫跨多個 Repo 的複雜邏輯)
├── repositories/           # 資料訪問層 (封裝所有 SQL/Redis 查詢)
└── db/                     # [調整] 基礎資料庫操作 (Session, Base)
alembic/                    # [新增] 獨立遷移資料夾
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


