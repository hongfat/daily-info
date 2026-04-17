import feedparser
import datetime

# 新聞來源 (維持後端抓取即可)
NEWS_SOURCES = {
    "📈 金融投資 (ETF/台股)": "https://news.google.com/rss/search?q=006208+ETF+台股+股市分析&hl=zh-TW&gl=TW&ceid=TW:zh-Hant",
    "💻 技術開發與趨勢": "https://technews.tw/feed/",
    "📚 圖書館系統與資訊": "https://news.google.com/rss/search?q=Exlibris+Alma+Library+Technology&hl=en-US&gl=US&ceid=US:en"
}

def generate_html():
    tz_offset = datetime.timezone(datetime.timedelta(hours=8))
    now = datetime.datetime.now(tz_offset).strftime("%Y-%m-%d %H:%M")
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>我的即時新知儀表板</title>
        <style>
            body {{ font-family: 'PingFang TC', sans-serif; line-height: 1.6; padding: 20px; max-width: 900px; margin: auto; background: #f0f2f5; color: #1c1e21; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .time {{ color: #65676b; font-size: 0.8em; }}
            .category-section {{ margin-bottom: 30px; }}
            .category-title {{ border-left: 5px solid #1877f2; padding-left: 10px; margin-bottom: 15px; color: #1c1e21; font-size: 1.4em; }}
            .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
            .card {{ background: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
            .mlb-card {{ background: #1a2a44; color: white; border-radius: 10px; padding: 15px; }}
            .mlb-score {{ font-size: 1.2em; font-weight: bold; margin: 5px 0; color: #f1c40f; }}
            .mlb-pitcher {{ font-size: 0.8em; color: #bdc3c7; }}
            .live-dot {{ color: #ff4d4f; font-weight: bold; }}
            a {{ text-decoration: none; color: #1877f2; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚀 即時新知儀表板</h1>
            <p class="time">新聞抓取時間：{now} (台北時間)</p>
        </div>

        <div class="category-section">
            <h2 class="category-title">⚾ MLB 即時戰況 (自動更新)</h2>
            <div id="mlb-container" class="grid">
                <p style="color:#65676b;">正在連線 MLB 官方數據庫...</p>
            </div>
        </div>

        <script>
            // 前端即時抓取 MLB API
            async function updateMLB() {
    try {
        // 加入 hydrate 參數獲取先發投手
        const response = await fetch('https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher');
        const data = await response.json();
        const container = document.getElementById('mlb-container');
        
        if (!data.dates || data.dates.length === 0) {
            container.innerHTML = '<p>今日目前無賽事</p>';
            return;
        }

        const games = data.dates[0].games;
        container.innerHTML = '';

        games.forEach(game => {
            const status = game.status.abstractGameState;
            const awayTeam = game.teams.away.team.name;
            const homeTeam = game.teams.home.team.name;
            const awayScore = game.teams.away.score || 0;
            const homeScore = game.teams.home.score || 0;

            // 讀取 Hydrate 後的投手資料
            // API 路徑通常在 teams.away.probablePitcher.fullName
            const awayP = game.teams.away.probablePitcher ? game.teams.away.probablePitcher.fullName : '未定';
            const homeP = game.teams.home.probablePitcher ? game.teams.home.probablePitcher.fullName : '未定';

            const card = document.createElement('div');
            card.className = 'mlb-card';
            card.innerHTML = `
                <div style="font-size:0.8em">${status === 'Live' ? '<span class="live-dot">● LIVE</span>' : status}</div>
                <div style="font-weight:bold">${awayTeam} vs ${homeTeam}</div>
                <div class="mlb-score">${status === 'Preview' ? '尚未開打' : awayScore + ' - ' + homeScore}</div>
                <div class="mlb-pitcher">
                    P: ${awayP} <br>
                    vs ${homeP}
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('MLB API Error:', error);
    }
}

            // 網頁開啟後執行，且每 60 秒自動更新一次
            updateMLB();
            setInterval(updateMLB, 60000);
        </script>
    """

    # 處理後端新聞 (這部分維持靜態生成，因為新聞不需秒級更新)
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

    html_template += "</body></html>"

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_html()
