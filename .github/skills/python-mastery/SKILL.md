---
name: python-mastery
description: 完整的 Python 開發標準，包含 async/await、設計模式、測試以及現代化代碼風格 (Ruff/Mypy)。適用於所有 Python 相關任務。
---

# Python 精通：標準與模式 (Python Mastery: Standards & Patterns)

本項技能將所有 Python 相關標準整合為單一的事實來源，旨在建立高性能且易於維護的應用程式。

## 核心支柱 (Core Pillars)

1. **現代程式碼風格**: 使用 `ruff` 進行代碼檢查與格式化，並使用 `mypy` 進行嚴格的型別檢查。
2. **卓越的異步處理**: 精通 `asyncio` 以實現非阻塞式 I/O。使用 `asyncio.gather()` 處理併發任務，並使用 `asyncio.to_thread()` 處理阻塞型的同步調用。
3. **強健的錯誤處理**: 使用自定義異常 (Custom Exceptions) 與具體的錯誤捕捉區塊。避免使用不指定類型的空 `except:`。
4. **測試驅動品質**: 使用 `pytest` 與 `pytest-asyncio`。重點放在 API 流程的整合測試。

## 最佳實踐 (Best Practices)

- **行寬限制**: 120 個字元。
- **命名規範**: 函式與變數使用 `snake_case`，類別使用 `PascalCase`。
- **異步規則**: 在調用路徑中保持完整的異步化。除非是將任務分派給執行緒 (Threads)，否則不要混用同步與異步代碼。
- **文件規範**: 所有公開 API 均須撰寫 Google 風格的文件字串 (Docstrings)。
