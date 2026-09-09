import pytest
from unittest.mock import patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

IMOVEL_EXEMPLO = {
    "id": 1,
    "logradouro": "Nicole Common",
    "tipo_logradouro": "Travessa",
    "bairro": "Lake Danielle",
    "cidade": "Judymouth",
    "cep": "85184",
    "tipo": "casa em condominio",
    "valor": 488423.52,
    "data_aquisicao": "2017-07-29",
}


IMOVEL_EXEMPLO_2 = {
    "id": 3,
    "logradouro": "Taylor Ranch",
    "tipo_logradouro": "Avenida",
    "bairro": "West Jennashire",
    "cidade": "Katherinefurt",
    "cep": "51116",
    "tipo": "apartamento",
    "valor": 815969.92,
    "data_aquisicao": "2020-04-24",
}

@patch("routes.listar_imoveis")
def test_listar_imoveis(client, mock_listar_imoveis):
    mock_listar_imoveis.return_value = [IMOVEL_EXEMPLO, IMOVEL_EXEMPLO_2]
    response = client.get("/imoveis")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["logradouro"] == "Nicole Common"
    mock_listar_imoveis.assert_called_once()

@patch("routes.listar_imoveis")
def test_listar_imoveis_vazio(client, mock_listar_imoveis):
    mock_listar_imoveis.return_value = []
    response = client.get("/imoveis")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0
    assert data [0]["logradouro"] == "Nicole Common"
    mock_listar_imoveis.assert_called_once()

@patch("routes.listar_imoveis")
def test_listar_imoveis_erro(client, mock_listar_imoveis):
    mock_listar_imoveis.side_effect = Exception("Erro ao listar imóveis")
    response = client.get("/imoveis")
    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Erro ao listar imóveis"
    mock_listar_imoveis.assert_called_once()