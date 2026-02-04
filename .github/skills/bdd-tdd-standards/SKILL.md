---
description: BDD (行為驅動開發) 與 TDD (測試驅動開發) 的標準作業規範與語言指南
---

# BDD/TDD 開發規範

此 Skill 定義了本專案在進行行為驅動開發 (BDD) 與測試驅動開發 (TDD) 時必須遵循的標準，特別是語言與格式要求。

## 1. BDD (.feature) 撰寫規範

當撰寫或修改 `.feature` 檔案時，**必須** 遵守以下規則：

### A. 語言要求
*   **關鍵字**：保留 Gherkin 英文關鍵字以確保語法高亮支援。
    *   `Feature`, `Scenario`, `Scenario Outline`, `Given`, `When`, `Then`, `And`, `But`, `Examples`
*   **描述內容**：所有的描述文字 **必須使用繁體中文 (Traditional Chinese)**。
    *   ✅ 正確：`Given 訂單 "ORD-001" 存在於資料庫中`
    *   ❌ 錯誤：`Given order "ORD-001" exists in the database`

### B. 檔案結構範例
```gherkin
Feature: 訂單狀態查詢功能 (Order Status Check)
    身為管理者
    我想要查詢訂單的付款狀態
    以便確認交易是否成功

    Scenario: 成功查詢已付款訂單
        Given 系統中存在一筆已付款的訂單 "ORD-2023-001"
        When 我透過 API 查詢該訂單狀態
        Then 回傳結果應顯示狀態為 "Paid"
        And 應包含正確的付款金額
```

## 2. TDD (Unit Test) 撰寫規範

*   測試函式名稱應具備描述性 (Descriptive Naming)。
*   Docstring 應使用 **繁體中文** 說明測試場景，並對應到 BDD 的 Scenario。
*   使用 `pytest` 作為測試框架。
*   使用 `pytest-mock` 或 `unittest.mock` 進行外部依賴隔離。

```python
def test_check_order_status_success():
    """
    場景：成功查詢已付款訂單
    驗證當服務回傳成功訊號時，能夠正確解析並回傳 Response 物件。
    """
    # Arrange (Given)
    ...
    
    # Act (When)
    ...
    
    # Assert (Then)
    ...
```
