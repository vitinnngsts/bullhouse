import sqlite3

def conectar():
    return sqlite3.connect("bullhouse.db", check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        endereco TEXT,
        pagamento TEXT,
        total REAL,
        status TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER,
        nome TEXT,
        quantidade INTEGER,
        observacoes TEXT
    )
    """)

    conn.commit()
    conn.close()
