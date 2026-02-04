---
name: unified-development-workflow
description: 所有 Python 開發任務的總綱執行指南，涵蓋從需求分析到部署的完整路徑。
---

# 統一開發工作流 (Unified Development Workflow)

當開始任何開發任務時，請**嚴格遵循**以下五個階段的執行順序。所有技術細節必須對應 `.github/skills/` 目錄下的特定規範文件。

## 第一階段：規格與架構設計 (Design & ADR)
- **架構對齊**：參考 `#file:system-architecture.md` 中的 **SOLID 原則**進行設計，確保低耦合度。
- **決策紀錄**：若涉及重大架構變動或技術選型，必須撰寫或更新 **ADR (Architectural Decision Records)**。
- **遷移確認**：若是 PayNGo 遷徙任務，需比對舊版 PHP 邏輯，確認 `#file:migration-and-modernization.md` 中的對應模式。

## 第二階段：行為驅動開發 (BDD Phase)
- **需求轉化**：在撰寫任何程式碼前，先依 `#file:bdd-tdd-standards.md` 撰寫 Gherkin 語法 (Given/When/Then) 的行為描述。
- **定義邊界**：確保 Feature 文件精確反映業務流程，作為後續測試的唯一基準。

## 第三階段：測試驅動開發 (TDD Phase)
- **紅燈預熱**：根據行為描述，撰寫一個必會失敗的 `pytest` 測試案例。
- **核心強制要求**：**禁止在沒有對應測試案例的情況下開始實作任何功能代碼。**
- **環境隔離**：利用 `pytest-mock` 嚴格隔離資料庫與外部 GCP 服務。

## 第四階段：規範化實作 (Implementation)
- **RSC 模式實作**：嚴格依照 `#file:web-api-design.md` 的順序開發，**嚴禁跨層調用**：
    1. 定義 **Pydantic Schema** (Request/Response)。
    2. 實作 **Repository** (SQLAlchemy 專屬層)。
    3. 實作 **Service** (處理 Business Logic)。
    4. 定義 **FastAPI Router** (Entry Point)。
- **代碼品質**：強制執行 `#file:python-mastery.md` 規範，必須通過 `ruff` 與 `mypy` 靜態檢查。
- **異步完整性**：確保 I/O 密集型任務全程使用 `async/await`，禁止阻塞主線程。

## 第五階段：驗證、重構與部署 (Verify & Deploy)
- **綠燈與重構**：測試通過後，根據 SOLID 原則重構以消除 Code Smell。
- **觀測標準**：檢查日誌是否符合 `#file:devops-and-observability.md` 的結構化日誌規範。
- **自動化驗證**：提交 PR 後必須通過 CI 流水線的所有自動化檢查，始可部署至 GCP Cloud Run。