# MVP 技術設計藍圖

遵照指示，以下是後端 MVP 的技術設計。

## 1. `urls` 資料表 SQLAlchemy 模型

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

## 2. FastAPI 核心 API 端點

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class URLBase(BaseModel):
    original_url: str

# 1. 建立短網址
@app.post("/api/urls", response_model=URLBase)
async def create_short_url(url: URLBase):
    ...

# 2. 重定向到原始網址
@app.get("/{short_key}")
async def redirect_to_original_url(short_key: str):
    ...
```
---
老闆，以上是您需要的設計藍圖。我會開始在 `src/main.py` 中實作這些功能。

---

# 開發日誌

### **日期: 2025-09-28**

**工作項目：**

1.  **完成 `src/main.py` MVP 實作**
    *   **內容**：根據設計藍圖，使用 FastAPI、SQLAlchemy (搭配 SQLite) 完整實作了 API 的所有功能，包括資料庫模型的建立、Pydantic 模型的定義，以及三個核心 API 端點 (`/api/urls`, `/{short_key}`, `/api/info/{short_key}`) 的邏輯。
    *   **決策**：選擇了 SQLite 作為 MVP 的資料庫，以求快速啟動和簡化設定。

2.  **修正重大 Bug：依賴注入錯誤**
    *   **問題**：測試時發現 `TypeError: cannot pickle 'module' object` 錯誤，導致服務器在處理 `favicon.ico` 等請求時崩潰。
    *   **除錯**：根本原因在於使用了 `db=next(get_db())` 的錯誤寫法，導致所有請求共用一個已關閉的資料庫 session。
    *   **修正**：將所有端點的資料庫依賴修改為 FastAPI 正確的 `db: Session = Depends(get_db)` 寫法，確保每個請求都有獨立的 session。

3.  **程式碼品質提升：處理棄用警告**
    *   **內容**：修正了 `pytest` 報告的三個主要棄用警告：
        1.  將 SQLAlchemy 的 `declarative_base` import 路徑更新至 `sqlalchemy.orm`。
        2.  將 Pydantic 的 `class Config` 語法更新為 V2 的 `model_config = ConfigDict(...)`。
        3.  將已棄用的 `datetime.utcnow` 更新為 Python 3.12+ 推薦的 `datetime.now(UTC)`。
    *   **目的**：確保專案的長期可維護性和技術現代性。

4.  **整合前端：提供靜態檔案服務**
    *   **內容**：在 `main.py` 中匯入 `StaticFiles`，並在所有 API 路由之後，使用 `app.mount("/", ...)` 將 `frontend/build` 目錄掛載到根路徑。
    *   **目的**：實現單一伺服器模式，簡化部署和測試流程，讓使用者只需訪問後端埠即可獲得完整應用體驗。

5.  **架構升級：遷移至 PostgreSQL**
    *   **動機**：為了讓專案更接近生產環境，我們需要從檔案型的 SQLite 遷移到更強大的主從式資料庫 PostgreSQL。
    *   **為什麼是 PostgreSQL?**：相較於 SQLite，PostgreSQL 是一個獨立運行的服務。它天生就為處理大量「同時」的讀寫請求而設計，提供了更強的效能、穩定性和資料一致性保障，是真實線上服務的首選。
    *   **執行**：
        1.  在 `requirements.txt` 中加入 `psycopg2-binary` 這個 PostgreSQL 驅動程式。
        2.  修改 `src/main.py`，讓資料庫連接字串 `DATABASE_URL` 從環境變數中讀取，如果讀取不到，則退回使用本地的 SQLite。這讓我們的程式碼在開發和生產環境中都能靈活運作。
