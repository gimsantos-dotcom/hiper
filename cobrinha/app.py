import random

from flask import Flask, redirect, render_template, session, url_for

app = Flask(__name__)
app.secret_key = "chave-secreta-jogo-da-cobrinha"

TAMANHO = 10

recorde = {"melhor": 0}

direcoes = {
    "cima": (0, -1),
    "baixo": (0, 1),
    "esquerda": (-1, 0),
    "direita": (1, 0),
}


def sortear_comida(cobra):
    livres = [
        [x, y]
        for x in range(TAMANHO)
        for y in range(TAMANHO)
        if [x, y] not in cobra
    ]
    return random.choice(livres)


def novo_jogo():
    session["cobra"] = [[5, 5], [4, 5], [3, 5]]
    session["comida"] = sortear_comida(session["cobra"])
    session["pontos"] = 0
    session["fim"] = False


def montar_tabuleiro(cobra, comida):
    tabuleiro = ["vazio"] * (TAMANHO * TAMANHO)
    tabuleiro[comida[1] * TAMANHO + comida[0]] = "comida"
    for x, y in cobra:
        tabuleiro[y * TAMANHO + x] = "corpo"
    x, y = cobra[0]
    tabuleiro[y * TAMANHO + x] = "cabeca"
    return tabuleiro


@app.route("/")
def index():
    if "cobra" not in session:
        novo_jogo()
    return render_template(
        "index.html",
        tabuleiro=montar_tabuleiro(session["cobra"], session["comida"]),
        pontos=session["pontos"],
        fim=session["fim"],
        recorde=recorde,
    )


@app.route("/mover/<direcao>")
def mover(direcao):
    if "cobra" not in session:
        novo_jogo()

    if session["fim"] or direcao not in direcoes:
        return redirect(url_for("index"))

    cobra = session["cobra"]
    dx, dy = direcoes[direcao]
    nova_cabeca = [cobra[0][0] + dx, cobra[0][1] + dy]

    # não deixa a cobra voltar para trás
    if nova_cabeca == cobra[1]:
        return redirect(url_for("index"))

    comeu = nova_cabeca == session["comida"]
    corpo = cobra if comeu else cobra[:-1]
    bateu_na_parede = not (0 <= nova_cabeca[0] < TAMANHO and 0 <= nova_cabeca[1] < TAMANHO)

    if bateu_na_parede or nova_cabeca in corpo:
        session["fim"] = True
        return redirect(url_for("index"))

    cobra.insert(0, nova_cabeca)
    if comeu:
        session["pontos"] += 1
        recorde["melhor"] = max(recorde["melhor"], session["pontos"])
        session["comida"] = sortear_comida(cobra)
    else:
        cobra.pop()

    session["cobra"] = cobra
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
