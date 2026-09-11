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

@patch("routes.buscar_imovel_por_id")
def test_buscar_imovel_por_id_existente(mock_buscar, client):
    mock_buscar.return_value = [IMOVEL_EXEMPLO, IMOVEL_EXEMPLO_2]
    response = client.get("/imoveis/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["cidade"] == "Judymouth"
    mock_buscar.assert_called_once_with(1)

@patch("routes.buscar_imovel_por_id")
def test_buscar_imovel_por_id_inexistente(mock_buscar, client):
    mock_buscar.return_value = None

    response = client.get("/imoveis/999")

    assert response.status_code == 404
    assert "erro" in response.get_json()
 
@patch("routes.criar_imovel")
def test_criar_imovel(mock_criar, client):
    mock_criar.return_value = 5
 
    novo_imovel = {
        "logradouro": "Stacey Isle",
        "tipo_logradouro": "Avenida",
        "bairro": "Reneeberg",
        "cidade": "Bentleymouth",
        "cep": "01631",
        "tipo": "terreno",
        "valor": 352507.35,
        "data_aquisicao": "2014-11-03",
    }
 
    response = client.post("/imoveis", json=novo_imovel)
 
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 5
    mock_criar.assert_called_once_with(novo_imovel)
 
 
def test_criar_imovel_dados_incompletos(client):
    response = client.post("/imoveis", json={"tipo": "casa"})
 
    assert response.status_code == 400
    assert "erro" in response.get_json()
 
 
def test_criar_imovel_sem_json(client):
    response = client.post("/imoveis")
 
    assert response.status_code == 400

@patch("routes.atualizar_imovel")
def test_atualizar_imovel_existente(mock_atualizar, client):
    mock_atualizar.return_value = 1
 
    dados = {
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Travessa",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "85184",
        "tipo": "casa em condominio",
        "valor": 500000.00,
        "data_aquisicao": "2017-07-29",
    }
 
    response = client.put("/imoveis/1", json=dados)
 
    assert response.status_code == 200
    mock_atualizar.assert_called_once_with(1, dados)
 
 
@patch("routes.atualizar_imovel")
def test_atualizar_imovel_inexistente(mock_atualizar, client):
    mock_atualizar.return_value = 0
 
    dados = {
        "logradouro": "Nicole Common",
        "tipo_logradouro": "Travessa",
        "bairro": "Lake Danielle",
        "cidade": "Judymouth",
        "cep": "85184",
        "tipo": "casa em condominio",
        "valor": 500000.00,
        "data_aquisicao": "2017-07-29",
    }
 
    response = client.put("/imoveis/999", json=dados)
 
    assert response.status_code == 404
 
def test_atualizar_imovel_dados_incompletos(client):
    response = client.put("/imoveis/1", json={"cidade": "Judymouth"})
 
    assert response.status_code == 400

@patch("routes.remover_imovel")
def test_remover_imovel_existente(mock_remover, client):
    mock_remover.return_value = 1
 
    response = client.delete("/imoveis/1")
 
    assert response.status_code == 200
    mock_remover.assert_called_once_with(1)
 
 
@patch("routes.remover_imovel")
def test_remover_imovel_inexistente(mock_remover, client):
    mock_remover.return_value = 0
 
    response = client.delete("/imoveis/999")
 
    assert response.status_code == 404

@patch("routes.buscar_imoveis_por_tipo")
def test_buscar_imoveis_por_tipo(mock_buscar, client):
    mock_buscar.return_value = [IMOVEL_EXEMPLO_2]
 
    response = client.get("/imoveis/tipo/apartamento")
 
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert all(item["tipo"] == "apartamento" for item in data)
    mock_buscar.assert_called_once_with("apartamento")

@patch("routes.buscar_imoveis_por_tipo")
def test_buscar_imoveis_por_tipo_inexistente(mock_buscar, client):
    mock_buscar.return_value = []
 
    response = client.get("/imoveis/tipo/inexistente")
 
    assert response.status_code == 200
    assert response.get_json() == []