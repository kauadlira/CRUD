import sqlite3  # Biblioteca do Sqlite3
import math
import os
import time
import getpass

def numero(a, c, d):
    n = 0
    while n != 1:
        b = input(c)
        if d == 1: #0, all
            if b != '0' and b != 'all':
                if len(b) == a and b.isnumeric():
                    n = 1
                else:
                    print("Formato incorreto! [{} numeros]".format(a))
            else:
                n = 1

        elif d == 3:
            if len(b) == a and b.isnumeric():
                n = 1
            else:
                print("Formato incorreto! [{} numeros]".format(a))
                n = 0
    return b

def filtro_SN(t):
    SN = 0
    while SN == 0:
        a = input(t).upper()
        if a == 'S':
            SN = 1
        elif a == 'N':
            SN = 1
        else:
            print("Opcao invalida [S/N] ")
    return a

def header(a, b):
    print("-*-"*b, "\n| {} |".format(a))
    print("-*-"*b)

def all():
    cursor.execute("select fz, modelo, variante, pais from caminhoes where id = {}".format(id))
    print("-*-" * 14)
    for linha in cursor.fetchall():
        print("|", linha, "|")
        print("-*-" * 14)

conn = sqlite3.connect("ProjetoDB.db")
cursor = conn.cursor()
cursor.execute('CREATE TABLE if not exists "caminhoes" ("fz"	integer NOT NULL, "modelo" varchar(30), "variante" integer, "pais" varchar(30), "id" integer);')
cursor.execute('CREATE TABLE if not exists "login"("usuario" varchar(20) NOT NULL, "senha" varchar(20) NOT NULL, "id" INTEGER NOT NULL, PRIMARY KEY("id"));')
conn.close()

crud = 'S'
while crud == 'S':
    continual = 'S'
    while continual == 'S':
        header("LOGIN", 3)
        print("\n[1]Fazer login\n[2]Novo usuário\n[0]Sair")
        entrada = input("\nOpção desejada: ")
        while entrada not in "1, 2, 0":
            entrada = str(input("Opção invalida, ação deseja realizar? "))
        conn = sqlite3.connect("ProjetoDB.db")
        cursor = conn.cursor()
        if entrada == '1':
            os.system('cls')
            header("LOGIN", 3)
            login = input("\nLogin: ")
            senha = getpass.getpass("senha: ")
            cursor.execute("select usuario, senha, id, count(*) from login where usuario = '{}'".format(login))
            lg = cursor.fetchone()
            if login == lg[0] and senha == lg[1]:
                id = lg[2]
                print("Login efetuado com sucesso!")
                time.sleep(2)
                continual = 'N'
            else:
                print("Login ou senha inválidos")
                time.sleep(2)
                os.system('cls')
        elif entrada == '2':
            os.system('cls')
            header("CADASTRO", 4)
            nvuser = input("\nLogin: ")
            nvsenha = input("Senha: ")
            cursor.execute("select count(*) from login where usuario = '{}'".format(nvuser))
            lg = cursor.fetchone()
            if lg[0] == 0:
                cursor.execute("select max(id) from login")
                idfetch = cursor.fetchone()
                if idfetch[0] is None:
                    cursor.execute("insert into login values ('{}', '{}', 0)".format(nvuser, nvsenha))
                else:
                    cursor.execute("insert into login values ('{}', '{}', {})".format(nvuser, nvsenha, idfetch[0] + 1))
                conn.commit()
                print("Usuário cadasrado!")            
            else:
                print("Usuario já cadastrado")
            time.sleep(2)
            os.system('cls')
        elif entrada == '0':
            exit()
        conn.close()

    continua1 = 'S'
    while continua1 == 'S':
        os.system("cls")
        header("MENU PRINCIPAL, ID {}".format(id), 8)
        print("\n[1]Cadastro\n[2]Busca\n[3]Apagar\n[4]Alterar\n[5]Alterar Usuário\n[0]Sair")
        opcao = str(input("\nQual açao deseja realizar? "))
        while opcao not in "1, 2, 3, 4, 5, 0":
            opcao = str(input("Opção invalida, ação deseja realizar? "))

        #Sair
        if opcao == "0":
            exit()

        #Cadastro
        if opcao == "1":
            continua = 'S'
            while continua == 'S':
                conn = sqlite3.connect("ProjetoDB.db")
                cursor = conn.cursor()
                # FZ
                os.system("cls")
                header("CADASTRO DE VEÍCULOS", 8)
                fz = numero(6, "\nQual o FZ do veículo? [0 para voltar]: ", 1)
                if fz == 'all':
                    all()
                    time.sleep(3)
                else:
                    if fz != '0'and fz != 'all' :
                        cursor.execute("select count(*) from caminhoes where fz = {} and id = {}".format(fz, id))
                        rs = cursor.fetchone()
                        while rs[0] != 0 and continua == 'S':
                            fz = numero(6, "FZ já existente!, Digite novamente: [0 para voltar] ", 1)
                            if fz != '0':
                                cursor.execute("select count(*) from caminhoes where fz = {} and id = {}".format(fz, id))
                                rs = cursor.fetchone()
                            else:
                                continua = 'N'


                        if fz != '0':
                            vmodelo = input("Qual o modelo do veículo?: ")
                            vvariante = numero(4, "Qual a variante do veículo?: ", 3)
                            vpais = input("Qual o país do veículo?: ")


                            SN = 0
                            while SN == 0:
                                vconfirma = input("Deseja cadastrar o veículo? [S/N]: ").upper()
                                if vconfirma == 'S':
                                    SN = 1
                                    cursor.execute("insert into caminhoes values ({}, '{}', {}, '{}', {})".format(fz, vmodelo, vvariante, vpais, id))
                                    conn.commit()
                                    print("Veículo Cadastrado!")
                                    continua = filtro_SN("\nDeseja cadastrar outro veículo? [S/N]: ")
                                elif vconfirma == 'N':
                                    SN = 1
                                    continua = filtro_SN("\nVeículo não cadastrado, deseja cadastrar outro veículo? [S/N]: ")
                                else:
                                    print("\nOpcão invalida [S/N]")
                    else:
                        continua = 'N'
                    os.system("cls")
                    conn.close()

        #Busca
        if opcao == "2":
            continua = 'S'
            busca = 0
            while continua == 'S':
                conn = sqlite3.connect("ProjetoDB.db")
                cursor = conn.cursor()
                
                if busca != '2':
                    os.system("cls")
                header("BUSCA DE VEÍCULOS", 7)
                busca = input("\n[1]Procurar por FZ\n[2]Ver todos\n[0]Voltar\nEscolha uma opcao:")
                if busca not in "1, 2, 0":
                    print("opção invalida\n")
                else:
                    if busca == '1':
                        fz = numero(6, "\nQual FZ deseja procurar no DB?:", 3)
                        cursor.execute("select count(*) from caminhoes where fz = {} and id = {}".format(fz, id))
                        rs = cursor.fetchone()
                        if rs[0] > 0:
                            os.system("cls")
                            header("BUSCA DE VEÍCULOS", 7)
                            cursor.execute("select fz, modelo, variante, pais from caminhoes where fz ={} and id = {}".format(fz, id))
                            rs = cursor.fetchone()
                            print("\nFZ = {}\nModelo = {} \nVariante = {} \nPaís = {}".format(rs[0], rs[1], rs[2], rs[3]))
                            continua = filtro_SN("Deseja realizar outra busca? [S/N]: ")
                        else:
                            continua = filtro_SN("FZ inexistente, deseja realizar outra busca? [S/N]: ")
                    if busca == '2':
                        all()
                            
                    if busca == '0':
                        continua = 'N'
                conn.close()
                


        #Apagar
        if opcao == "3":
            continua = 'S'
            while continua == 'S':
                os.system("cls")
                header("APAGAR VEÍCULOS", 6)
                conn = sqlite3.connect("ProjetoDB.db")
                cursor = conn.cursor()
                fz = numero(6, "\nQual FZ deseja deletar no DB? [0 para voltar]: ", 1)
                if fz == 'all':
                    all = filtro_SN("\nCuidado! Deseja apagar TODO o banco de dados? [S/N]: ")
                    if all == 'S':
                        trysenha = getpass.getpass("Digite a senha de administrador: ")
                        if trysenha == senha:
                            cursor.execute("delete from caminhoes")
                            conn.commit()
                            print("voce apagou tudo, ta feliz agora? ")
                            time.sleep(2)
                elif fz != 'all' and fz != '0':
                    cursor.execute("select count(*) from caminhoes where fz = {} and id = {}".format(fz, id))
                    rs = cursor.fetchone()
                        
                    if rs[0] != 0:
                        cursor.execute("select count(*), modelo, variante, pais from caminhoes where fz ={} and id = {}".format(fz, id))
                        rs = cursor.fetchone()
                        print("Modelo = {} \nVariante = {} \nPaís = {}".format(rs[1], rs[2], rs[3]))

                        SN = 0
                        while SN == 0:
                            confirma = input("Deseja apagar o veículo? [S/N]: ").upper()
                            if confirma == 'S':
                                cursor.execute("delete from caminhoes where fz = {} and id = {}".format(fz, id))
                                conn.commit()
                                continua = filtro_SN("\nO veículo foi apagado! deseja apagar outro veículo? [S/N]: ")
                                SN = 1
                            elif confirma == 'N':
                                continua = filtro_SN("\nO veículo nao foi apagado, Deseja apagar outro veículo? [S/N]: ")
                                SN = 1
                            else:
                                print("\nOpcão invalida [S/N]")
                    else:
                        continua = filtro_SN("FZ inexistente, deseja apagar outro veículo? [S/N]: ")
                    conn.close()
                else:
                    continua = 'N'

        #Alterar
        if opcao == "4":
            continua = 'S'
            while continua == 'S':
                os.system("cls")
                header("ALTERAÇÃO DE VEÍCULOS", 8)
                conn = sqlite3.connect("ProjetoDB.db")
                cursor = conn.cursor()
                fz = numero(6, "\nQual FZ deseja Modificar no DB? [0 para voltar]: ", 1)
                if fz == 'all':
                    all()
                    time.sleep(3)
                elif fz != 'all':
                    if fz != '0':
                        cursor.execute("select count(*), modelo, variante, pais from caminhoes where fz ={} and id = {}".format(fz, id))
                        rs = cursor.fetchone()
                        if rs[0] > 0:
                            print(
                                "[1]Modelo = {} \n[2]Variante = {} \n[3]País = {} \n[0]Procurar outro FZ".format(rs[1], rs[2], rs[3]))
                            opcao = input("Qual dado voce quer modificar? ")
                            while opcao not in "1, 2, 3, 0":
                                opcao = input("Opção invalida, Qual dado voce quer modificar? ")
                            if opcao == '1':
                                update = 'modelo'
                            elif opcao == '2':
                                update = 'variante'
                            elif opcao == '3':
                                update = 'pais'

                            if opcao != '0':
                                vnovo = input("Qual o novo valor a ser inserido? ")
                                cursor.execute("update caminhoes set {} = '{}' where fz ={} and id = {}".format(update, vnovo, fz, id))
                                conn.commit()
                                cursor.execute("select count(*), modelo, variante, pais from caminhoes where fz ={} and id = {}".format(fz, id))
                                rs = cursor.fetchone()
                                print(
                                    "Os novos dados são: \nModelo = {}  Variante = {}   País = {}".format(rs[1], rs[2], rs[3]))

                                continua = filtro_SN("\nDeseja modificar outro veículo? [S/N]: ")
                            else:
                                continua = 'S'
                        else:
                            conn.close()
                            continua = filtro_SN("\nFz nao encontrado, deseja modificar outro veículo? [S/N]: ")
                    else:
                        continua = 'N'

                conn.close()
        elif opcao == '5':
            continua1 = 'N'
            os.system('cls')
            

