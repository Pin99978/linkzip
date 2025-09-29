# 前端開發計畫

我將使用 React 來開發 LinkZip 的使用者介面。

## 開發步驟

1.  **初始化專案**: 在根目錄建立 `frontend` 資料夾，並使用 `create-react-app` 初始化 React 專案。
2.  **元件設計**: 開發一個核心元件 `URLShortener`，包含：
    *   一個用於輸入原始網址的 `input` 欄位。
    *   一個 `button` 用於提交表單。
    *   一個區域用於顯示後端返回的短網址。
3.  **API 串接**: 撰寫與後端 `/api/urls` 端點互動的邏輯，使用 `fetch` 或 `axios` 來發送 POST 請求。
4.  **樣式設計**: 使用現代 CSS 技術為介面添加簡潔的樣式。

---

# 開發日誌

### **日期: 2025-09-28**

**工作項目：**

1.  **建立 React 專案**
    *   **內容**：在專案根目錄下，使用 `npx create-react-app frontend` 指令成功初始化了前端專案的基本架構。

2.  **完成 MVP 介面開發**
    *   **內容**：修改 `src/App.js` 和 `src/App.css`，實作了一個包含標題、輸入框、提交按鈕和結果顯示區域的單頁應用介面。使用 React `useState` Hook 來管理表單狀態和 API 回應。

3.  **設定開發環境代理 (Proxy)**
    *   **內容**：為了讓前端開發伺服器 (port 3000) 能順利地將 `/api` 請求轉發到後端伺服器 (port 8000)，在 `package.json` 中加入了 `"proxy": "http://127.0.0.1:8000"` 設定。

4.  **除錯重大環境問題：`react-scripts not found`**
    *   **問題**：使用者回報 `npm start` 指令失敗，提示 `react-scripts` 找不到。
    *   **除錯**：經過多次嘗試（包括 `npm install`、清理快取），發現是 `npm` 的依賴樹狀態與 `node_modules` 的實際情況不一致。最終透過**移除 `package.json` 中的依賴，再手動重新安裝 `react`, `react-dom`, `react-scripts`** 的方式，強制 `npm` 重新建立了完整的依賴樹，成功解決了問題。

5.  **除錯次要依賴問題：`web-vitals` 遺失**
    *   **問題**：在修復 `react-scripts` 問題時，因手動重裝依賴，遺漏了 `web-vitals` 這個 `create-react-app` 的預設套件，導致編譯失敗。
    *   **修正**：執行 `npm install web-vitals` 將其補回。

6.  **修正短網址重定向邏輯**
    *   **問題**：使用者回報產生的短網址 `http://localhost:3000/XXXXXX` 無法正確重定向。
    *   **除錯**：意識到這是開發環境下的雙伺服器問題。重定向邏輯存在於後端 (port 8000)，而前端產生的連結指向了前端自身 (port 3000)。
    *   **修正**：修改 `src/App.js` 中的連結產生邏輯，將 `window.location.origin` 硬編碼為後端位址 `http://localhost:8000`，以確保在開發環境下點擊連結能正確命中後端服務。

7.  **UI 重構與功能疊代**
    *   **動機**：根據 PM 需求，擴充 UI 以區分不同類型的縮網址服務，並增加「一鍵複製」功能。
    *   **執行**：
        1.  **元件化**：將 `App.js` 中的表單邏輯，抽離至一個可複用的新元件 `frontend/src/components/ShortenerForm.js`。
        2.  **組裝**：修改 `App.js`，讓它三次渲染 `ShortenerForm` 元件，並傳入不同的 `title` 和 `placeholder`。
        3.  **複製功能**：在 `ShortenerForm.js` 中，使用 `navigator.clipboard.writeText()` API 實現了點擊複製功能，並加入了狀態變化，提供「已複製！」的視覺回饋。

8.  **UI 視覺優化**
    *   **動機**：根據 PM 的設計回饋，優化頁面配色與互動元素。
    *   **執行**：
        1.  **背景色**：修改 `App.css`，為 `body` 增加了深色背景 (`#20232a`)，使整體風格統一。
        2.  **圖示化**：在 `ShortenerForm.js` 中，將「Copy」文字按鈕替換為更直觀的 SVG 圖示，並加入了成功時的「打勾」圖示，提升使用者體驗。

9.  **生產環境 Hotfix**
    *   **問題**：部署到 AWS 後，發現生成的短網址依然是 `http://localhost:8000/...`，導致線上服務不可用。
    *   **除錯**：意識到之前為了解決本地開發問題而做的硬編碼，在生產環境中是錯誤的。
    *   **修正**：修改 `ShortenerForm.js`，將硬編碼的 `http://localhost:8000` 替換為動態的 `window.location.origin`。這確保了無論在哪個環境下，產生的連結主機位址都是正確的。
