---
name: migration-and-modernization
description: 從 PHP/Laravel 遺留程式碼遷移至現代 Python/GCP 架構的最佳實踐。
---

# 系統遷徙與現代化指南 (Migration & Modernization Guide)

專為 PayNGo 系統從 PHP 轉型為 Python 開發所設計的專業技能規範。

## 遷徙模式 (Migration Patterns)

1. **從命令到任務 (Command to Task)**: 將 Laravel 的 Artisan 指令遷移至 Python CLI 工具或 Prefect 任務流。
2. **從任務到事件驅動 (Job to Event-Driven)**: 使用 GCP Pub/Sub 與非同步事件處理程式 (Async Event Handlers) 取代原本的 Laravel Queues 佇列系統。
3. **從 Eloquent 到 SQLAlchemy**: 確保資料庫模型 (Models) 與關聯性 (Relations) 的精確映射與對接。

## 現代化目標 (Modernization Goals)

- **無伺服器化**: 全面遷移至 Serverless 架構 (如 GCP Cloud Functions 或 Cloud Run)。
- **非同步改造**: 使用非阻塞式 (Non-blocking) 的 `async` 邏輯取代原本的阻塞式同步 (Blocking sync) 邏輯。
- **集中化觀測**: 實施統一的觀測機制 (結合 Python Logging 與 GCP Cloud Logging)。
