import json
import os

contatos_suportados = ("telefone", "email", "endereco")

def contato_para_texto(nome_contato: str, **formas_contato):  
    formato_texto = f"{nome_contato}"
    for meio_contato, contato in formas_contato.items():
        formato_texto = f"{formato_texto}\n{meio_contato.upper()}"
        contador_formas = 1
        for valor in contato:
            formato_texto = f"{formato_texto}\n\t{contador_formas} - {valor}"
            contador_formas = contador_formas + 1
    return formato_texto


def agenda_para_texto(**agenda_completa):
   
    formato_texto = ""
    for nome_contato, formas_contato in agenda_completa.items():
        formato_texto = f"{formato_texto}{contato_para_texto(nome_contato, **formas_contato)}\n"
        formato_texto = f"{formato_texto}--------------------------------\n"
    return formato_texto


def altera_nome_contato(agenda_original: dict, nome_original: str, nome_atualizado: str):
    
    if nome_original in agenda_original.keys():
        copia_contatos = agenda_original[nome_original].copy()
        agenda_original.pop(nome_original)
        agenda_original[nome_atualizado] = copia_contatos
        return True
    return False


def altera_forma_contato(lista_contatos: list, valor_antigo: str, novo_valor: str):
   
    if valor_antigo in lista_contatos:
        posicao_valor_antigo = lista_contatos.index(valor_antigo)
        lista_contatos.pop(posicao_valor_antigo)
        lista_contatos.insert(posicao_valor_antigo, novo_valor)
        return True
    return False


def exclui_contato(agenda: dict, nome_contato: str):
    
    if nome_contato in agenda.keys():
        agenda.pop(nome_contato)
        return True
    return False


def inclui_contato(agenda: dict, nome_contato: str, **formas_contato):
          
    agenda[nome_contato] = formas_contato


def inclui_forma_contato(formas_contato: dict, forma_incluida: str, valor_incluido: str):

    if forma_incluida in formas_contato.keys():
        formas_contato[forma_incluida].append(valor_incluido)
        return True
    elif forma_incluida in contatos_suportados:
        formas_contato[forma_incluida] = [valor_incluido]
        return True
    return False


def usuario_inclui_contato(agenda: dict):
    
    nome = input("Informe o nome do novo contato que será inserido na agenda: ")
    if nome.isdigit():
        print("❌Erro: Por favor, digite um nome válido (não apenas números).")   
    else:    
        dicionario_formas = {}
        for forma in contatos_suportados:
            resposta = input(f"Deseja inserir um {forma} para para {nome.upper()}? \nSIM ou NÃO ->")
            lista_contatos = []

            while "S" in resposta.upper():
                lista_contatos.append(input(f"Informe um {forma}: "))
                print("✅Inclusão bem sucedida!\n")
                resposta = input(f"Deseja inserir outro {forma} para {nome.upper()}?\n SIM ou NÃO -> ")   
                    
                if lista_contatos:  
                        dicionario_formas[forma] = lista_contatos.copy()
                                                  
                if dicionario_formas:  
                            inclui_contato(agenda, nome, **dicionario_formas)
                else:
                    print("É necessário incluir pelo menos uma forma de contato!\nA agenda não foi alterada.\n11")              
               
               
def usuario_inclui_forma_contato(agenda: dict):
    
    nome = input("Informe o nome do contato para o qual deseja incluir uma forma de contato: ")
    if nome not in agenda.keys():
            print("❌Erro: Este nome não se encontra na lista.")
                         
    if nome in agenda.keys():      
        print(f"As formas de contato suportadas pelo sistema são: {contatos_suportados}")
        forma_incluida = input("Qual a forma de contato deseja incluir?\n ")
        if forma_incluida.isdigit():
                print("❌Erro: Por favor, digite um contato suportado.")   
        else:
            if forma_incluida in contatos_suportados:
                valor_incluido = input(f"Informe o {forma_incluida} que deseja incluir: ")
                if inclui_forma_contato(agenda[nome], forma_incluida, valor_incluido):
                    print("✅Operação bem sucedida! A nova forma de contato foi incluida!\n ")
            else:
                    print("❌Erro: A forma de contato informada não é suportada.\n")
                

def usuario_exclui_contato(agenda: dict):
    nome = input("Informe o nome do contato que deseja excluir: ")
    if nome.isdigit():
        print("❌Erro: Por favor, digite um nome válido (não apenas números).")
    if exclui_contato(agenda, nome):
        print("✅Usuário excluido com sucesso!")
    else:
        print("❌Nome do usuário não localizado na agenda. Não foram feitas alterações.")


def usuario_altera_nome_contato(agenda: dict):
    nome_original = input("Informe o nome do contato que deseja alterar: ")
    nome_atualizado = input("Informe o nome do novo contato: ")
    if nome_atualizado.isdigit():
        print("❌Erro: Por favor, digite um nome válido (não apenas números).")
    if altera_nome_contato(agenda, nome_original, nome_atualizado):
        print(f"✅O contato foi atualizado e agora se chama {nome_atualizado}.")
    else:
        print(f"❌O contato original não foi localizado. A agenda não foi alterada.")


def usuario_altera_forma_contato(agenda: dict):
    nome = input("Informe o nome do contato que deseja alterar: ")
    if nome.isdigit():
        print("❌Erro: Por favor, digite um nome válido (não apenas números).")
    if nome in agenda.keys():
        print(f"As formas de contato suportadas pelo sistema são: {contatos_suportados}")
        forma_incluida = input("Qual forma de contato deseja incluir?")
        if forma_incluida in contatos_suportados:
            print(contato_para_texto(nome, **agenda[nome]))
            valor_antigo = input(
                f"Informe o {forma_incluida} que deseja alterar")
            nova_valor = input(f"Informe o novo {forma_incluida}")
            if altera_forma_contato(agenda[nome][forma_incluida], valor_antigo, nova_valor):
                print("✅Contato alterado com sucesso!")
            else:
                print("Ocorreu um erro durante a alteração do contato. A agenda não foi alterada.")
        else:
            print(f"{forma_incluida} não é uma forma de contato suportada pelo sistema. A agenda não foi alterada.")
    else:
        print(f"O contato {nome} não está na agenda. A agenda não foi alterada.")


def usuario_contato_para_texto(agenda: dict):
    nome = input("Informe o nome do contato que deseja exibir: ")
    if nome.isdigit():
        print("❌Erro: Por favor, digite um nome válido (não apenas números).")
    if nome in agenda.keys():
        print(contato_para_texto(nome, **agenda[nome]))
    else:
        print("O contato informado não está na agenda.")


def agenda_para_txt(nome_arquivo: str, agenda):
    if "txt" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(agenda_para_texto(**agenda))
        print("✅Agenda exportada com sucesso")


def json_para_agenda(nome_arquivo: str):
    if not os.path.isfile(nome_arquivo):
        print(f"❌ Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    print("✅Agenda carregada com sucesso!")
    return json.loads(conteudo)
   

def agenda_para_json(nome_arquivo: str, agenda):
    if ".json" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.json"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(agenda, indent=4, ensure_ascii=False))
        print("✅Agenda exportada com sucesso!!")


def exibemenu():
    print("""_______________________MANIPULADOR DE AGENDA_______________________ """)
    print("1 - Incluir contato na agenda")
    print("2 - Incluir uma forma de contato")
    print("3 - Alterar o nome de um contato")
    print("4 - Alterar uma forma de contato")
    print("5 - Exibir um contato")
    print("6 - Exibir toda a agenda")
    print("7 - Excluir toda a agenda")
    print("8 - Exportar agenda para txt")
    print("9 - Exportar agenda para JSON")
    print("10 - Importar agenda de JSON")
    print("11 - Sair")
    print("""____________________________________________________________________ """)


def manipular_agenda():
    agenda = {}
    op = 1
    while op != 11:
        exibemenu()
        while True:
            try:
                op = int(input("Informe a opção desejada: "))
                break
            except ValueError:
                print("❌ Erro: Por favor, digite apenas algumas das opções disponíveis.")
        if op == 1:
            usuario_inclui_contato(agenda)

        elif op == 2:
            usuario_inclui_forma_contato(agenda)

        elif op == 3:
            usuario_altera_nome_contato(agenda)

        elif op == 4:
            usuario_altera_forma_contato(agenda)

        elif op == 5:
            usuario_contato_para_texto(agenda)

        elif op == 6:
            print(agenda_para_texto(**agenda))

        elif op == 7:
            usuario_exclui_contato(agenda)

        elif op == 8:
            nome_arquivo = input("Informe o nome do arquivo: ")
            agenda_para_txt(nome_arquivo, agenda)
        elif op == 9:
            nome_arquivo = input("Informe o nome do arquivo: ")
            agenda_para_json(nome_arquivo, agenda)

        elif op == 10:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda = json_para_agenda(nome_arquivo)

        elif op == 11:
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida! Informe uma opção existente.")

manipular_agenda()
