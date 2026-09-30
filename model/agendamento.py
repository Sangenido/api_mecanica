from config.db import get_connection

CAMPOS = """id, nome_cliente, telefone, servico_id,
            DATE_FORMAT(data_agendamento, '%Y-%m-%d') AS data_agendamento,
            status, observacao"""


class Agendamento:

    @staticmethod
    def consultar_todos():
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT {CAMPOS} FROM agendamentos")
        dados = cur.fetchall()
        cur.close()
        conn.close()
        return dados

    @staticmethod
    def consultar_por_id(id):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT {CAMPOS} FROM agendamentos WHERE id = %s", (id,))
        dado = cur.fetchone()
        cur.close()
        conn.close()
        return dado

    @staticmethod
    def cadastrar(d):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO agendamentos (nome_cliente, telefone, servico_id, data_agendamento, observacao) "
            "VALUES (%s, %s, %s, %s, %s)",
            (d["nome_cliente"], d["telefone"], d["servico_id"], d["data_agendamento"], d.get("observacao")),
        )
        conn.commit()
        novo_id = cur.lastrowid
        cur.close()
        conn.close()
        return novo_id

    @staticmethod
    def atualizar(id, d):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE agendamentos SET nome_cliente=%s, telefone=%s, servico_id=%s, "
            "data_agendamento=%s, status=%s, observacao=%s WHERE id=%s",
            (d["nome_cliente"], d["telefone"], d["servico_id"], d["data_agendamento"],
             d.get("status", "pendente"), d.get("observacao"), id),
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def excluir(id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM agendamentos WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
