import requests
import json
from datetime import datetime

sources = {
    "FitGirl": "https://hydralinks.cloud/sources/fitgirl.json",
    "SteamRip": "https://hydralinks.cloud/sources/steamrip.json",
    "OnlineFix": "https://hydralinks.cloud/sources/onlinefix.json",
    "Dodi": "https://hydralinks.cloud/sources/dodi.json",
    "ByXatab": "https://hydralinks.cloud/sources/xatab.json",
    "FreeGOG": "https://hydralinks.cloud/sources/gog.json",
    "AtopGames": "https://hydralinks.cloud/sources/atop-games.json",
    "Empress": "https://hydralinks.cloud/sources/empress.json",
    "TinyRepacks": "https://hydralinks.cloud/sources/tinyrepacks.json",
    "KaOsKrew": "https://hydralinks.cloud/sources/kaoskrew.json"
}


mega_lista = {
    "name": "Hydra Global Masters - All-in-One Source",
    "description": f"Updated: {datetime.now().strftime('%Y-%m-%d')}",
    "downloads": []
}

for name, url in sources.items():
    try:
        data = requests.get(url, timeout=30).json()
        games = data.get("downloads", []) or data.get("games", [])
        mega_lista["downloads"].extend(games)
    except:
        pass

with open("Hydra-Global-Masters.json", "w", encoding="utf-8") as f:
    json.dump(mega_lista, f, indent=2, ensure_ascii=False)
