import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/club")
def club():
    return render_template("club.html")

@main.route("/horaires")
def horaires():
    return render_template("horaires.html")

@main.route("/calendrier-competitions")
def calendrier_competitions():
    return render_template("calendrier_competitions.html")

@main.route("/calendrier-competitions/adultes")
def competitions_adultes():
    return render_template("competitions_adultes.html")

@main.route("/calendrier-competitions/adultes/equipe-1")
def equipe_1():
    return render_template("equipe_1.html")

@main.route("/calendrier-competitions/adultes/equipe-2")
def equipe_2():
    return render_template("equipe_2.html")

@main.route("/calendrier-competitions/adultes/equipe-3")
def equipe_3():
    return render_template("equipe_3.html")

@main.route("/calendrier-competitions/adultes/equipe-4")
def equipe_4():
    return render_template("equipe_4.html")

@main.route("/calendrier-competitions/adultes/equipe-5")
def equipe_5():
    return render_template("equipe_5.html")

@main.route("/calendrier-competitions/jeunes")
def competitions_jeunes():
    return render_template("competitions_jeunes.html")

@main.route("/calendrier-competitions/jeunes/equipe_jeunes_1")
def equipe_jeunes_1():
    return render_template("equipe_jeunes_1.html")

@main.route("/calendrier-competitions/jeunes/equipe_jeunes_2")
def equipe_jeunes_2():
    return render_template("equipe_jeunes_2.html")

@main.route("/calendrier-competitions/criterium")
def criterium():
    return render_template("criterium.html")

@main.route("/tarifs")
def tarifs():
    return render_template("tarifs.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")

@main.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None

    if request.method == "POST":
        password = request.form.get("password")

        if password == "JoePingASBTT35^^":
            session["admin_connected"] = True
            return redirect(url_for("main.admin_dashboard"))
        else:
            error = "Mot de passe incorrect."

    return render_template("admin_login.html", error=error)

@main.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_connected"):
        return redirect(url_for("main.admin_login"))

    return render_template("admin_dashboard.html")

@main.route("/admin/logout")
def admin_logout():
    session.pop("admin_connected", None)
    return redirect(url_for("main.admin_login"))


DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "matchs.json")

def charger_matchs():
    with open(DATA_PATH, "r", encoding="utf-8") as fichier:
        return json.load(fichier)

def sauvegarder_matchs(data):
    with open(DATA_PATH, "w", encoding="utf-8") as fichier:
        json.dump(data, fichier, indent=4, ensure_ascii=False)

@main.route("/admin/matchs")
def admin_matchs():
    if not session.get("admin"):
        return redirect(url_for("main.admin_login"))

    data = charger_matchs()
    return render_template("admin_matchs.html", data=data)

@main.route("/admin/matchs/<categorie>/<equipe_id>", methods=["GET", "POST"])
def admin_modifier_equipe(categorie, equipe_id):
    if not session.get("admin"):
        return redirect(url_for("main.admin_login"))

    data = charger_matchs()
    equipes = data.get(categorie, [])

    equipe = next((e for e in equipes if e["id"] == equipe_id), None)

    if equipe is None:
        return "Équipe introuvable", 404

    if request.method == "POST":
        equipe["nom"] = request.form["nom"]
        equipe["division"] = request.form["division"]

        nouveaux_matchs = []

        tours = request.form.getlist("tour")
        dates = request.form.getlist("date")
        equipes_dom = request.form.getlist("equipe_dom")
        equipes_ext = request.form.getlist("equipe_ext")
        lieux = request.form.getlist("lieu")

        for i in range(len(tours)):
            nouveaux_matchs.append({
                "tour": tours[i],
                "date": dates[i],
                "equipe_dom": equipes_dom[i],
                "equipe_ext": equipes_ext[i],
                "lieu": lieux[i]
            })

        equipe["matchs"] = nouveaux_matchs
        sauvegarder_matchs(data)

        return redirect(url_for("main.admin_matchs"))

    return render_template("admin_modifier_equipe.html", equipe=equipe, categorie=categorie)