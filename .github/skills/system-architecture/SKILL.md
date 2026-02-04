---
name: system-architecture
description: 高階架構模式、SOLID 原則、資料庫優化以及 ADR 架構決策紀錄標準。
---

# 系統架構與資料庫標準 (System Architecture & Database Standards)

旨在設計具備韌性 (Resilient) 的系統與優化資料層的指導方針。

## 核心關注領域 (Key Focus Areas)

1. **SOLID 原則**: 特別強調「單一職責原則 (Single Responsibility)」與「依賴倒置原則 (Dependency Inversion)」。
2. **資料庫效能**: 正確配置索引 (Indexing)、避免 N+1 查詢問題，並使用優化後的 Join 查詢。
3. **ADR (架構決策紀錄)**: 詳細記錄重大技術決策背後的具體原因與考量。
4. **設計模式**: 偏好「組合 (Composition)」優於「繼承 (Inheritance)」。針對複雜的邏輯分支，優先使用工廠模式 (Factories) 與策略模式 (Strategies)。