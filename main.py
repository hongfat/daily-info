import feedparser
import datetime

# 1. 定義分類與來源 (你可以隨時修改關鍵字)
NEWS_SOURCES = {
    "⚾ 棒球賽況與新聞": "https://news.google.com/rss/search?q=中職+MLB+棒球+賽程&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "📈 金融投資 (ETF/台股)": "https://news.google.com/rss/search?q=006208+ETF+台股+股市分析&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "💻 技術開發與趨勢": "https://technews.tw/feed/",
    "📚 圖書館系統與資訊": "https://news.google.com/rss/search?q=Exlibris+Alma+Library+Technology&hl=en-US&gl=US&ceid=US:en"
}

def generate_html():
    # 獲取目前的 UTC 時間，並加上 8 小時轉換為台灣時間
    tz_offset = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz_offset).strftime("%Y-%m-%d %H:%M")
    # -----------------------
    
    # HTML 標頭與樣式
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>我的每日新知儀表板</title>
        <style>
            body {{ font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif; line-height: 1.6; padding: 20px; max-width: 900px; margin: auto; background: #f0f2f5; color: #1c1e21; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .time {{ color: #65676b; font-size: 0.9em; }}
            .category-section {{ margin-bottom: 30px; }}
            .category-title {{ border-left: 5px solid #1877f2; padding-left: 10px; margin-bottom: 15px; color: #1c1e21; font-size: 1.4em; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
            .card {{ background: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: transform 0.2s; }}
            .card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }}
            .card a {{ text-decoration: none; color: #1877f2; font-weight: bold; font-size: 1.1em; display: block; }}
            .card .source {{ color: #65676b; font-size: 0.85em; margin-top: 8px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗓️ 每日新知儀表板</h1>
            <p class="time">更新於：{now} (每日自動更新)</p>
        </div>
    """

    # 循環處理每個類別
    for category, url in NEWS_SOURCES.items():
        feed = feedparser.parse(url)
        html_template += f"""
        <div class="category-section">
            <h2 class="category-title">{category}</h2>
            <div class="grid">
        """
        
        # 每個分類抓取前 5 則新聞
        for entry in feed.entries[:5]:
            # 嘗試取得來源名稱 (Google News RSS 格式通常在標題最後面)
            title = entry.title
            html_template += f"""
            <div class="card">
                <a href="{entry.link}" target="_blank">{title}</a>
                <div class="source">發布時間: {entry.published if 'published' in entry else 'N/A'}</div>
            </div>
            """
        
        html_template += "</div></div>"

    html_template += """
        <div style="text-align: center; margin-top: 50px; padding: 20px; color: #90949c; font-size: 0.8em;">
            Built with GitHub Actions & Python
        </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_html()
