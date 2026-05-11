from flask import Blueprint, render_template

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