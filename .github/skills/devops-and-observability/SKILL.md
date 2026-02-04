---
name: devops-and-observability
description: CI/CD pipeline standards, GCP deployment, and centralized logging.
---

# DevOps & Observability Standards

## 1. CI Pipeline (Automated Checks)
- **Static Analysis**: 每次 Commit 必須通過 `ruff check` 與 `mypy`。
- **Automated Testing**: PR 合併前必須通過 100% 的測試案例。
- **Security**: 使用 `bandit` 掃描潛在安全性漏洞。

## 2. CD & Deployment (GCP)
- **Containerization**: 使用 Docker 分層構建（Multi-stage builds）優化映像檔大小。
- **Infrastructure**: 使用 Cloud Run 部署 API，設定適當的 CPU 與 Memory 限制。
- **Environment**: 嚴格區分 `dev`, `staging`, `prod` 環境。

## 3. Observability
- **Structured Logging**: 統一使用 JSON 格式輸出日誌，包含 `trace_id` 以追蹤請求。
- **Monitoring**: 關鍵業務邏輯需埋設 Google Cloud Monitoring 自定義指標。