from database import conectar
from models import Cliente


class ClienteRepository:
    """Camada de persistência (Repository Pattern) para gravar e consultar dados no MySQL."""

    def salvar(self, cliente: Cliente) -> bool:
        conexao = conectar()
        if not conexao:
            return False

        cursor = conexao.cursor()
        try:
            # Evita duplicidade caso o script seja executado mais de uma vez
            cursor.execute("SELECT CPF FROM Cliente WHERE CPF = %s", (cliente.cpf,))
            if cursor.fetchone():
                print(f"Aviso: Cliente {cliente.nome} (CPF {cliente.cpf}) já está cadastrado no banco.")
                return True

            # 1. Grava na tabela principal Cliente
            cursor.execute(
                "INSERT INTO Cliente (CPF, Nome) VALUES (%s, %s)",
                (cliente.cpf, cliente.nome),
            )

            # 2. Grava os objetos compostos nas tabelas filhas (1:N)
            for tel in cliente.telefones:
                cursor.execute(
                    "INSERT INTO Telefone (CPF_Cliente, Numero, Tipo) VALUES (%s, %s, %s)",
                    (cliente.cpf, tel.numero, tel.tipo),
                )

            for email in cliente.emails:
                cursor.execute(
                    "INSERT INTO Email (CPF_Cliente, Endereco_Email) VALUES (%s, %s)",
                    (cliente.cpf, email.endereco),
                )

            for conta in cliente.contas:
                cursor.execute(
                    """
                    INSERT INTO Conta_Bancaria (CPF_Cliente, Banco, Agencia, Conta, Saldo, Data_Saldo)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (cliente.cpf, conta.banco, conta.agencia, conta.conta, conta.saldo, conta.data_saldo),
                )

            for inv in cliente.investimentos:
                cursor.execute(
                    """
                    INSERT INTO Investimento (CPF_Cliente, Tipo_Investimento, Valor_Investido)
                    VALUES (%s, %s, %s)
                    """,
                    (cliente.cpf, inv.tipo_investimento, inv.valor_investido),
                )

            conexao.commit()
            print(f"Sucesso: Cliente {cliente.nome} e seus vínculos foram gravados no MySQL!")
            return True

        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao salvar cliente no banco: {erro}")
            return False
        finally:
            cursor.close()
            conexao.close()

    def listar_carteira_geral(self) -> list[dict]:
        conexao = conectar()
        if not conexao:
            return []

        cursor = conexao.cursor(dictionary=True)
        try:
            query = """
                SELECT c.CPF, c.Nome, i.Tipo_Investimento, i.Valor_Investido
                FROM Cliente c
                LEFT JOIN Investimento i ON c.CPF = i.CPF_Cliente
                ORDER BY c.Nome
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            conexao.close()