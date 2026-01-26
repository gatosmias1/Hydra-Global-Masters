import requests
import json
from datetime import datetime

sources = {
    "FitGirl": "https://hydralinks.pages.dev/sources/fitgirl.json",
    "SteamRip": "https://hydralinks.pages.dev/sources/steamrip.json",
    "OnlineFix": "https://hydralinks.pages.dev/sources/onlinefix.json",
    "Dodi": "https://hydralinks.pages.dev/sources/dodi.json",
    "ByXatab": "https://hydralinks.pages.dev/sources/xatab.json",
    "FreeGOG": "https://hydralinks.pages.dev/sources/gog.json",
    "AtopGames": "https://hydralinks.pages.dev/sources/atop-games.json",
    "Empress": "https://hydralinks.pages.dev/sources/empress.json",
    "TinyRepacks": "https://hydralinks.pages.dev/sources/tinyrepacks.json",
    "KaOsKrew": "https://hydralinks.pages.dev/sources/kaoskrew.json"
}

mega_lista = {
    "name": "Hydra Global Masters - All-in-One Source",
    "description": f"Hub for FitGirl, Dodi, SteamRip and more. Updated: {datetime.now().strftime('%Y-%m-%d')}",
    "downloads": []
}

for name, url in sources.items():
    try:
        data = requests.get(url, timeout=15).json()
        games = data.get("downloads", []) or data.get("games", [])
        mega_lista["downloads"].extend(games)
        print(f"✅ {name} added!")
    except:
        print(f"❌ Error on {name}")

with open("mega_fontes.json", "w", encoding="utf-8") as f:
    json.dump(mega_lista, f, indent=2, ensure_ascii=False)
