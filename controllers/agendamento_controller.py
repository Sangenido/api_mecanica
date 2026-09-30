from flask import Blueprint, jsonify, request
from model.agendamento import Agendamento

agendamentos_bp = Blueprint("agendamentos", __name__)

OBRIGATORIOS = ["nome_cliente", "telefone", "servico_id", "data_agendamento"]


def campos_faltando(dados):
    return [c for c in OBRIGATORIOS if not dados.get(c)]


@agendamentos_bp.route("/agendamentos", methods=["GET"])
def consultar_todos():
    """
    Consulta todos os agendamentos
    ---
    tags:
      - Agendamentos
    responses:
      200:
        description: Lista de agendamentos
    """
    return jsonify(Agendamento.consultar_todos()), 200


@agendamentos_bp.route("/agendamentos/<int:id>", methods=["GET"])
def consultar_por_id(id):
    """
    Consulta um agendamento por ID
    ---
    tags:
      - Agendamentos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Agendamento encontrado
      404:
        description: Agendamento não encontrado
    """
    agendamento = Agendamento.consultar_por_id(id)
    if not agendamento:
        return jsonify({"erro": "Agendamento não encontrado"}), 404
    return jsonify(agendamento), 200


@agendamentos_bp.route("/agendamentos", methods=["POST"])
def cadastrar():
    """
    Cadastra um agendamento
    ---
    tags:
      - Agendamentos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [nome_cliente, telefone, servico_id, data_agendamento]
          properties:
            nome_cliente:
              type: string
              example: Carlos Silva
            telefone:
              type: string
              example: "(51) 90000-0000"
            servico_id:
              type: integer
              example: 1
            data_agendamento:
              type: string
              example: "2026-10-25"
            observacao:
              type: string
              example: Barulho ao frear
    responses:
      201:
        description: Agendamento cadastrado
      400:
        description: Dados inválidos
    """
    dados = request.get_json(silent=True) or {}
    faltando = campos_faltando(dados)
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios: {', '.join(faltando)}"}), 400

    novo_id = Agendamento.cadastrar(dados)
    return jsonify({"id": novo_id, "mensagem": "Agendamento cadastrado"}), 201


@agendamentos_bp.route("/agendamentos/<int:id>", methods=["PUT"])
def atualizar(id):
    """
    Atualiza um agendamento
    ---
    tags:
      - Agendamentos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [nome_cliente, telefone, servico_id, data_agendamento]
          properties:
            nome_cliente:
              type: string
              example: Carlos Silva
            telefone:
              type: string
              example: "(51) 90000-0000"
            servico_id:
              type: integer
              example: 1
            data_agendamento:
              type: string
              example: "2026-10-25"
            status:
              type: string
              example: confirmado
            observacao:
              type: string
              example: Cliente confirmou por telefone
    responses:
      200:
        description: Agendamento atualizado
      400:
        description: Dados inválidos
      404:
        description: Agendamento não encontrado
    """
    if not Agendamento.consultar_por_id(id):
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    dados = request.get_json(silent=True) or {}
    faltando = campos_faltando(dados)
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios: {', '.join(faltando)}"}), 400

    Agendamento.atualizar(id, dados)
    return jsonify({"mensagem": "Agendamento atualizado"}), 200


@agendamentos_bp.route("/agendamentos/<int:id>", methods=["DELETE"])
def excluir(id):
    """
    Exclui um agendamento
    ---
    tags:
      - Agendamentos
    parameters:
      - in: path
        name: id
        type: integer
        required: true
    responses:
      200:
        description: Agendamento excluído
      404:
        description: Agendamento não encontrado
    """
    if not Agendamento.consultar_por_id(id):
        return jsonify({"erro": "Agendamento não encontrado"}), 404

    Agendamento.excluir(id)
    return jsonify({"mensagem": "Agendamento excluído"}), 200
