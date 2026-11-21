from models import (
    Administrador,
    Cliente,
    ContaBancaria,
    Contato,
    Email,
    Funcionario,
    Investimento,
    Telefone,
)


def executar_simulacao():
    # 1. Instanciando Cliente e seus objetos compostos
    cliente1 = Cliente("111.222.333-44", "Carlos Mendes", "carlos.mendes", "senha123")
    cliente1.adicionar_telefone(Telefone("(61) 99999-1111", "Celular"))
    cliente1.adicionar_email(Email("carlos.mendes@email.com"))

    conta1 = ContaBancaria("Banco do Brasil", "1234-5", "98765-0", 15400.50, "2026-11-21")
    conta1.depositar(600.00)
    cliente1.adicionar_conta(conta1)

    cliente1.adicionar_investimento(Investimento("Tesouro Selic", 10000.00))
    cliente1.adicionar_investimento(Investimento("CDB Liquidez Diária", 5000.00))

    # 2. Instanciando Funcionário, Administrador e registrando Contato
    consultora = Funcionario(1, "Ana Paula Souza", "ana.souza", "admin456", "Consultora Sênior")
    admin = Administrador("Roberto Lima", "roberto.admin", "root789")

    atendimento = Contato(
        cliente=cliente1,
        funcionario=consultora,
        forma_contato="Telefone",
        data_contato="2026-11-20",
        produto_assunto="Aporte Tesouro Selic",
    )

    # 3. Exibindo resultados no terminal
    print("=== XPTO INVESTIMENTOS - TESTE DE DOMÍNIO (POO) ===")
    print(f"Login Carlos válido? {cliente1.autenticar('senha123')}")
    print(f"Cliente: {cliente1.nome} | CPF: {cliente1.cpf}")
    print(f"Contato principal: {cliente1.telefones[0]} | {cliente1.emails[0]}")
    print(f"Saldo atualizado em conta: R$ {cliente1.contas[0].saldo:,.2f}")
    print(f"Total investido (Cliente): R$ {cliente1.calcular_patrimonio_investido():,.2f}")
    print(f"Total sob gestão (Admin {admin.nome}): R$ {admin.gerar_resumo_carteira([cliente1]):,.2f}")
    print("\n--- Histórico de Atendimento ---")
    print(atendimento.resumo_atendimento())


if __name__ == "__main__":
    executar_simulacao()