from datetime import date
from models import Cliente, ContaBancaria, Email, Investimento, Telefone
from repository import ClienteRepository


def ler_cpf(mensagem: str = "CPF (apenas números): ") -> str:
    while True:
        entrada = input(mensagem).strip()
        digitos = "".join(c for c in entrada if c.isdigit())
        if len(digitos) == 11:
            return f"{digitos[:3]}.{digitos[3:6]}.{digitos[6:9]}-{digitos[9:]}"
        print("CPF inválido. Digite exatamente 11 números (ex: 11122233344).")


def ler_valor_monetario(mensagem: str) -> float:
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if valor < 0:
                print("Digite um valor maior ou igual a zero.")
                continue
            return valor
        except ValueError:
            print("Valor inválido. Digite apenas números (ex: 1500.50).")


def cadastrar_cliente(repo: ClienteRepository):
    print("\n--- Novo Cadastro de Cliente ---")
    cpf = ler_cpf("CPF (apenas números): ")
    nome = input("Nome completo: ").strip()
    login = input("Login de acesso: ").strip()
    senha = input("Senha inicial: ").strip()

    cliente = Cliente(cpf, nome, login, senha)

    telefone = input("Telefone celular: ").strip()
    if telefone:
        cliente.adicionar_telefone(Telefone(telefone, "Celular"))

    email = input("E-mail: ").strip()
    if email:
        cliente.adicionar_email(Email(email))

    print("\n-- Dados da Conta Bancária --")
    banco = input("Banco: ").strip()
    agencia = input("Agência: ").strip()
    conta = input("Número da Conta: ").strip()
    saldo = ler_valor_monetario("Saldo inicial (R$): ")
    cliente.adicionar_conta(ContaBancaria(banco, agencia, conta, saldo, date.today().isoformat()))

    print("\n-- Primeiro Investimento --")
    tipo_inv = input("Produto (ex: Tesouro Selic, CDB): ").strip()
    valor_inv = ler_valor_monetario("Valor aplicado (R$): ")
    cliente.adicionar_investimento(Investimento(tipo_inv, valor_inv))

    if repo.salvar(cliente):
        print(f"\nCliente '{nome}' cadastrado com sucesso no MySQL!")


def listar_carteira(repo: ClienteRepository):
    print("\n--- Carteira Consolidada (MySQL) ---")
    registros = repo.listar_carteira_geral()
    if not registros:
        print("Nenhum registro encontrado.")
        return

    for item in registros:
        valor = f"R$ {item['Valor_Investido']:,.2f}" if item["Valor_Investido"] else "Sem investimentos"
        produto = item["Tipo_Investimento"] or "-"
        print(f"Cliente: {item['Nome']} ({item['CPF']}) | Produto: {produto} | Valor: {valor}")


def consultar_cliente(repo: ClienteRepository):
    cpf = ler_cpf("\nDigite o CPF do cliente (apenas números): ")
    dados = repo.buscar_por_cpf(cpf)
    if not dados:
        print("Cliente não encontrado no banco.")
        return

    cli = dados["cliente"]
    print(f"\n=== Ficha do Cliente: {cli['Nome']} ({cli['CPF']}) ===")

    print("\nContas Bancárias:")
    for c in dados["contas"]:
        print(f"  - {c['Banco']} | Ag: {c['Agencia']} | Conta: {c['Conta']} | Saldo: R$ {c['Saldo']:,.2f}")

    print("\nInvestimentos:")
    if not dados["investimentos"]:
        print("  - Nenhum investimento ativo.")
    for inv in dados["investimentos"]:
        print(f"  - {inv['Tipo_Investimento']}: R$ {inv['Valor_Investido']:,.2f}")


def atualizar_saldo_conta(repo: ClienteRepository):
    print("\n--- Atualizar Saldo Bancário ---")
    cpf = ler_cpf("CPF do cliente (apenas números): ")
    conta = input("Número da conta (ex: 98765-0): ").strip()
    novo_saldo = ler_valor_monetario("Novo saldo (R$): ")

    if repo.atualizar_saldo(cpf, conta, novo_saldo):
        print("Saldo atualizado com sucesso no MySQL!")
    else:
        print("Não foi possível atualizar. Confira se o CPF e o número da conta estão corretos.")


def remover_investimento(repo: ClienteRepository):
    print("\n--- Resgatar / Remover Investimento ---")
    cpf = ler_cpf("CPF do cliente (apenas números): ")
    produto = input("Nome exato do produto (ex: Tesouro Selic): ").strip()

    if repo.excluir_investimento(cpf, produto):
        print("Investimento removido com sucesso do banco!")
    else:
        print("Registro não encontrado. Confira o CPF e o nome do produto.")


def menu_principal():
    repo = ClienteRepository()

    while True:
        print("\n==========================================")
        print("   XPTO INVESTIMENTOS - SISTEMA CRM")
        print("==========================================")
        print("1. Cadastrar novo cliente (Create)")
        print("2. Listar carteira geral (Read)")
        print("3. Consultar ficha por CPF (Read)")
        print("4. Atualizar saldo de conta (Update)")
        print("5. Remover investimento (Delete)")
        print("0. Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_cliente(repo)
        elif opcao == "2":
            listar_carteira(repo)
        elif opcao == "3":
            consultar_cliente(repo)
        elif opcao == "4":
            atualizar_saldo_conta(repo)
        elif opcao == "5":
            remover_investimento(repo)
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Digite um número de 0 a 5.")


if __name__ == "__main__":
    menu_principal()