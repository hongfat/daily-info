import urllib.request
import json
import datetime

def test_api():
    # 測試獲取今日和明日的日期 (美東時間或台灣時間？)
    # MLB API 的日期通常以美東時間或本地為準。如果我們傳入 startDate 和 endDate 參數會更精確。
    # 讓我們先看看不帶日期參數，只帶 hydrate 的預設回傳。
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&hydrate=probablePitcher,linescore,venue,decisions"
    print("Fetching default url:", url)
    try:
        with urllib.request.urlopen(url) as req:
            data = json.loads(req.read().decode('utf-8'))
            print("Total dates in response:", len(data.get("dates", [])))
            if data.get("dates"):
                date_info = data["dates"][0]
                print("Date in response:", date_info.get("date"))
                games = date_info.get("games", [])
                print("Total games:", len(games))
                if games:
                    game = games[0]
                    print("Game status:", game.get("status"))
                    print("Teams info:", game.get("teams"))
                    print("Decisions (if exists):", game.get("decisions"))
    except Exception as e:
        print("Error:", e)

    # 測試帶有 startDate 和 endDate 的 URL
    # 我們獲取台灣時間的今天和明天
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    url_range = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&startDate={today}&endDate={tomorrow}&hydrate=probablePitcher,linescore,venue,decisions"
    print("\nFetching range url:", url_range)
    try:
        with urllib.request.urlopen(url_range) as req:
            data = json.loads(req.read().decode('utf-8'))
            print("Dates in range response:")
            for d in data.get("dates", []):
                print(f"  Date: {d.get('date')} - Games count: {len(d.get('games', []))}")
                if d.get('games'):
                    for g in d['games'][:2]:
                        print(f"    Game {g.get('gamePk')}: {g.get('teams', {}).get('away', {}).get('team', {}).get('name')} @ {g.get('teams', {}).get('home', {}).get('team', {}).get('name')}")
                        print(f"      Status: {g.get('status', {}).get('abstractGameState')} / {g.get('status', {}).get('detailedState')}")
                        print(f"      Decisions: {g.get('decisions')}")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_api()
