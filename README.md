# PayChecked Admin (Python Migration)

本專案為 PayChecked 後台管理系統的 Python 重構版本，採用 **FastAPI** + **Clean Architecture** 實作。

## 核心架構

```text
app/
├── main.py                 # FastAPI 入口 + 全域錯誤處理
├── main_cli.py             # Typer CLI + 全域錯誤處理
├── core/
│   ├── config.py           # 環境設定 + 驗證
│   └── container.py        # 依賴注入容器 (DI Container)
├── db/
│   └── session.py          # Async DB Session + 連線池
├── models/                 # SQLAlchemy 2.0 Async Models
├── schemas/                # Pydantic V2 Schemas
├── services/               # 業務邏輯層 (DI 注入)
├── repositories/           # 資料存取層
└── commands/               # CLI 指令 (@inject 注入)
```

## 近期重構 (2026-02-04)

### 架構改善
- ✅ **DI Container**: 使用 `dependency-injector` 統一管理依賴
- ✅ **全域錯誤處理**: API (`exception_handler`) / CLI (`cli_exception_handler`)
- ✅ **DB 連線池**: 配置 `pool_size`, `max_overflow`, `pool_recycle`
- ✅ **Repository 拆分**: `OrderRepository` / `OrderStatusRepository`
- ✅ **重試機制**: `tenacity` 處理 HTTP 逾時與連線錯誤
- ✅ **CORS 環境感知**: 根據 `ENVIRONMENT` 動態設定 Origins

### 測試框架
- ✅ **pytest-bdd**: 取代 behave，整合 pytest 生態系
- ✅ **單元測試**: 9/9 通過

---

## 快速啟動

### Docker (推薦)
```bash
docker-compose up --build -d
```
- API: http://127.0.0.1:8000/docs

### 本地開發
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## CLI 指令

```bash
# 訂單狀態反查
python -m app.main_cli charge-status <訂單編號> [ICP|CTBC]
```

---

## 測試

```bash
# 單元測試
$env:PYTHONPATH = "."; pytest tests/unit/ -v

# BDD 測試 (開發中)
$env:PYTHONPATH = "."; pytest tests/step_defs/ -v
```

---

## 遷移進度

- [x] FastAPI + SQLAlchemy Async + Docker
- [x] DI Container + 全域錯誤處理
- [x] `charge-status` 指令
- [ ] `check-order-diff` 指令
- [x] 安全性掃描整合 (Semgrep)
