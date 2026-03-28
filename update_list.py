import requests
import json
from datetime import datetime

sources = {
    "FitGirl":     "https://hydralinks.cloud/sources/fitgirl.json",
    "SteamRip":    "https://hydralinks.cloud/sources/steamrip.json",
    "OnlineFix":   "https://hydralinks.cloud/sources/onlinefix.json",
    "Dodi":        "https://hydralinks.cloud/sources/dodi.json",
    "ByXatab":     "https://hydralinks.cloud/sources/xatab.json",
    "FreeGOG":     "https://hydralinks.cloud/sources/gog.json",
    "AtopGames":   "https://hydralinks.cloud/sources/atop-games.json",
    "Empress":     "https://hydralinks.cloud/sources/empress.json",
    "TinyRepacks": "https://hydralinks.cloud/sources/tinyrepacks.json",
    "KaOsKrew":    "https://hydralinks.cloud/sources/kaoskrew.json"
}

mega_lista = {
    "name": "Hydra Global Masters - All-in-One Source",
    "description": f"Updated: {datetime.now().strftime('%Y-%m-%d')}",
    "downloads": []
}

for name, url in sources.items():
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # lança erro se status != 200
        data = response.json()

        # Pega "downloads" ou "games", sem usar `or` perigoso
        if "downloads" in data:
            games = data["downloads"]
        elif "games" in data:
            games = data["games"]
        else:
            print(f"[AVISO] {name}: nenhuma chave conhecida encontrada. Keys: {list(data.keys())}")
            games = []

        print(f"[OK] {name}: {len(games)} jogos adicionados")
        mega_lista["downloads"].extend(games)

    except requests.exceptions.Timeout:
        print(f"[ERRO] {name}: timeout ao conectar")
    except requests.exceptions.HTTPError as e:
        print(f"[ERRO] {name}: HTTP {e.response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[ERRO] {name}: falha de conexão")
    except json.JSONDecodeError:
        print(f"[ERRO] {name}: resposta não é um JSON válido")
    except Exception as e:
        print(f"[ERRO] {name}: erro inesperado - {e}")

total = len(mega_lista["downloads"])
print(f"\nTotal: {total} jogos coletados")

with open("Hydra-Global-Masters.json", "w", encoding="utf-8") as f:
    json.dump(mega_lista, f, indent=2, ensure_ascii=False)

print("Arquivo salvo: Hydra-Global-Masters.json")
