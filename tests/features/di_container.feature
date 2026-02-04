# language: zh-TW
功能: 依賴注入容器
  作為開發者
  我希望使用依賴注入容器管理服務依賴
  以便介面層不需要手動建立 Repository

  場景: 透過 Container 取得 ChargeStatusService
    假設 DI Container 已初始化
    當 我從 Container 請求 ChargeStatusService
    那麼 我應該取得一個可用的服務實例
    而且 該服務應該已注入 OrderRepository

  場景: Container 提供正確的資料庫連線
    假設 DI Container 已初始化
    當 我從 Container 請求 db_session
    那麼 我應該取得一個有效的 AsyncSession

  場景: CLI Command 透過 Container 執行訂單反查
    假設 DI Container 已初始化
    當 我執行 charge-status 指令並傳入訂單編號 "TEST-001"
    那麼 服務應該被正確注入並執行
