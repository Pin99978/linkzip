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
