from flask import Flask, render_template, session, request, jsonify, redirect

app = Flask(__name__)
app.secret_key = "bullhouse-secret"

# ================= PRODUTOS =================

PRODUTOS_HAMBURGUER = [
    {
        "id": 1,
        "nome": "NELORE",
        "preco": 24.99,
        "descricao": "Servido no delicioso pão de brioche com bife de 180g assado na brasa, queijo prato, ovo, salada e dois molhos de sua preferência. Um clássico do hambúrguer artesanal.",
        "imagem": "nelore.webp"
    },
    {
        "id": 2,
        "nome": "JAVALI",
        "preco": 29.99,
        "descricao": "Bife de costelinha suína 180g assado na brasa, queijo canastra, bacon artesanal Bull, pão de gergelim, ovo, salada e dois molhos à escolha.",
        "imagem": "javali.webp"
    },
    {
        "id": 3,
        "nome": "ANGUS",
        "preco": 34.99,
        "descricao": "Hambúrguer 100% angus de 200g, extremamente suculento, servido no pão brioche, com queijo canastra, salada e dois molhos especiais.",
        "imagem": "angus.webp"
    },
    {
        "id": 4,
        "nome": "ZEBU",
        "preco": 29.99,
        "descricao": "Pão australiano com bife de 180g na brasa, queijo cheddar, bacon artesanal Bull, ovo, salada e dois molhos.",
        "imagem": "zebu.webp"
    },
    {
        "id": 5,
        "nome": "GUZERÁ",
        "preco": 31.99,
        "descricao": "Bife de 180g assado na brasa, queijo cheddar, bacon artesanal Bull, anéis de cebola empanados, ovo, salada e dois molhos no pão australiano.",
        "imagem": "guzera.webp"
    },
    {
        "id": 6,
        "nome": "MINOTAURO",
        "preco": 41.99,
        "descricao": "Dois bifes de 180g na brasa, duplo cheddar, duplo bacon artesanal Bull, pão de gergelim, salada, ovo e dois molhos. Para quem tem fome de verdade.",
        "imagem": "minotauro.webp"
    },
    {
        "id": 7,
        "nome": "BEZERRO",
        "preco": 20.99,
        "descricao": "Hambúrguer infantil com bife de 100g, pão brioche, queijo prato, ovo, salada e dois molhos opcionais.",
        "imagem": "bezerro.webp"
    },
    {
        "id": 8,
        "nome": "COCOTA",
        "preco": 29.99,
        "descricao": "Bife de frango 180g assado na brasa, bacon artesanal Bull, queijo cheddar, salada, ovo e dois molhos no pão brioche.",
        "imagem": "cocota.webp"
    },
    {
        "id": 9,
        "nome": "CARACU",
        "preco": 31.99,
        "descricao": "Bife de 180g na brasa, queijo cheddar, bacon artesanal Bull, ovo, cebola caramelizada e salada no pão brioche. Equilíbrio perfeito do agridoce.",
        "imagem": "caracu.webp"
    },
    {
        "id": 10,
        "nome": "HOLANDÊS",
        "preco": 45.99,
        "descricao": "Dois bifes de 180g, duplo cheddar, duplo bacon artesanal Bull, duplo ovo, salaminho italiano, cebola caramelizada, pão de gergelim e dois molhos.",
        "imagem": "holandes.webp"
    },
]

PRODUTOS_PORCOES = [
    {
        "id": 101,
        "nome": "BATATA FRITA COMPLETA",
        "preco": 29.99,
        "descricao": "Batata frita crocante acompanhada de queijo derretido e bacon artesanal.",
        "imagem": "completa.webp"
    },
    {
        "id": 102,
        "nome": "BATATA FRITA SIMPLES",
        "preco": 24.99,
        "descricao": "Batata frita palito, crocante e sequinha.",
        "imagem": "simples.webp"
    },
    {
        "id": 103,
        "nome": "BATATA INDIVIDUAL",
        "preco": 10.00,
        "descricao": "Porção individual de batata frita.",
        "imagem": "individual.webp"
    },
    {
        "id": 104,
        "nome": "CEBOLA EMPANADA",
        "preco": 14.99,
        "descricao": "Anéis de cebola empanados e crocantes.",
        "imagem": "cebola.webp"
    }
]

# ================= PREÇOS =================
PRECOS = {p["id"]: p["preco"] for p in PRODUTOS_HAMBURGUER + PRODUTOS_PORCOES}

# ================= PEDIDOS =================
PEDIDOS = []

# ================= INIT =================
@app.before_request
def init():
    session.setdefault("carrinho", [])

# ================= ROTAS =================
@app.route("/")
def homepage():
    return render_template(
        "homepage.html",
        produtos_hamburguer=PRODUTOS_HAMBURGUER,
        produtos_porcoes=PRODUTOS_PORCOES
    )

@app.route("/add_carrinho", methods=["POST"])
def add_carrinho():
    dados = request.get_json()

    item = {
        "id": dados["id"],
        "nome": dados["nome"],
        "quantidade": int(dados["quantidade"]),
        "observacoes": dados.get("observacoes", "")
    }

    for p in session["carrinho"]:
        if p["id"] == item["id"]:
            p["quantidade"] += item["quantidade"]
            session.modified = True
            return jsonify({"status": "ok"})

    session["carrinho"].append(item)
    session.modified = True
    return jsonify({"status": "ok"})

@app.route("/get_carrinho")
def get_carrinho():
    return jsonify(session["carrinho"])

@app.route("/total")
def total():
    total = sum(PRECOS[i["id"]] * i["quantidade"] for i in session["carrinho"])
    return jsonify({"total": round(total, 2)})

@app.route("/checkout")
def checkout():
    carrinho = session["carrinho"]
    total = sum(PRECOS[i["id"]] * i["quantidade"] for i in carrinho)
    return render_template("checkout.html", carrinho=carrinho, total=round(total, 2))

@app.route("/finalizar_pedido", methods=["POST"])
def finalizar_pedido():
    pedido = {
        "id": len(PEDIDOS) + 1,
        "cliente": request.form["nome"],
        "endereco": request.form["endereco"],
        "pagamento": request.form["pagamento"],
        "itens": session["carrinho"],
        "total": round(sum(PRECOS[i["id"]] * i["quantidade"] for i in session["carrinho"]), 2),
        "status": "Novo"
    }

    PEDIDOS.append(pedido)
    session["carrinho"] = []
    session.modified = True

    return render_template("pedido_sucesso.html", pedido=pedido)

@app.route("/pedido/<int:pid>")
def pedido_cliente(pid):
    for p in PEDIDOS:
        if p["id"] == pid:
            return render_template("pedido_cliente.html", pedido=p)
    return "Pedido não encontrado", 404

@app.route("/api/status/<int:pid>")
def api_status(pid):
    for p in PEDIDOS:
        if p["id"] == pid:
            return jsonify({"status": p["status"]})
    return jsonify({"status": "Pedido não encontrado"}), 404

@app.route("/admin")
def admin():
    return render_template("admin.html", pedidos=PEDIDOS)

@app.route("/alterar_status", methods=["POST"])
def alterar_status():
    idx = int(request.form["index"])
    PEDIDOS[idx]["status"] = request.form["status"]
    return redirect("/admin")

@app.route("/remover_carrinho", methods=["POST"])
def remover_carrinho():
    dados = request.get_json()
    pid = dados["id"]

    session["carrinho"] = [
        i for i in session["carrinho"] if i["id"] != pid
    ]
    session.modified = True

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()
