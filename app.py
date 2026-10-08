from flask import Flask, render_template, request, redirect, url_for, session
import game

app = Flask(__name__)
app.secret_key = "tic-tac-toe-dev-secret-key"


def init_session():
    session.setdefault("board", game.new_board())
    session.setdefault("difficulty", "easy")
    session.setdefault("status", "playing")
    session.setdefault("winning_line", [])
    session.setdefault("scores", {"player": 0, "computer": 0, "draw": 0})


def start_new_board():
    session["board"] = game.new_board()
    session["status"] = "playing"
    session["winning_line"] = []


def sync_status_and_score(board):
    winner, line = game.check_winner(board)

    if winner == game.PLAYER:
        session["status"] = "player_win"
        session["winning_line"] = line
        session["scores"]["player"] += 1
    elif winner == game.COMPUTER:
        session["status"] = "computer_win"
        session["winning_line"] = line
        session["scores"]["computer"] += 1
    elif game.is_draw(board):
        session["status"] = "draw"
        session["winning_line"] = []
        session["scores"]["draw"] += 1


@app.route("/")
def index():
    init_session()
    return render_template(
        "index.html",
        board=session["board"],
        difficulty=session["difficulty"],
        status=session["status"],
        winning_line=session["winning_line"],
        scores=session["scores"],
    )


@app.route("/move/<int:cell>", methods=["POST"])
def move(cell):
    init_session()
    board = session["board"]

    if not game.play_player_move(board, cell):
        return redirect(url_for("index"))

    sync_status_and_score(board)

    if session["status"] == "playing":
        game.play_computer_turn(board, session["difficulty"])
        sync_status_and_score(board)

    session["board"] = board
    session.modified = True
    return redirect(url_for("index"))


@app.route("/set_difficulty", methods=["POST"])
def set_difficulty():
    init_session()
    chosen = request.form.get("difficulty", "easy")

    if chosen in ("easy", "medium"):
        session["difficulty"] = chosen

    start_new_board()
    session.modified = True
    return redirect(url_for("index"))


@app.route("/new_game", methods=["POST"])
def new_game():
    init_session()
    start_new_board()
    session.modified = True
    return redirect(url_for("index"))


@app.route("/reset_score", methods=["POST"])
def reset_score():
    init_session()
    session["scores"] = {"player": 0, "computer": 0, "draw": 0}
    start_new_board()
    session.modified = True
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
