---
name: web-api-design
description: 使用 FastAPI 構建生產就緒 API 的標準，包含相依注入、安全性和 OpenAPI 文件規範。
---

# Web API 設計與 FastAPI 標準 (Web API Design & FastAPI Standards)

用於構建可擴展、安全且文件齊備的 API 的統一指南。

## 核心原則 (Core Principles)

1. **FastAPI 結構**: 使用 **Repository-Service-Controller (RSC)** 模式來解耦邏輯。
2. **相依注入 (Dependency Injection)**: 利用 FastAPI 的 `Depends` 功能來處理資料庫會話 (DB sessions) 與身份驗證 (Auth)。
3. **數據模型 (Schemas)**: 所有請求與響應的驗證必須使用 **Pydantic V2**。
4. **自動化文件**: 確保每個終端點 (Endpoint) 都具備清晰的摘要 (Summary) 與標籤 (Tags)，以生成優質的 OpenAPI 文件。

## 實作流程 (Implementation Flow)

- 定義 **Pydantic Schema** (數據結構)。
- 實作 **Repository** (負責 SQLAlchemy/Tortoise 等資料庫操作)。
- 實作 **Service** (負責核心業務邏輯)。
- 在 **APIRouter** 中定義終端點 (Endpoint)。

## 嚴禁行為 (Anti-Patterns)
- **禁止**在 Controller (Router) 中直接調用 `db.execute()` 或 `session.query()`。
- **禁止**在 Service 層撰寫原生 SQL 或複雜的 ORM 查詢邏輯。
- **規則**: Service 層只能調用 Repository 的 method (例如 `self.repo.get_by_id`)。