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
