Feature: 訂單付款狀態查詢
  身為一個管理者
  我想要查詢訂單的付款狀態
  以便確認付款是否成功

  Scenario: 成功查詢 ICP 訂單狀態
    Given 存在一筆訂單 ID 為 "ORD-2023-001" 且付款方式為 "ICP"
    And 外部 ICP 服務回傳 "TradeStatus: 1" (成功)
    When 我查詢 "ORD-2023-001" 的 "ICP" 付款狀態
    Then 結果應為包含 "TradeStatus": 1 的成功 JSON 回應

  Scenario: 成功查詢 OP 訂單狀態
    Given 存在一筆訂單 ID 為 "ORD-2023-002" 且付款方式為 "OP"
    And 外部 OP 服務回傳 "1|OK"
    When 我查詢 "ORD-2023-002" 的 "OP" 付款狀態
    Then 結果應為 "1|OK"

  Scenario: 查無訂單
    Given 不存在 ID 為 "ORD-NON-EXISTENT" 的訂單
    When 我查詢 "ORD-NON-EXISTENT" 的 "OP" 付款狀態
    Then 結果應顯示失敗或 "False"

  Scenario: 外部服務失敗 (Timeout)
    Given 存在一筆訂單 ID 為 "ORD-2023-003" 且付款方式為 "ICP"
    And 外部 ICP 服務逾時
    When 我查詢 "ORD-2023-003" 的 "ICP" 付款狀態
    Then 結果應顯示錯誤
