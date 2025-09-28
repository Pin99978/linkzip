# DevOps 工作日誌

### **日期: 2025-09-28**

**工作項目 (歷史補登)：**

1.  **建立後端依賴清單 (`requirements.txt`)**
    *   **內容**：使用 `pip freeze` 指令，篩選出專案核心依賴 (fastapi, uvicorn, sqlalchemy 等)，並將其導出至 `requirements.txt`。
    *   **目的**：為 Docker 映像的建立和標準化部署提供一個明確的依賴清單。

2.  **建立 `.dockerignore` 檔案**
    *   **內容**：撰寫 `.dockerignore` 檔案，排除 `venv`, `__pycache__`, `.git` 等不需要被複製到 Docker 映像中的檔案和目錄。
    *   **目的**：保持最終映像檔的輕量與乾淨，並加快建置速度。

3.  **撰寫 `Dockerfile`**
    *   **內容**：為後端 FastAPI 應用編寫了 `Dockerfile`，定義了從基礎映像、安裝依賴、複製程式碼到啟動服務的完整流程。

4.  **除錯 Docker 建置問題**
    *   **問題 1**：`docker build` 失敗，提示 `python:3.12-slim-buster: not found`。
    *   **修正 1**：意識到基礎映像標籤錯誤，將其修正為更標準的 `python:3.12-slim`。
    *   **問題 2**：建置過程中出現 `LegacyKeyValueFormat` 警告。
    *   **修正 2**：將 `Dockerfile` 中的 `ENV KEY VALUE` 語法更新為現代的 `ENV KEY=VALUE` 格式，消除警告，提升程式碼品質。

---

**工作項目 (新功能疊代)：**

1.  **建置更新後的前端應用**
    *   **內容**：在前端工程師完成 UI 重構和新功能開發後，執行 `npm run build` 指令。
    *   **目的**：產生包含了新介面和「一鍵複製」功能的生產級別靜態檔案，以便後端伺服器能夠提供最新的版本給使用者。
