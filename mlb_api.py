"""
Funciones para consultar el Stats API público de la MLB.
No requiere API key. Base: https://statsapi.mlb.com/api/v1
"""
import requests

BASE_URL = "https://statsapi.mlb.com/api/v1"


def get_team_id(team_name):
    """Busca el ID de un equipo por nombre (ej. 'Yankees', 'Dodgers')."""
    resp = requests.get(f"{BASE_URL}/teams", params={"sportId": 1}, timeout=10)
    resp.raise_for_status()
    teams = resp.json().get("teams", [])
    for t in teams:
        if team_name.lower() in t["name"].lower():
            return t["id"]
    return None


def get_team_runs_per_game(team_id, season):
    """Promedio de carreras anotadas por partido en la temporada dada."""
    resp = requests.get(
        f"{BASE_URL}/teams/{team_id}/stats",
        params={"stats": "season", "group": "hitting", "season": season},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    try:
        stat = data["stats"][0]["splits"][0]["stat"]
        runs = float(stat["runs"])
        games = float(stat["gamesPlayed"])
        return round(runs / games, 2) if games else None
    except (KeyError, IndexError):
        return None


def get_pitcher_id(full_name):
    """Busca el ID de un jugador/pitcher por nombre completo."""
    resp = requests.get(
        f"{BASE_URL}/sports/1/players",
        timeout=10,
    )
    resp.raise_for_status()
    people = resp.json().get("people", [])
    for p in people:
        if full_name.lower() in p.get("fullName", "").lower():
            return p["id"]
    return None


def get_pitcher_era(player_id, season):
    """ERA de un pitcher en la temporada dada."""
    resp = requests.get(
        f"{BASE_URL}/people/{player_id}/stats",
        params={"stats": "season", "group": "pitching", "season": season},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    try:
        stat = data["stats"][0]["splits"][0]["stat"]
        return float(stat["era"])
    except (KeyError, IndexError):
        return None


def get_todays_schedule(date_str=None):
    """Calendario de partidos de un día (formato YYYY-MM-DD). Sin fecha, usa hoy."""
    params = {"sportId": 1}
    if date_str:
        params["date"] = date_str
    resp = requests.get(f"{BASE_URL}/schedule", params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()
