import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(override=True)

conn = mysql.connector.connect(
    host=os.getenv("AIVEN_HOST"),
    port=int(os.getenv("AIVEN_PORT")),
    user=os.getenv("AIVEN_USER"),
    password=os.getenv("AIVEN_PASSWORD"),
    database=os.getenv("AIVEN_DB"),
    ssl_ca=os.getenv("AIVEN_CA"),  
    ssl_verify_cert=True
)

