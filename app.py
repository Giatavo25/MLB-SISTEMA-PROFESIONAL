from flask import Flask, render_template, request, jsonify
from mlb_api import get_team_id, get_team_runs_per_game, get_todays_schedule
from calculations import (
    combined_over_under,
    team_over_under,
    american_to_implied,
    remove_vig,
    edge,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/team_runs")
def team_runs():
    team_name = request.args.get("team", "")
    season = request.args.get("season", "2026")
    team_id = get_team_id(team_name)
    if not team_id:
        return jsonify({"error": "Equipo no encontrado"}), 404
    runs_per_game = get_team_runs_per_game(team_id, season)
    return jsonify({"team_id": team_id, "runs_per_game": runs_per_game})


@app.route("/api/schedule")
def schedule():
    date_str = request.args.get("date")
    data = get_todays_schedule(date_str)
    games = []
    for day in data.get("dates", []):
        for g in day.get("games", []):
            games.append(
                {
                    "gamePk": g["gamePk"],
                    "home": g["teams"]["home"]["team"]["name"],
                    "away": g["teams"]["away"]["team"]["name"],
                    "status": g["status"]["detailedState"],
                }
            )
    return jsonify(games)


@app.route("/api/moneyline")
def moneyline():
    odds_a = request.args.get("odds_a", type=float)
    odds_b = request.args.get("odds_b", type=float)
    if odds_a is None or odds_b is None:
        return jsonify({"error": "Faltan odds_a u odds_b"}), 400
    imp_a = american_to_implied(odds_a)
    imp_b = american_to_implied(odds_b)
    fair_a, fair_b = remove_vig(imp_a, imp_b)
    return jsonify(
        {
            "implied_a": round(imp_a, 4),
            "implied_b": round(imp_b, 4),
            "fair_a": round(fair_a, 4),
            "fair_b": round(fair_b, 4),
            "vig": round((imp_a + imp_b - 1) * 100, 2),
        }
    )


@app.route("/api/value")
def value():
    my_prob = request.args.get("my_prob", type=float)
    fair_prob = request.args.get("fair_prob", type=float)
    if my_prob is None or fair_prob is None:
        return jsonify({"error": "Faltan my_prob o fair_prob"}), 400
    return jsonify({"edge_pts": edge(my_prob, fair_prob)})


@app.route("/api/total")
def total():
    lam_h = request.args.get("lam_h", type=float)
    lam_a = request.args.get("lam_a", type=float)
    line = request.args.get("line", type=float)
    if lam_h is None or lam_a is None or line is None:
        return jsonify({"error": "Faltan lam_h, lam_a o line"}), 400
    result = combined_over_under(lam_h, lam_a, line)
    return jsonify(result)


@app.route("/api/team_total")
def team_total():
    lam = request.args.get("lam", type=float)
    line = request.args.get("line", type=float)
    if lam is None or line is None:
        return jsonify({"error": "Faltan lam o line"}), 400
    return jsonify(team_over_under(lam, line))


if __name__ == "__main__":
    app.run(debug=True)
