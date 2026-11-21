import mysql.connector
from mysql.connector import Error


def conectar():
    """Abre e retorna uma conexão com o banco XPTO_Investimentos no MySQL local."""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="umdoistres",  
            database="XPTO_Investimentos",
        )
        return conexao
    except Error as erro:
        print(f"Erro ao conectar ao MySQL: {erro}")
        return None