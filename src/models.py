class Usuario:
    """Classe base (superclasse) para todos os perfis de acesso do sistema."""

    def __init__(self, nome: str, login: str, senha: str):
        self.nome = nome
        self.login = login
        self._senha = senha  # Atributo protegido (encapsulamento)

    def autenticar(self, senha_informada: str) -> bool:
        return self._senha == senha_informada

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> bool:
        if self.autenticar(senha_atual):
            self._senha = nova_senha
            return True
        return False


class Telefone:
    def __init__(self, numero: str, tipo: str = "Celular"):
        self.numero = numero
        self.tipo = tipo

    def __str__(self) -> str:
        return f"{self.numero} ({self.tipo})"


class Email:
    def __init__(self, endereco: str):
        self.endereco = endereco

    def __str__(self) -> str:
        return self.endereco


class ContaBancaria:
    def __init__(self, banco: str, agencia: str, conta: str, saldo: float = 0.0, data_saldo: str = ""):
        self.banco = banco
        self.agencia = agencia
        self.conta = conta
        self._saldo = saldo
        self.data_saldo = data_saldo

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do depósito deve ser maior que zero.")
        self._saldo += valor

    def sacar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do saque deve ser maior que zero.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para realizar o saque.")
        self._saldo -= valor


class Investimento:
    def __init__(self, tipo_investimento: str, valor_investido: float):
        self.tipo_investimento = tipo_investimento
        self.valor_investido = valor_investido


class Cliente(Usuario):
    """Herda de Usuario e agrega contatos, contas bancárias e investimentos."""

    def __init__(self, cpf: str, nome: str, login: str, senha: str):
        super().__init__(nome, login, senha)
        self.cpf = cpf
        self.telefones: list[Telefone] = []
        self.emails: list[Email] = []
        self.contas: list[ContaBancaria] = []
        self.investimentos: list[Investimento] = []

    def adicionar_telefone(self, telefone: Telefone) -> None:
        self.telefones.append(telefone)

    def adicionar_email(self, email: Email) -> None:
        self.emails.append(email)

    def adicionar_conta(self, conta: ContaBancaria) -> None:
        self.contas.append(conta)

    def adicionar_investimento(self, investimento: Investimento) -> None:
        self.investimentos.append(investimento)

    def calcular_patrimonio_investido(self) -> float:
        return sum(inv.valor_investido for inv in self.investimentos)


class Funcionario(Usuario):
    """Herda de Usuario e representa os consultores de atendimento."""

    def __init__(self, id_funcionario: int, nome: str, login: str, senha: str, cargo: str = "Consultor"):
        super().__init__(nome, login, senha)
        self.id_funcionario = id_funcionario
        self.cargo = cargo


class Administrador(Usuario):
    """Herda de Usuario com permissões de gestão e relatórios consolidados."""

    def __init__(self, nome: str, login: str, senha: str, nivel_acesso: str = "Total"):
        super().__init__(nome, login, senha)
        self.nivel_acesso = nivel_acesso

    def gerar_resumo_carteira(self, clientes: list[Cliente]) -> float:
        return sum(cliente.calcular_patrimonio_investido() for cliente in clientes)


class Contato:
    """Classe associativa que conecta Cliente e Funcionario (relacionamento N:N)."""

    def __init__(
        self,
        cliente: Cliente,
        funcionario: Funcionario,
        forma_contato: str,
        data_contato: str,
        produto_assunto: str,
    ):
        self.cliente = cliente
        self.funcionario = funcionario
        self.forma_contato = forma_contato
        self.data_contato = data_contato
        self.produto_assunto = produto_assunto

    def resumo_atendimento(self) -> str:
        return (
            f"[{self.data_contato}] {self.forma_contato} | "
            f"Cliente: {self.cliente.nome} | Consultor: {self.funcionario.nome} | "
            f"Assunto: {self.produto_assunto}"
        )