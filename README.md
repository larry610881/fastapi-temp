# PayChecked Admin (Python Migration)

本專案為 PayChecked 後台管理系統的 Python 重構版本，採用 **FastAPI** 與 **Clean Architecture** 實作，並逐步遷移原 Laravel 系統之核心商業邏輯。

## 核心架構

本專案採用分層架構，確保邏輯清晰、易於測試且具備高度擴展性：

```text
app/
├── main.py                 # 應用程式進入點 (FastAPI)
├── main_cli.py             # 命令行工具進入點 (Typer)
├── api/                    # 路由層 (Request/Response)
├── core/                   # 核心配置 (Config, Security, Redis)
├── db/                     # 資料庫核心 (Session, Base)
├── models/                 # 資料庫模型 (SQLAlchemy 2.0 Async)
├── schemas/                # 資料驗證模型 (Pydantic V2)
├── services/               # 業務邏輯層 (Service Pattern)
├── repositories/           # 資料存取層 (Repository Pattern)
└── commands/               # 命令行指令 (Console Commands)
```

## 快速啟動

### 方式一：Docker 一鍵啟動 (推薦)

自動啟動 **API + MySQL 8.0 + Redis**：

1.  啟動服務：
    ```bash
    docker-compose up --build -d
    ```
2.  驗證狀態：
    - API Health: [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 方式二：本地開發

1.  安裝依賴：
    ```bash
    pip install -r requirements.txt
    ```
2.  啟動開發伺服器：
    ```bash
    uvicorn app.main:app --reload
    ```

## 開發指南

### 資料庫遷移 (Alembic)

本專案使用 Alembic 進行資料庫版本控制。當修改 `app/models` 下的模型定義後：

1.  **產生遷移檔**：
    ```bash
    alembic revision --autogenerate -m "描述變更內容"
    ```
2.  **套用遷移**：
    ```bash
    alembic upgrade head
    ```

### 命令行工具 (CLI)

專案整合 **Typer** 用於執行各類後台任務與排程指令：

```bash
# 語法
python -m app.main_cli <指令名稱> [選項]

# 範例：執行訂單狀態更新
python -m app.main_cli charge-status
```

### 測試規範 (TDD & BDD)

遵循 **TDD** 與 **BDD** 開發流程，並依專案規範使用 **繁體中文** 撰寫測試描述 (.feature 檔與 Docstrings)。

- **單元測試 (Unit Tests)**:
  ```bash
  pytest
  ```
- **行為測試 (BDD)**:
  ```bash
  behave
  ```

## 遷移進度 (Migration Progress)

目前正逐步將 PHP/Laravel 邏輯遷移至 Python 環境：

- [x] **核心架構**: FastAPI + SQLAlchemy Async + Docker 環境搭建
- [x] **資料庫模型**: 完成 Order, User, Bank, Gps 及主要金流對帳表 (BMS, Cathay, ICP, PayUni 等) 之模型定義
- [x] **自動化遷移**: 整合 Alembic 並接管現有資料庫結構
- [/] **Console Commands**:
    - [x] `charge-status`: 訂單狀態更新
    - [ ] `check-order-diff`: 訂單差異比對 (規劃中)
    - [ ] 產品與結算相關指令 (遷移中)
