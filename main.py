
import textwrap

# --- FUNÇÕES DE CADASTRO E BUSCA ---

def filtrar_usuario(cpf, usuarios):
    """Filtra um usuário na lista de usuários com base no CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    """Permite o cadastro de um novo usuário, validando se o CPF já existe."""
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Erro! Já existe usuário com este CPF. @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print("\n=== Usuário criado com sucesso! ===")

def criar_conta(agencia, numero_conta, usuarios, contas):
    """Cria uma nova conta para um usuário existente."""
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n@@@ Erro! Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    contas.append({
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario
    })
    print("\n=== Conta criada com sucesso! ===")


# --- FUNÇÕES DAS OPERAÇÕES BANCÁRIAS ---

def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito em uma conta.
    Argumentos aceitos apenas por posição (positional-only).
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\t\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """
    Realiza um saque de uma conta.
    Argumentos aceitos apenas por nome (keyword-only).
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, *, extrato):
    """
    Exibe o extrato da conta.
    Argumentos: saldo por posição, extrato por nome (keyword-only).
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\t\tR$ {saldo:.2f}")
    print("==========================================")

# --- FUNÇÃO PRINCIPAL ---

def main():
    """Função principal que gerencia o fluxo do programa."""
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        menu = """\n
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [nu] Novo Usuário
        [nc] Nova Conta
        [q] Sair
        => """
        
        opcao = input(textwrap.dedent(menu))

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: R$ "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: R$ "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            criar_conta(AGENCIA, numero_conta, usuarios, contas)
            numero_conta += 1

        elif opcao == "q":
            print("\nObrigado por usar nosso sistema bancário. Até mais!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# Executa o programa
if __name__ == "__main__":
    main()