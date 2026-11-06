from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-jogo-da-velha"

placar = {"X": 0, "O": 0, "Empate": 0}


def tabuleiro_vazio():
    return [" "] * 9


def verificar_vencedor(tabuleiro):
    combinacoes = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6),
    ]
    for a, b, c in combinacoes:
        if tabuleiro[a] != " " and tabuleiro[a] == tabuleiro[b] == tabuleiro[c]:
            return tabuleiro[a]
    if " " not in tabuleiro:
        return "Empate"
    return None


def novo_jogo():
    session["tabuleiro"] = tabuleiro_vazio()
    session["jogador_atual"] = "X"


@app.route("/")
def index():
    if "tabuleiro" not in session:
        novo_jogo()
    return render_template(
        "index.html",
        tabuleiro=session["tabuleiro"],
        jogador_atual=session["jogador_atual"],
        vencedor=verificar_vencedor(session["tabuleiro"]),
        placar=placar,
    )


@app.route("/jogar/<int:posicao>")
def jogar(posicao):
    tabuleiro = session["tabuleiro"]

    if verificar_vencedor(tabuleiro) or tabuleiro[posicao] != " ":
        return redirect(url_for("index"))

    tabuleiro[posicao] = session["jogador_atual"]
    session["tabuleiro"] = tabuleiro
    session["jogador_atual"] = "O" if session["jogador_atual"] == "X" else "X"

    resultado = verificar_vencedor(tabuleiro)
    if resultado:
        placar[resultado] += 1

    return redirect(url_for("index"))


@app.route("/reiniciar")
def reiniciar():
    novo_jogo()
    return redirect(url_for("index"))


@app.route("/regras")
def regras():
    return render_template("regras.html")


if __name__ == "__main__":
    app.run(debug=True)
