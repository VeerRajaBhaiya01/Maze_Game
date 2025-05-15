from flask import Flask, render_template, request, jsonify, session
from game.logic import Game

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route("/")
def index():
    session.clear()
    game = Game()
    session["game"] = game.to_dict()
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    direction = request.json["direction"]
    game = Game.from_dict(session["game"])
    result = game.move_hero(direction)
    session["game"] = game.to_dict()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
