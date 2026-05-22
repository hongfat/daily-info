# Daily Info

每日資訊摘要是一個自動化的排程腳本，它會每天自動抓取網路上的熱門新聞，包含科技、財經、綜合三大領域，並生成一份結構化的每日摘要。使用者可以透過定時執行 (cron job) 或手動執行的方式來獲取最新的資訊摘要。

## 功能

- **自動化資訊抓取**：每日固定時間抓取網路新聞。
- **多元資訊來源**：涵蓋科技、財經、綜合三大領域。
- **結構化摘要輸出**：生成的摘要包含日期、領域分類及新聞標題。
- **多種輸出格式**：支援 Markdown (`md`) 和純文字 (`txt`) 格式。
- **可透過 Line Notify 分享**：可選填功能，將摘要透過 Line Notify 推送到指定群組或個人。

## 安裝與設定

### 前置需求

- Python 3.6 或以上版本
- 必要的套件：`requests`, `feedparser`

### 設定步驟

1. **取得 Python 依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定 Line Notify (選填)**
   - 登入 Line Notify 官方網站。
   - 取得您的 Line Notify Token。
   - 在 `.env` 檔案中設定 `LINE_NOTIFY_TOKEN`。

3. **設定環境變數**
   創建 `.env` 檔案（若無）並加入以下變數：
   ```env
   LINE_NOTIFY_TOKEN=YOUR_LINE_NOTIFY_TOKEN_HERE
   ```

## 使用方法

### 手動執行

```bash
python main.py --start-date "2023-01-01" --end-date "2023-01-01"
```

**參數說明：**

- `--start-date`: 開始日期（格式：YYYY-MM-DD）。預設為當日。
- `--end-date`: 結束日期（格式：YYYY-MM-DD）。預設為當日。
- `--format`: 輸出格式。可選 `md` (Markdown) 或 `txt` (Text)。預設為 `md`。
- `--line`: 是否使用 Line Notify 傳送。`true` 或 `false`。預設為 `false`。
- `--output-dir`: 輸出目錄。預設為 `./output`。

### 定時執行 (Cron Job)

您可以使用 `cron` (Linux/Mac) 或 `Task Scheduler` (Windows) 來設定每日自動執行。

**Linux/Mac Cron 範例：**

將以下內容加入您的 Crontab (例如，每天早上 8 點執行)：

```cron
0 8 * * * /usr/bin/python3 /path/to/your/project/daily-info/main.py --line true
```

> 請確保使用 Python 的絕對路徑以及專案的絕對路徑。
