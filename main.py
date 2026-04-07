import feedparser
import datetime

# 1. 設定新聞來源 (RSS)
# 這裡抓取「台灣科技」與「運動」關鍵字的新聞
RSS_URL = "https://news.google.com/rss/search?q=科技+運動&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"

def generate_html():
    feed = feedparser.parse(RSS_URL)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 2. 開始組合 HTML 內容
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>我的每日新知</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; max-width: 800px; margin: auto; background: #f9f9f9; }}
            .card {{ background: white; padding: 15px; margin-bottom: 10px; border-radius: 8px; shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            a {{ text-decoration: none; color: #007bff; font-weight: bold; }}
            .time {{ color: #666; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <h1>📅 每日新知摘要</h1>
        <p class="time">最後更新時間：{now}</p>
        <hr>
    """

    # 3. 抓取前 15 則新聞
    for entry in feed.entries[:15]:
        html_template += f"""
        <div class="card">
            <a href="{entry.link}" target="_blank">{entry.title}</a>
        </div>
        """

    html_template += "</body></html>"

    # 4. 將結果儲存為 index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_html()
