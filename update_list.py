import json
from datetime import datetime, timezone
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE = "https://raw.githubusercontent.com/ArnamentGames/HydraLinks/main"

SOURCES = {
    "FitGirl": f"{BASE}/fitgirl.json",
    "SteamRip": f"{BASE}/steamrip.json",
    "OnlineFix": f"{BASE}/onlinefix.json",
    "Dodi": f"{BASE}/dodi.json",
    "ByXatab": f"{BASE}/xatab.json",
    "FreeGOG": f"{BASE}/gog.json",
    "AtopGames": f"{BASE}/atop-games.json",
    "Empress": f"{BASE}/empress.json",
    "TinyRepacks": f"{BASE}/tinyrepacks.json",
    "KaOsKrew": f"{BASE}/kaoskrew.json",
}

HEADERS = {"User-Agent": "Mozilla/5.0"}


def build_session() -> requests.Session:
    retry = Retry(
        total=6,
        connect=6,
        read=6,
        status=6,
        backoff_factor=1.2,
        status_forcelist=(403, 408, 425, 429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
    s = requests.Session()
    s.headers.update(HEADERS)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def extract_games(source_name: str, data: dict) -> list[dict]:
    if isinstance(data, dict) and isinstance(data.get("downloads"), list):
        return data["downloads"]
    if isinstance(data, dict) and isinstance(data.get("games"), list):
        return data["games"]
    raise KeyError(f"{source_name}: formato inesperado")


def normalize_item(item: dict) -> dict:
    title = item.get("title")
    uris = item.get("uris")
    upload_date = item.get("uploadDate")
    file_size = item.get("fileSize")

    if not isinstance(title, str) or not title.strip():
        raise ValueError("title inválido")
    if not isinstance(uris, list) or not uris or not all(isinstance(u, str) and u.strip() for u in uris):
        raise ValueError("uris inválido")

    out = {
        "title": title.strip(),
        "uris": [u.strip() for u in uris if u.strip()],
        "uploadDate": upload_date,
        "fileSize": file_size,
    }
    return out


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for it in items:
        key = (it.get("title"), tuple(sorted(it.get("uris", []))))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    out.sort(key=lambda x: (str(x.get("title", "")).casefold(), str(x.get("uploadDate", ""))))
    return out


def main() -> None:
    session = build_session()
    collected: list[dict] = []
    errors: list[str] = []

    for name, url in SOURCES.items():
        try:
            r = session.get(url, timeout=40)
            if r.status_code >= 400:
                raise requests.HTTPError(f"HTTP {r.status_code}")
            data = r.json()
            games = extract_games(name, data)
            ok = 0
            for g in games:
                if not isinstance(g, dict):
                    continue
                try:
                    collected.append(normalize_item(g))
                    ok += 1
                except Exception:
                    continue
            print(f"[OK] {name}: {ok} jogos")
        except Exception as e:
            msg = f"[ERRO] {name}: {type(e).__name__}: {e}"
            print(msg)
            errors.append(msg)

    collected = dedupe(collected)

    out = {
        "name": "Hydra Global Masters - All-in-One Source",
        "description": f"Updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d')} (UTC)",
        "downloads": collected,
    }

    total = len(out["downloads"])
    print(f"\nTotal: {total} jogos (após deduplicação)")

    if errors:
        print(f"\nFontes com erro ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    if total == 0:
        raise SystemExit("ERRO CRÍTICO: Nenhum jogo coletado.")

    output_path = Path(__file__).with_name("Hydra-Global-Masters.json")
    output_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Arquivo salvo: {output_path.name}")


if __name__ == "__main__":
    main()
