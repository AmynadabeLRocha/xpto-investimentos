from datetime import date
from database import conectar
from models import Cliente


class ClienteRepository:
    """Camada de persistência (Repository Pattern) com operações completas de CRUD no MySQL."""

    # CREATE
    def salvar(self, cliente: Cliente) -> bool:
        conexao = conectar()
        if not conexao:
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute("SELECT CPF FROM Cliente WHERE CPF = %s", (cliente.cpf,))
            if cursor.fetchone():
                print(f"Aviso: Cliente {cliente.nome} (CPF {cliente.cpf}) já está cadastrado.")
                return False

            cursor.execute(
                "INSERT INTO Cliente (CPF, Nome) VALUES (%s, %s)",
                (cliente.cpf, cliente.nome),
            )

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
            return True

        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao salvar cliente no banco: {erro}")
            return False
        finally:
            cursor.close()
            conexao.close()

    # READ (Geral)
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

    # READ (Detalhado por CPF)
    def buscar_por_cpf(self, cpf: str) -> dict | None:
        conexao = conectar()
        if not conexao:
            return None

        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT CPF, Nome FROM Cliente WHERE CPF = %s", (cpf,))
            cliente = cursor.fetchone()
            if not cliente:
                return None

            cursor.execute(
                "SELECT Banco, Agencia, Conta, Saldo, Data_Saldo FROM Conta_Bancaria WHERE CPF_Cliente = %s",
                (cpf,),
            )
            contas = cursor.fetchall()

            cursor.execute(
                "SELECT Tipo_Investimento, Valor_Investido FROM Investimento WHERE CPF_Cliente = %s",
                (cpf,),
            )
            investimentos = cursor.fetchall()

            return {
                "cliente": cliente,
                "contas": contas,
                "investimentos": investimentos,
            }
        finally:
            cursor.close()
            conexao.close()

    # UPDATE
    def atualizar_saldo(self, cpf: str, numero_conta: str, novo_saldo: float) -> bool:
        conexao = conectar()
        if not conexao:
            return False

        cursor = conexao.cursor()
        try:
            hoje = date.today().isoformat()
            cursor.execute(
                """
                UPDATE Conta_Bancaria
                SET Saldo = %s, Data_Saldo = %s
                WHERE CPF_Cliente = %s AND Conta = %s
                """,
                (novo_saldo, hoje, cpf, numero_conta),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao atualizar saldo: {erro}")
            return False
        finally:
            cursor.close()
            conexao.close()

    # DELETE
    def excluir_investimento(self, cpf: str, tipo_investimento: str) -> bool:
        conexao = conectar()
        if not conexao:
            return False

        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                DELETE FROM Investimento
                WHERE CPF_Cliente = %s AND Tipo_Investimento = %s
                """,
                (cpf, tipo_investimento),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            print(f"Erro ao excluir investimento: {erro}")
            return False
        finally:
            cursor.close()
            conexao.close()