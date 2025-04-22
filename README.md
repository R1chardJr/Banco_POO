# Banco_POO


# 💰 Richard's Finance - Sistema Bancário em Python

Este é um sistema bancário simples, orientado a objetos, feito em Python. Ele permite gerenciar **clientes**, **contas correntes**, realizar **depósitos**, **saques**, emitir **extratos**, e muito mais — tudo via terminal.

---

## 📌 Funcionalidades

- ✅ Cadastro de clientes (Pessoa Física)
- ✅ Criação de contas correntes com número automático
- ✅ Realização de **depósitos** e **saques**
- ✅ Emissão de **extrato bancário**
- ✅ Limite de saques diários (3 saques)
- ✅ Listagem de usuários e contas
- ✅ Histórico completo das transações

---

## 🧱 Estrutura de Classes

### `Cliente` e `Pessoa_fisica`
Representa os usuários do banco. Armazena dados como nome, CPF, endereço, data de nascimento e suas contas bancárias.

### `Conta` e `Conta_Corrente`
Representa uma conta bancária genérica (`Conta`) e uma implementação concreta com regras específicas de limite e saques (`Conta_Corrente`).

### `Historico`
Armazena todas as transações (depósitos e saques) realizadas na conta, com data, tipo e valor.

### `Transacao`, `Saque`, `Deposito`
Utiliza o padrão de projeto **Command Pattern**. Cada transação sabe como se registrar no histórico da conta.

---

## ▶️ Como usar

1. Clone o repositório:
```bash
git clone https://github.com/R1chardJr/Banco_POO.git
cd Banco_POO
```

2. Execute o programa:
```bash
python banco_POO.py
```

3. Siga o menu de opções no terminal:
```
Escolha uma opcao:
[d] Depositar
[s] Sacar
[e] Extrato
[u] Criar usuario
[c] Criar conta corrente
[lu] Listar usuarios
[lc] Listar contas correntes
[q] Sair
```

---

## ⚙️ Exemplo de uso

```
Digite o CPF: 12345678900
Digite o nome: Maria Silva
Digite a data de nascimento: 01-01-1990
Digite o endereço: Rua X, 123 - Bairro Y - Cidade Z/SP

Cliente cadastrado com sucesso!
```

---

## 🛠 Requisitos

- Python 3.7+
- Nenhuma biblioteca externa necessária

---

## 🧠 Conceitos aplicados

- Programação Orientada a Objetos (POO)
- Herança e Polimorfismo
- Abstração com `ABC` (Abstract Base Classes)
- Boas práticas de encapsulamento
- Separação de responsabilidades

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Sinta-se à vontade para usar e modificar.

