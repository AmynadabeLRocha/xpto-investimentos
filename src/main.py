from models import (
    Cliente,
    ContaBancaria,
    Email,
    Investimento,
    Telefone,
)
from repository import ClienteRepository


def executar_integracao():
    repo = ClienteRepository()

    # 1. Instancia uma nova cliente via POO e grava no MySQL
    nova_cliente = Cliente("999.888.777-66", "Fernanda Costa", "fernanda.costa", "invest2026")
    nova_cliente.adicionar_telefone(Telefone("(61) 97777-3333", "Celular"))
    nova_cliente.adicionar_email(Email("fernanda.costa@email.com"))
    nova_cliente.adicionar_conta(
        ContaBancaria("Nubank", "0001", "54321-9", 22000.00, "2026-11-21")
    )
    nova_cliente.adicionar_investimento(Investimento("LCI Banco Inter", 12000.00))
    nova_cliente.adicionar_investimento(Investimento("Tesouro IPCA+", 6500.00))

    print("=== XPTO INVESTIMENTOS - INTEGRAÇÃO PYTHON + MYSQL ===")
    repo.salvar(nova_cliente)

    # 2. Consulta todos os registros gravados no banco (dados do SQL + dados inseridos via Python)
    print("\n--- Carteira Consolidada no Banco de Dados ---")
    registros = repo.listar_carteira_geral()
    for item in registros:
        valor = f"R$ {item['Valor_Investido']:,.2f}" if item["Valor_Investido"] else "Sem investimentos"
        produto = item["Tipo_Investimento"] or "-"
        print(f"Cliente: {item['Nome']} ({item['CPF']}) | Produto: {produto} | Valor: {valor}")


if __name__ == "__main__":
    executar_integracao()