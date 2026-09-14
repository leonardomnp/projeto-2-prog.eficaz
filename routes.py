from flask import jsonify, request, url_for
from servidor import (
    listar_imoveis, buscar_imovel_por_id, criar_imovel,
    atualizar_imovel, remover_imovel,
    buscar_imoveis_por_tipo, buscar_imoveis_por_cidade
)

CAMPOS_OBRIGATORIOS = [
    "logradouro", "tipo_logradouro", "bairro",
    "cidade", "cep", "tipo", "valor", "data_aquisicao"
]


def validar_dados(dados):
    return [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados]


def links_da_colecao(self_href=None):
    colecao = url_for("rota_listar_imoveis")
    return {
        "self": {"href": self_href or colecao, "method": "GET"},
        "create": {"href": colecao, "method": "POST"},
        "filter_by_type": {
            "href": f"{colecao}/tipo/{{tipo}}",
            "method": "GET",
            "templated": True,
        },
        "filter_by_city": {
            "href": f"{colecao}/cidade/{{cidade}}",
            "method": "GET",
            "templated": True,
        },
    }


def links_do_imovel(imovel_id):
    recurso = url_for("rota_buscar_imovel", imovel_id=imovel_id)
    return {
        "self": {"href": recurso, "method": "GET"},
        "update": {"href": recurso, "method": "PUT"},
        "delete": {"href": recurso, "method": "DELETE"},
        "collection": {"href": url_for("rota_listar_imoveis"), "method": "GET"},
    }


def representar_imovel(imovel):
    representacao = dict(imovel)
    representacao["_links"] = links_do_imovel(representacao["id"])
    return representacao


def representar_colecao(imoveis, self_href=None):
    return {
        "imoveis": [representar_imovel(imovel) for imovel in imoveis],
        "_links": links_da_colecao(self_href),
    }


def registrar_rotas(app):

    @app.route("/imoveis", methods=["GET"])
    def rota_listar_imoveis():
        try:
            imoveis = listar_imoveis()
            return jsonify(representar_colecao(imoveis)), 200
        except Exception as e:
            return jsonify({
                "erro": "Erro interno ao listar imóveis",
                "_links": {"self": {"href": url_for("rota_listar_imoveis"), "method": "GET"}},
            }), 500

    @app.route("/imoveis/<int:imovel_id>", methods=["GET"])
    def rota_buscar_imovel(imovel_id):
        imovel = buscar_imovel_por_id(imovel_id)
        if imovel is None:
            return jsonify({
                "erro": "Imóvel não encontrado",
                "_links": {"collection": {"href": url_for("rota_listar_imoveis"), "method": "GET"}},
            }), 404
        return jsonify(representar_imovel(imovel)), 200

    @app.route("/imoveis", methods=["POST"])
    def rota_criar_imovel():
        dados = request.get_json(silent=True) or {}
        faltando = validar_dados(dados)
        if faltando:
            return jsonify({
                "erro": f"Campos obrigatórios faltando: {faltando}",
                "_links": {"collection": {"href": url_for("rota_listar_imoveis"), "method": "GET"}},
            }), 400

        novo_id = criar_imovel(dados)
        resposta = jsonify({"id": novo_id, "_links": links_do_imovel(novo_id)})
        resposta.status_code = 201
        resposta.headers["Location"] = url_for("rota_buscar_imovel", imovel_id=novo_id)
        return resposta

    @app.route("/imoveis/<int:imovel_id>", methods=["PUT"])
    def rota_atualizar_imovel(imovel_id):
        dados = request.get_json(silent=True) or {}
        faltando = validar_dados(dados)
        if faltando:
            return jsonify({
                "erro": f"Campos obrigatórios faltando: {faltando}",
                "_links": links_do_imovel(imovel_id),
            }), 400

        linhas_afetadas = atualizar_imovel(imovel_id, dados)
        if linhas_afetadas == 0:
            return jsonify({
                "erro": "Imóvel não encontrado",
                "_links": {"collection": {"href": url_for("rota_listar_imoveis"), "method": "GET"}},
            }), 404
        return jsonify({
            "message": "Imóvel atualizado com sucesso",
            "_links": links_do_imovel(imovel_id),
        }), 200

    @app.route("/imoveis/<int:imovel_id>", methods=["DELETE"])
    def rota_remover_imovel(imovel_id):
        linhas_afetadas = remover_imovel(imovel_id)
        if linhas_afetadas == 0:
            return jsonify({
                "erro": "Imóvel não encontrado",
                "_links": {"collection": {"href": url_for("rota_listar_imoveis"), "method": "GET"}},
            }), 404
        return jsonify({
            "message": "Imóvel removido com sucesso",
            "_links": {"collection": {"href": url_for("rota_listar_imoveis"), "method": "GET"}},
        }), 200

    @app.route("/imoveis/tipo/<string:tipo>", methods=["GET"])
    def rota_buscar_imoveis_por_tipo(tipo):
        imoveis = buscar_imoveis_por_tipo(tipo)
        if not imoveis:
            return jsonify({
                "erro": "Nenhum imóvel encontrado para o tipo especificado",
                "_links": links_da_colecao(url_for("rota_buscar_imoveis_por_tipo", tipo=tipo)),
            }), 404
        return jsonify(representar_colecao(
            imoveis,
            url_for("rota_buscar_imoveis_por_tipo", tipo=tipo),
        )), 200

    @app.route("/imoveis/cidade/<cidade>", methods=["GET"])
    def rota_buscar_por_cidade(cidade):
        imoveis = buscar_imoveis_por_cidade(cidade)
        if not imoveis:
            return jsonify({
                "erro": "Nenhum imóvel encontrado para a cidade especificada",
                "_links": links_da_colecao(url_for("rota_buscar_por_cidade", cidade=cidade)),
            }), 404
        return jsonify(representar_colecao(
            imoveis,
            url_for("rota_buscar_por_cidade", cidade=cidade),
        )), 200
