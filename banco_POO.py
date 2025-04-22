from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def add_conta(self, conta):
        self.contas.append(conta)
    
class Pessoa_fisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        
class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    
    def sacar(self,valor):
        if valor > self._saldo:
            print("Saldo insuficiente")
        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} efetuado com sucesso!")
            return True
        else:
            print("Valor inválido. O valor do saque deve ser maior que zero")
        return False
            
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito de R$ {valor:.2f} efetuado com sucesso!")
 
        else:
            print("Valor inválido")
            return False

        return True


class Conta_Corrente(Conta):
    def __init__(self,numero,cliente,limite = 500,limite_saques = 3):
        super().__init__(numero,cliente)
        self.limite = limite
        self._limite_saques = limite_saques
        
    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        
        if numero_saques >= self._limite_saques:
            print("Limite de saques diários atingido")         
        elif valor > self.limite:
            print("O valor ultrapassa o limite para saque")
        else:
            return super().sacar(valor) #Vai fazer a operacao e retornar True
        return False
    
    def __str__(self):
        return f"""\
            Agência:{self.agencia}
            C/C:{self.numero}
            Titular:{self.cliente.nome}
        """
        
 
class Historico:
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes

    def add_transacao(self,transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        pass
   
class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_saque = conta.sacar(self.valor)
        
        if sucesso_saque:
            conta.historico.add_transacao(self)
    
class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        sucesso_deposito = conta.depositar(self.valor)
        
        if sucesso_deposito:
            conta.historico.add_transacao(self)

def encontra_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    if not clientes_filtrados:
        return None
    else:
        return clientes_filtrados[0] 
    
    
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]
    
    print("\nContas disponíveis:")
    for i, conta in enumerate(cliente.contas):
        print(f"[{i}] Conta número: {conta.numero}")

    while True:
        try:
            escolha = int(input("Digite o numero da conta desejada: "))
            if 0 <= escolha < len(cliente.contas):
                return cliente.contas[escolha]
            else:
                print("@@@ Índice inválido. Tente novamente. @@@")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
        

def depositar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = encontra_cliente(cpf,clientes)
            
    if not cliente:
        print("Cliente não encontrado")
        return
    
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("Valor inválido! Digite um número.")
        return
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("Conta do cliente não encontrada")
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = encontra_cliente(cpf,clientes)
    
    if not cliente:
        print("Cliente não encontrado")
        return
    
    print("Sacar".center(20, "#"))
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("Valor inválido! Digite um número.")
        return
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("Conta do cliente não encontrada")
        return
    
    cliente.realizar_transacao(conta, transacao)
    

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = encontra_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        print("Conta do cliente não encontrada")
        return
    
    print("Extrato".center(20, "#"))
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Nenhuma transação realizada")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']} de R$ {transacao['valor']:.2f} em {transacao['data']}")
        print(f"Saldo atual: R$ {conta.saldo:.2f}")

    
def criar_cliente(clientes):
    cpf = input("Digite o CPF: ")
    cliente = encontra_cliente(cpf, clientes)
    
    if cliente:
        print("Cliente já cadastrado")
        return cliente
    
    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço(logradouro, nro - bairro - cidade/sigla estado): ")
    
    cliente_novo = Pessoa_fisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente_novo)
    print("Cliente cadastrado com sucesso") 

def criar_conta_corrente(clientes,numero_conta,contas):
    cpf = input("Digite o CPF: ")
    cliente = encontra_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado")
        return
    conta = Conta_Corrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("Conta corrente criada com sucesso")

def listar_usuarios(clientes):
    if not clientes:
        print("Nenhum usuário cadastrado")
    else:
        print("Usuários cadastrados:\n")
        for cliente in clientes:
            print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}, Endereço: {cliente.endereco}")
                  
          
def listar_contas_correntes(cliente):
    contas_correntes = cliente.contas
    if not contas_correntes:
        print("Nenhuma conta corrente cadastrada")
    else:
        print("Contas correntes cadastradas:\n")
        for conta_cc in contas_correntes:
            print(conta_cc)
            

def main():
    clientes = []
    contas = []
    
    menu = """
    Escolha uma opcao:
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [u] Criar usuario
    [c] Criar conta corrente
    [lu] Listar usuarios
    [lc] Listar contas correntes
    [q] Sair
    => """

    print("\nBem-vindo ao Banco Richard's Finance")
    while True:

        opcao = input(menu).lower()
        
        if opcao == "d":
            depositar(clientes)
            
        elif opcao == "s":
            sacar(clientes)
            
        elif opcao == "e":
            exibir_extrato(clientes)
            
        elif opcao == "u":
            criar_cliente(clientes)
            
        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta_corrente(clientes, numero_conta, contas)
        
        elif opcao == "lu":
            listar_usuarios(clientes)
            
        elif opcao == "lc":
            cpf = input("Digite o CPF do cliente: ")
            cliente = encontra_cliente(cpf, clientes)
            if cliente:
                listar_contas_correntes(cliente)
            else:
                print("Cliente não encontrado")
        
        elif opcao == "q":
            print("Sair")
            print("Até logo!")
            break 

        else:
            print("Opção inválida. Tente novamente")
            
if __name__ == "__main__":
    main()