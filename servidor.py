import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

CAMPOS = [
    "logradouro", "tipo_logradouro", "bairro",
    "cidade", "cep", "tipo", "valor", "data_aquisicao"
]

def load_db():
    conn = mysql.connector.connect(
    host=os.getenv("AIVEN_HOST"),
    port=int(os.getenv("AIVEN_PORT")),
    user=os.getenv("AIVEN_USER"),
    password=os.getenv("AIVEN_PASSWORD"),
    database=os.getenv("AIVEN_DB"),
    ssl_ca=os.getenv("AIVEN_CA"),  
    ssl_verify_cert=True
)
    return conn

def listar_imoveis():
    conn = load_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis")
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado

def buscar_imovel_por_id(imovel_id):
    conn = load_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (imovel_id,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado

def criar_imovel(dados):
    conn = load_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"],
         dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"])
    )
    conn.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return novo_id

def atualizar_imovel(imovel_id, dados):
    conn = load_db()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE imoveis SET logradouro=%s, tipo_logradouro=%s, bairro=%s, cidade=%s,
           cep=%s, tipo=%s, valor=%s, data_aquisicao=%s WHERE id=%s""",
        (dados["logradouro"], dados["tipo_logradouro"], dados["bairro"], dados["cidade"],
         dados["cep"], dados["tipo"], dados["valor"], dados["data_aquisicao"], imovel_id)
    )
    conn.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()
    return linhas_afetadas

def remover_imovel(imovel_id):
    conn = load_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (imovel_id,))
    conn.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conn.close()
    return linhas_afetadas

def buscar_imoveis_por_tipo(tipo):
    conn = load_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultado
