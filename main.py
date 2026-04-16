import feedparser
import datetime
import requests

# 1. 原始新聞來源定義
NEWS_SOURCES = {
    "📈 金融投資 (ETF/台股)": "https://news.google.com/rss/search?q=006208+ETF+台股+股市分析&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "💻 技術開發與趨勢": "https://technews.tw/feed/",
    "📚 圖書館系統與資訊": "https://news.google.com/rss/search?q=Exlibris+Alma+Library+Technology&hl=en-US&gl=US&ceid=US:en"
}

# 2. 獲取 MLB 資料的函式
def get_mlb_games():
    # 使用 MLB 官方 API 獲取今日賽事
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        games_list = data.get('dates', [{}])[0].get('games', [])
        
        mlb_results = []
        for game in games_list:
            # 隊伍名稱
            away_team = game['teams']['away']['team']['name']
            home_team = game['teams']['home']['team']['name']
            
            # 比分 (如果還沒開打會是 None)
            away_score = game['teams']['away'].get('score', 0)
            home_score = game['teams']['home'].get('score', 0)
            
            # 狀態 (例如: Final, Live, Preview)
            status = game['status']['abstractGameState']
            
            # 先發投手 (Probable Pitchers)
            away_p = game['teams']['away'].get('probablePitcher', {}).get('name', '未定')
            home_p = game['teams']['home'].get('probablePitcher', {}).get('name', '未定')
            
            mlb_results.append({
                "matchup": f"{away_team} vs {home_team}",
                "score": f"{away_score} - {home_score}" if status != "Preview" else "尚未開打",
                "pitchers": f"先發：{away_p} (客) vs {home_p} (主)",
                "status": status
            })
        return mlb_results
    except Exception as e:
        print(f"MLB API Error: {e}")
        return []

def generate_html():
    # 設定台北時區
    tz_offset = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz_offset).strftime("%Y-%m-%d %H:%M")
    
    mlb_games = get_mlb_games()
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>我的每日新知儀表板</title>
        <style>
            body {{ font-family: 'PingFang TC', sans-serif; line-height: 1.6; padding: 20px; max-width: 900px; margin: auto; background: #f0f2f5; color: #1c1e21; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .time {{ color: #65676b; font-size: 0.9em; }}
            .category-section {{ margin-bottom: 30px; }}
            .category-title {{ border-left: 5px solid #1877f2; padding-left: 10px; margin-bottom: 15px; color: #1c1e21; font-size: 1.4em; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
            .card {{ background: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .mlb-card {{ background: #1a2a44; color: white; border-radius: 10px; padding: 15px; margin-bottom: 10px; }}
            .mlb-card b {{ color: #f1c40f; }}
            .mlb-score {{ font-size: 1.2em; font-weight: bold; margin: 5px 0; }}
            .mlb-pitcher {{ font-size: 0.85em; color: #bdc3c7; }}
            .card a {{ text-decoration: none; color: #1877f2; font-weight: bold; }}
            .source {{ color: #65676b; font-size: 0.85em; margin-top: 8px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🗓️ 每日新知儀表板</h1>
            <p class="time">最後更新時間：{now} (台北時間)</p>
        </div>

        <div class="category-section">
            <h2 class="category-title">⚾ MLB 今日戰況</h2>
            <div class="grid">
    """

    for game in mlb_games:
        status_label = "🔴 LIVE" if game['status'] == "Live" else game['status']
        html_template += f"""
        <div class="mlb-card">
            <div><small>{status_label}</small></div>
            <div class="mlb-matchup">{game['matchup']}</div>
            <div class="mlb-score">{game['score']}</div>
            <div class="mlb-pitcher">{game['pitchers']}</div>
        </div>
        """

    if not mlb_games:
        html_template += "<p>今日尚無賽事資訊</p>"

    html_template += "</div></div>"

    # 新聞區塊
    for category, url in NEWS_SOURCES.items():
        feed = feedparser.parse(url)
        html_template += f"""
        <div class="category-section">
            <h2 class="category-title">{category}</h2>
            <div class="grid">
        """
        for entry in feed.entries[:5]:
            html_template += f"""
            <div class="card">
                <a href="{entry.link}" target="_blank">{entry.title}</a>
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
