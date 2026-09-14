from flask import jsonify, request
from servidor import (
    listar_imoveis, buscar_imovel_por_id, criar_imovel, atualizar_imovel, remover_imovel, buscar_imoveis_por_tipo, buscar_imoveis_por_cidade
)
 
CAMPOS_OBRIGATORIOS = [
    "logradouro", "tipo_logradouro", "bairro",
    "cidade", "cep", "tipo", "valor", "data_aquisicao"
]
 
 
def validar_dados(dados):
    return [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados]
 
 
def registrar_rotas(app):
 
    @app.route("/imoveis", methods=["GET"])
    def rota_listar_imoveis():
        imoveis = listar_imoveis()
        return jsonify(imoveis), 200
 
    @app.route("/imoveis/<int:imovel_id>", methods=["GET"])
    def rota_buscar_imovel(imovel_id):
        imovel = buscar_imovel_por_id(imovel_id)
        if imovel is None:
            return jsonify({"erro": "Imóvel não encontrado"}), 404
        return jsonify(imovel), 200

    @app.route("/imoveis", methods=["POST"])
    def rota_criar_imovel():
        dados = request.get_json(silent=True) or {}
        faltando = validar_dados(dados)
        if faltando:
            return jsonify({"erro": f"Campos obrigatórios faltando: {faltando}"}), 400

        novo_id = criar_imovel(dados)
        return jsonify({"id": novo_id}), 201

    @app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
    def rota_atualizar_imovel(imovel_id):
        dados = request.get_json(silent=True) or {}
        faltando = validar_dados(dados)
        if faltando:
            return jsonify({"erro": f"Campos obrigatórios faltando: {faltando}"}), 400

        linhas_afetadas = atualizar_imovel(imovel_id, dados)
        if linhas_afetadas == 0:
            return jsonify({"erro": "Imóvel não encontrado"}), 404

        return jsonify({"message": "Imóvel atualizado com sucesso"}), 200

    @app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
    def rota_remover_imovel(imovel_id):
        linhas_afetadas = remover_imovel(imovel_id)
        if linhas_afetadas == 0:
            return jsonify({"erro": "Imóvel não encontrado"}), 404

        return jsonify({"message": "Imóvel removido com sucesso"}), 200 

    @app.route("/imoveis/tipo/<string:tipo>", methods=["GET"])
    def rota_buscar_imoveis_por_tipo(tipo):
        imoveis = buscar_imoveis_por_tipo(tipo)
        if not imoveis:
            return jsonify({"erro": "Nenhum imovel encontrado para o tipo especificado"}), 404
        return jsonify(imoveis), 200

    @app.route("/imoveis/cidade/<cidade>", methods=["GET"])
    def rota_buscar_por_cidade(cidade):
        imoveis = buscar_imoveis_por_cidade(cidade)
        return jsonify(imoveis), 200