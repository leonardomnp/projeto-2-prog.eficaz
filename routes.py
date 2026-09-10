from flask import jsonify, request
from servidor import (
    listar_imoveis   
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