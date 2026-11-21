# XPTO Investimentos — Sistema CRM

Sistema de gerenciamento de relacionamento com clientes (CRM) desenvolvido em **Python** e **MySQL** para controle de carteira de investimentos, contas bancárias e histórico de atendimentos. Projeto desenvolvido como entrega do **Projeto Integrador 4**.

## Arquitetura e Tecnologias

* **Linguagem:** Python 3.14+
* **Banco de Dados:** MySQL 8.0 (Modelo Relacional com 7 tabelas)
* **Padrões e Boas Práticas:**
  * **Programação Orientada a Objetos (POO):** Herança (`Usuario` -> `Cliente` e `Funcionario`), encapsulamento e composição (`Cliente` composto por `Telefone`, `Email`, `ContaBancaria` e `Investimento`).
  * **Repository Pattern:** Isolamento da camada de persistência SQL (`src/repository.py`) em relação às regras de domínio (`src/models.py`) e à interface CLI (`src/main.py`).
  * **Segurança:** Gerenciamento de credenciais via variáveis de ambiente (`.env` com `python-dotenv`) e consultas SQL parametrizadas contra SQL Injection.

## Estrutura do Projeto

```text
xpto-investimentos/
├── database/               # Scripts SQL de criação do schema (DDL) e carga inicial (DML)
├── src/
│   ├── models.py           # Classes de domínio e regras de negócio (POO)
│   ├── database.py         # Conexão segura com o MySQL via variáveis de ambiente
│   ├── repository.py       # Camada de persistência com operações CRUD
│   └── main.py             # Interface interativa via terminal (CLI)
├── .env.example            # Modelo de configuração de ambiente
├── .gitignore              # Bloqueio de .venv, cache e credenciais locais
└── requirements.txt        # Dependências do projeto
```

## Funcionalidades (CRUD Interativo)

1. **Create:** Cadastro completo de cliente com conta bancária e primeiro aporte financeiro.
2. **Read (Geral):** Listagem consolidada de toda a carteira de clientes e produtos ativos.
3. **Read (Individual):** Consulta detalhada da ficha do cliente por CPF (com máscara automática a partir dos dígitos).
4. **Update:** Atualização de saldo bancário com registro automático da data de movimentação.
5. **Delete:** Resgate/remoção de ativos da carteira de investimentos.

## Como Executar Localmente

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/AmynadabeLRocha/xpto-investimentos.git](https://github.com/AmynadabeLRocha/xpto-investimentos.git)
   cd xpto-investimentos
   ```

2. **Configurar o banco de dados:**
   * Execute os scripts da pasta `database/` no **MySQL Workbench** para criar o schema `XPTO_Investimentos` e popular os dados iniciais.

3. **Criar e ativar o ambiente virtual:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

4. **Configurar as variáveis de ambiente:**
   * Copie `.env.example` para `.env` na raiz do projeto e preencha com sua senha local do MySQL.

5. **Executar a aplicação:**
   ```powershell
   python src/main.py
   ```