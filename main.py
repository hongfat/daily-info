import feedparser
import datetime

# 新聞來源 (維持後端抓取)
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
            :root {{
                --primary-bg: #f4f7f6;
                --mlb-blue: #1a2a44;
                --accent-yellow: #f1c40f;
                --text-dark: #2c3e50;
                --card-shadow: 0 4px 6px rgba(0,0,0,0.07);
            }}
            body {{ font-family: 'PingFang TC', 'Heiti TC', sans-serif; background-color: var(--primary-bg); color: var(--text-dark); margin: 0; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            
            .header {{ text-align: center; padding: 20px 0; background: white; border-radius: 15px; box-shadow: var(--card-shadow); margin-bottom: 30px; }}
            .header h1 {{ margin: 0; font-size: 1.8em; color: var(--mlb-blue); }}
            .time {{ font-size: 0.85em; color: #7f8c8d; margin-top: 5px; }}

            .section-title {{ border-left: 6px solid var(--mlb-blue); padding-left: 15px; margin: 30px 0 15px; font-size: 1.4em; display: flex; align-items: center; }}
            
            /* MLB 卡片樣式 */
            .mlb-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
            .mlb-card {{ background: linear-gradient(135deg, #1a2a44 0%, #2c3e50 100%); color: white; border-radius: 12px; padding: 20px; box-shadow: 0 6px 12px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.1); }}
            .status-tag {{ font-size: 0.75em; background: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 4px; display: inline-block; margin-bottom: 10px; }}
            .live-dot {{ color: #ff4d4f; animation: blink 1s infinite; }}
            @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} 100% {{ opacity: 1; }} }}
            
            .team-row {{ display: flex; justify-content: space-between; align-items: center; margin: 5px 0; }}
            .team-name {{ font-weight: 600; font-size: 1.1em; }}
            .score {{ font-size: 1.4em; font-weight: 800; color: var(--accent-yellow); }}
            
            .pitcher-info {{ border-top: 1px solid rgba(255,255,255,0.1); margin-top: 15px; padding-top: 10px; font-size: 0.85em; color: #bdc3c7; line-height: 1.4; }}
            .venue {{ font-size: 0.75em; color: #95a5a6; margin-top: 5px; text-align: right; }}

            /* 新聞卡片樣式 */
            .news-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }}
            .news-card {{ background: white; padding: 18px; border-radius: 12px; box-shadow: var(--card-shadow); transition: transform 0.2s; text-decoration: none; color: inherit; display: block; }}
            .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }}
            .news-card b {{ color: #2980b9; font-size: 1.05em; display: block; margin-bottom: 8px; }}
            
            footer {{ text-align: center; padding: 40px 0; color: #95a5a6; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 我的個人新知儀表板</h1>
                <div class="time">新聞更新：{now} | MLB：每 60 秒即時更新</div>
            </div>

            <div class="section-title">⚾ MLB 即時戰報</div>
            <div id="mlb-container" class="mlb-grid">
                <p>正在載入最新球況...</p>
            </div>

            <script>
                async function updateMLB() {{
                    try {{
                        const response = await fetch('https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher,linescore,venue');
                        const data = await response.json();
                        const container = document.getElementById('mlb-container');
                        
                        if (!data.dates || data.dates.length === 0) {{
                            container.innerHTML = '<p style="color:#65676b;">今日暫無比賽</p>';
                            return;
                        }}

                        const games = data.dates[0].games;
                        container.innerHTML = '';

                        games.forEach(game => {{
                            const status = game.status.abstractGameState;
                            const detailStatus = game.status.detailedState;
                            const isLive = status === 'Live';
                            const away = game.teams.away;
                            const home = game.teams.home;
                            const inning = game.linescore ? (game.linescore.inningHalf + ' ' + game.linescore.currentInningOrdinal) : '';
                            
                            const awayP = away.probablePitcher ? away.probablePitcher.fullName : '未定';
                            const homeP = home.probablePitcher ? home.probablePitcher.fullName : '未定';
                            const venue = game.venue.name;

                            const card = document.createElement('div');
                            card.className = 'mlb-card';
                            card.innerHTML = `
                                <div class="status-tag">
                                    ${{isLive ? '<span class="live-dot">● </span>' + inning : detailStatus}}
                                </div>
                                <div class="team-row">
                                    <span class="team-name">${{away.team.name}}</span>
                                    <span class="score">${{status === 'Preview' ? '-' : (away.score || 0)}}</span>
                                </div>
                                <div class="team-row">
                                    <span class="team-name">${{home.team.name}}</span>
                                    <span class="score">${{status === 'Preview' ? '-' : (home.score || 0)}}</span>
                                </div>
                                <div class="pitcher-info">
                                    P: ${{awayP}} (客) <br>
                                    P: ${{homeP}} (主)
                                </div>
                                <div class="venue">📍 ${{venue}}</div>
                            `;
                            container.appendChild(card);
                        }});
                    }} catch (e) {{ console.error(e); }}
                }}
                updateMLB();
                setInterval(updateMLB, 60000);
            </script>
    """

    for category, url in NEWS_SOURCES.items():
        feed = feedparser.parse(url)
        html_template += f"""
            <div class="section-title">{category}</div>
            <div class="news-grid">
        """
        for entry in feed.entries[:6]:
            html_template += f"""
                <a href="{entry.link}" target="_blank" class="news-card">
                    <b>{entry.title}</b>
                </a>
            """
        html_template += "</div>"

    html_template += """
            <footer>Powered by GitHub Actions & MLB Stats API</footer>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    generate_html()
