from flask import Flask, render_template, session, request, jsonify, redirect
from database import criar_tabelas
from database import conectar



app = Flask(__name__)
criar_tabelas()

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
    nome = request.form["nome"]
    endereco = request.form["endereco"]
    carrinho = session["carrinho"]

    total = sum(
        PRECOS[i["id"]] * i["quantidade"]
        for i in carrinho
    )

    conn = conectar()
    cursor = conn.cursor()

    # cria pedido
    cursor.execute("""
        INSERT INTO pedidos (cliente, endereco, pagamento, total, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        nome,
        endereco,
        "Mercado Pago",
        total,
        "Aguardando pagamento"
    ))

    pedido_id = cursor.lastrowid

    # salva itens
    for item in carrinho:
        cursor.execute("""
            INSERT INTO itens (pedido_id, nome, quantidade, observacoes)
            VALUES (?, ?, ?, ?)
        """, (
            pedido_id,
            item["nome"],
            item["quantidade"],
            item.get("observacoes", "")
        ))

    conn.commit()
    conn.close()

    # salva pedido_id na sessão

    session.modified = True

    return redirect(f"/pedido/{pedido_id}")




@app.route("/pedido/<int:pid>")
def pedido_cliente(pid):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, cliente, endereco, pagamento, total, status FROM pedidos WHERE id = ?",
        (pid,)
    )
    pedido = cursor.fetchone()

    if not pedido:
        conn.close()
        return "Pedido não encontrado", 404

    cursor.execute(
        "SELECT nome, quantidade, observacoes FROM itens WHERE pedido_id = ?",
        (pid,)
    )
    itens = cursor.fetchall()

    conn.close()

    return render_template(
        "pedido_cliente.html",
        pedido={
            "id": pedido[0],
            "cliente": pedido[1],
            "endereco": pedido[2],
            "pagamento": pedido[3],
            "total": pedido[4],
            "status": pedido[5],
            "itens": itens
        }
    )


@app.route("/api/status/<int:pid>")
def api_status(pid):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM pedidos WHERE id = ?",
        (pid,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"status": "Pedido não encontrado"}), 404

    return jsonify({"status": row[0]})

@app.route("/admin")
def admin():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos ORDER BY id DESC")
    pedidos_raw = cursor.fetchall()

    pedidos = []
    for p in pedidos_raw:
        cursor.execute(
            "SELECT nome, quantidade FROM itens WHERE pedido_id = ?",
            (p[0],)
        )
        itens = cursor.fetchall()

        pedidos.append({
            "id": p[0],
            "cliente": p[1],
            "endereco": p[2],
            "pagamento": p[3],
            "total": p[4],
            "status": p[5],
            "itens": itens
        })

    conn.close()
    return render_template("admin.html", pedidos=pedidos)


@app.route("/alterar_status", methods=["POST"])
def alterar_status():
    pedido_id = request.form["id"]
    status = request.form["status"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (status, pedido_id)
    )

    conn.commit()
    conn.close()

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

import mercadopago
import os

sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))

@app.route("/pagar/<int:pedido_id>")
def pagar(pedido_id):
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT total FROM pedidos WHERE id = ?",
            (pedido_id,)
        )
        pedido = cursor.fetchone()

        if not pedido:
            conn.close()
            return "Pedido não encontrado", 404

        total = float(pedido[0])

        cursor.execute(
            "SELECT nome, quantidade FROM itens WHERE pedido_id = ?",
            (pedido_id,)
        )
        itens_db = cursor.fetchall()
        conn.close()

        itens = [{
            "title": nome,
            "quantity": quantidade,
            "currency_id": "BRL",
            "unit_price": total / len(itens_db)
        } for nome, quantidade in itens_db]

        preference_data = {
            "items": itens,
            "external_reference": str(pedido_id),
            "notification_url": "https://SEU-SITE.onrender.com/webhook",
            "auto_return": "approved"
        }

        preference = sdk.preference().create(preference_data)

        return redirect(preference["response"]["init_point"])

    except Exception as e:
        return f"Erro ao criar pagamento: {str(e)}", 500







@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and data.get("type") == "payment":
        payment_id = data["data"]["id"]
        payment = sdk.payment().get(payment_id)

        if payment["response"]["status"] == "approved":
            pedido_id = payment["response"]["external_reference"]

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE pedidos SET status = ? WHERE id = ?",
                ("Pago", pedido_id)
            )

            conn.commit()
            conn.close()

    return "ok"


@app.route("/aguardando")
def aguardando():
    return "Pagamento confirmado! Seu pedido está sendo preparado."




if __name__ == "__main__":
    app.run()
