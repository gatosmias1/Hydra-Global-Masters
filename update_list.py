import requests
import json
from datetime import datetime

# URLs via GitHub em vez de hydralinks.cloud
# hydralinks.cloud bloqueia IPs do GitHub Actions com 403/429
BASE = "https://raw.githubusercontent.com/ArnamentGames/HydraLinks/refs/heads/main"

sources = {
    "FitGirl":     f"{BASE}/fitgirl.json",
    "SteamRip":    f"{BASE}/steamrip.json",
    "OnlineFix":   f"{BASE}/onlinefix.json",
    "Dodi":        f"{BASE}/dodi.json",
    "ByXatab":     f"{BASE}/xatab.json",
    "FreeGOG":     f"{BASE}/gog.json",
    "AtopGames":   f"{BASE}/atop-games.json",
    "Empress":     f"{BASE}/empress.json",
    "TinyRepacks": f"{BASE}/tinyrepacks.json",
    "KaOsKrew":    f"{BASE}/kaoskrew.json",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

mega_lista = {
    "name": "Hydra Global Masters - All-in-One Source",
    "description": f"Updated: {datetime.now().strftime('%Y-%m-%d')}",
    "downloads": []
}

erros = []

for name, url in sources.items():
    try:
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "downloads" in data:
            games = data["downloads"]
        elif "games" in data:
            games = data["games"]
        else:
            msg = f"[AVISO] {name}: chaves desconhecidas -> {list(data.keys())}"
            print(msg)
            erros.append(msg)
            games = []

        print(f"[OK] {name}: {len(games)} jogos")
        mega_lista["downloads"].extend(games)

    except requests.exceptions.Timeout:
        msg = f"[ERRO] {name}: timeout"
        print(msg)
        erros.append(msg)
    except requests.exceptions.HTTPError as e:
        msg = f"[ERRO] {name}: HTTP {e.response.status_code} - {e.response.reason}"
        print(msg)
        erros.append(msg)
    except requests.exceptions.ConnectionError as e:
        msg = f"[ERRO] {name}: falha de conexão - {e}"
        print(msg)
        erros.append(msg)
    except json.JSONDecodeError:
        msg = f"[ERRO] {name}: resposta não é JSON válido"
        print(msg)
        erros.append(msg)
    except Exception as e:
        msg = f"[ERRO] {name}: erro inesperado - {type(e).__name__}: {e}"
        print(msg)
        erros.append(msg)

total = len(mega_lista["downloads"])
print(f"\nTotal: {total} jogos coletados")

if erros:
    print(f"\nFontes com erro ({len(erros)}):")
    for e in erros:
        print(f"  {e}")

if total == 0:
    raise SystemExit("ERRO CRÍTICO: Nenhum jogo coletado. Verifique os erros acima.")

with open("Hydra-Global-Masters.json", "w", encoding="utf-8") as f:
    json.dump(mega_lista, f, indent=2, ensure_ascii=False)

print("Arquivo salvo: Hydra-Global-Masters.json")
