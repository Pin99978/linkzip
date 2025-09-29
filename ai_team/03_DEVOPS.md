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

---

**工作項目 (架構升級)：**

1.  **引入 Docker Compose 管理多容器應用**
    *   **動機**：為了模擬真實生產環境，我們需要同時管理後端應用和一個獨立的資料庫服務。
    *   **執行**：撰寫 `docker-compose.yml` 檔案，在其中定義了 `backend` 和 `db` 兩個服務。

2.  **透過 Docker Compose 管理 PostgreSQL**
    *   **「安裝」方式**：我們沒有在主機上安裝 PostgreSQL，而是在 `docker-compose.yml` 中指定 `image: postgres:13`。這會讓 Docker 自動從 Docker Hub 下載官方的 PostgreSQL 映像檔並作為一個容器運行。
    *   **環境設定**：透過 `environment` 關鍵字，我們在啟動容器時向其內部傳入 `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` 等環境變數，用以在容器首次啟動時自動初始化資料庫。
    *   **資料持久化**：這是最關鍵的一步。我們設定了 `volumes: - postgres_data:/var/lib/postgresql/data/`。這會將容器內 PostgreSQL 存放資料的目錄，映射到一個由 Docker 管理的、在主機上的具名磁碟區 `postgres_data`。這樣做可以確保即使我們用 `docker-compose down` 關閉並移除了容器，資料庫的數據依然會被保留下來，下次啟動時能無縫接軌。

3.  **解決服務啟動的「競態條件」問題**
    *   **問題**：`docker-compose up` 啟動時，後端應用 (`backend`) 崩潰，日誌顯示 `connection refused`。
    *   **診斷**：這是一個典型的競態條件。`depends_on` 只保證了 `db` 容器比 `backend` 容器先**啟動**，但無法保證 `db` 容器內的 PostgreSQL 服務已經**準備好接受連線**。我們的後端應用啟動太快，在資料庫準備好之前就嘗試連線，因此被拒絕。
    *   **解決方案 (標準流程)**：引入一個健康檢查腳本 `wait-for-it.sh`。
        1.  **下載腳本**：將 `wait-for-it.sh` 腳本儲存到專案根目錄。
        2.  **修改 Dockerfile**：將該腳本複製到映像檔中，並賦予其執行權限 (`RUN chmod +x wait-for-it.sh`)。
        3.  **修改 docker-compose.yml**：修改 `backend` 服務的 `command`，讓它在啟動 `uvicorn` 之前，先執行 `./wait-for-it.sh db:5432 -- ...`。這個指令會持續檢查 `db` 服務的 `5432` 埠是否可以連線，直到成功後，才會執行 `--` 後面的主程式。這確保了我們的應用在啟動時，資料庫絕對是可用的。
