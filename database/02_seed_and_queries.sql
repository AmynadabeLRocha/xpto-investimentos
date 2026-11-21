USE XPTO_Investimentos;

-- 1. Inserindo registros nas tabelas principais (sem Foreign Key)
INSERT INTO Cliente (CPF, Nome) VALUES 
('111.222.333-44', 'Carlos Mendes'),
('555.666.777-88', 'Mariana Silva');

INSERT INTO Funcionario (Nome_Funcionario) VALUES 
('Ana Paula Souza'),
('Roberto Lima');

-- 2. Inserindo registros dependentes (relacionamentos 1:N)
INSERT INTO Telefone (CPF_Cliente, Numero, Tipo) VALUES 
('111.222.333-44', '(61) 99999-1111', 'Celular'),
('555.666.777-88', '(61) 98888-2222', 'Celular');

INSERT INTO Email (CPF_Cliente, Endereco_Email) VALUES 
('111.222.333-44', 'carlos.mendes@email.com'),
('555.666.777-88', 'mariana.silva@email.com');

INSERT INTO Conta_Bancaria (CPF_Cliente, Banco, Agencia, Conta, Saldo, Data_Saldo) VALUES 
('111.222.333-44', 'Banco do Brasil', '1234-5', '98765-0', 15400.50, '2026-11-21');

INSERT INTO Investimento (CPF_Cliente, Tipo_Investimento, Valor_Investido) VALUES 
('111.222.333-44', 'Tesouro Selic', 10000.00),
('111.222.333-44', 'CDB Liquidez Diária', 5000.00),
('555.666.777-88', 'Fundo Imobiliário', 8500.00);

-- 3. Inserindo na tabela associativa Contato (relacionamento N:N)
INSERT INTO Contato (CPF_Cliente, ID_Funcionario, Forma_Contato, Data_Contato, Produto_Assunto) VALUES 
('111.222.333-44', 1, 'Telefone', '2026-11-20', 'Aporte Tesouro Selic'),
('555.666.777-88', 2, 'E-mail', '2026-11-21', 'Carteira de FIIs');

-- 4. Consultas práticas (simulando os Casos de Uso do sistema)
SELECT c.Nome AS Cliente, i.Tipo_Investimento, i.Valor_Investido
FROM Cliente c
INNER JOIN Investimento i ON c.CPF = i.CPF_Cliente;

SELECT c.Nome AS Cliente, f.Nome_Funcionario AS Consultor, ct.Forma_Contato, ct.Data_Contato, ct.Produto_Assunto
FROM Contato ct
INNER JOIN Cliente c ON ct.CPF_Cliente = c.CPF
INNER JOIN Funcionario f ON ct.ID_Funcionario = f.ID_Funcionario;