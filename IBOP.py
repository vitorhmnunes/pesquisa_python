import os
import unicodedata

class Perguntas: #Classe que determina as informações que serão inseridas pelo usuário
    sexo=''
    idade=''
    fuma=''
    escolaridade=''

def removendo_acentos(linha): #Função que remove os acentos das palavras do arquivo
    normalized = unicodedata.normalize('NFD', str(linha))
    return normalized.encode('ascii', 'ignore').decode('utf8').casefold()

def usando_dicionario(linha): #Função que cria um dicionário e atribui valores para determinados dados do arquivo
    dic = {'feminino' : 1, 'masculino': 2, 'sim': 3, 'nao': 4}
    lista_dic = []
    linha = removendo_acentos(linha).split(' ') #Separação da string retornada pela função 'removendo_acentos' em uma lista de strings
    for i in linha: #Estrutura de repetição para atribuir os valores as suas respctivas chaves
        if i in dic:
            valor = dic.get(i)
        else:
            valor = i
        lista_dic.append(valor)
    return lista_dic

def percentual_mulheres(arquivo, idade): #Função que calcula o percentual de mulheres fumantes acima de 40 anos
    mulheres = 0
    total = 0
    arq = open(arquivo, 'r')
    linha = arq.readline()
    while linha: #Estrutura de repetição que lê uma linha por vez do arquivo e analisa os dados dessa linha
        dados = usando_dicionario(linha)
        if dados[0] == 1 and dados[1] > idade and dados[2] == 3:
            mulheres +=1
        if dados[0] == 1:
            total += 1
        linha = arq.readline()
    arq.close()
    if total > 0:
        mulheres = (mulheres/total)*100
    return mulheres

def percentual_homens(arquivo, idade): #Função que calcula o percentual de homens não fumantes abaixo de 40 anos
    homens = 0
    total = 0
    arq = open(arquivo,'r')
    linha = arq.readline()
    while linha:  #Estrutura de repetição que lê uma linha por vez do arquivo e analisa os dados dessa linha
        dados = usando_dicionario(linha)
        if dados[0] == 2 and dados[1] < idade and dados[2] == 4:
            homens += 1
        if dados[0] == 2:
            total += 1
        linha = arq.readline()
    arq.close()
    if total > 0:
        homens = (homens/total)*100 
    return homens

def percentual_fumantes(arquivo): #Função que calcula o percentual de fumantes em relação ao todo
    fumantes=0
    pessoas = 0
    arq = open(arquivo,'r')
    linha =arq.readline()
    while linha: #Estrutura de repetição para a contagem de pessoas fumantes a partir da leitura das linhas do arquivo
        dados = usando_dicionario(linha)
        if dados[2] == 3:
            fumantes += 1
        pessoas += 1
        linha = arq.readline()
    arq.close()
    if pessoas > 0:
        fumantes= (fumantes/pessoas)*100
    return fumantes

def verificacao_de_existencia(arquivo): #Função que faz a verificação de existência do arquivo
    if os.path.exists(arquivo):
        return True
    else:
        return False

def insercao_arquivo(arquivo,lista): #Função pra inserir dados no arquivo
    if verificacao_de_existencia(arquivo): #Verificação de existência do arquivo. Se existir usa o modo de abertura 'append'. Se não existir usa o modo de abertura 'write' que cria um arquivo
        p=lista[0]
        arq=open(arquivo,"a")
        arq.write(p.sexo + ' ' + str(p.idade) + ' ' + p.fuma + ' ' + p.escolaridade + '\n')
        arq.close()
    else:
        p=lista[0]
        arq=open(arquivo,"w")
        arq.write(p.sexo + ' ' + str(p.idade) + ' ' + p.fuma + ' ' + p.escolaridade + '\n')
        arq.close()

def dados_pessoa(arquivo): #Função que recebe os dados das perguntas do usuário e armzena-os em uma lista com a classe Perguntas
    lista=[]
    p=Perguntas()
    p.sexo=input("Digite o sexo: Feminino ou Masculino? -> ")
    p.idade=input("Digite a idade -> ")
    p.fuma=input("É fumante: sim ou não? -> ")
    p.escolaridade=input("Insira a escolaridade: fundamental, médio ou superior -> ")
    print("Pessoa inserida com sucesso!!!")
    lista.append(p)
    insercao_arquivo(arquivo,lista)

def menu(): #Função que cria um menu, liberando a opção de parada ou de inserção de uma pessoa para o usuário
    print("____________________")
    print("Inserir Pessoa.....1")
    print("Sair...............0")
    op=input("->")
    return op

def main():
    arquivo_pesquisa='pesquisa.txt'
    op=''
    while op != '0': #Estrutura de repetição para análise da opção do menu
        op=menu()
        if op == '1':
            dados_pessoa(arquivo_pesquisa) #Chamada da função para receber os dados do usuário
        elif op == '0':
            print("Saindo...")
        else:
            print("Opção não existente")
    idade='40'
    print('Segue abaixo os dados da pesquisa:')
    if verificacao_de_existencia(arquivo_pesquisa):
        print(f'Percentual de fumantes em relação ao número total de pessoas entrevistadas: {percentual_fumantes(arquivo_pesquisa)}%')
        print(f'Percentual de homens não fumantes abaixo de 40 anos, em relação ao número total de homens entrevistados: {percentual_homens(arquivo_pesquisa, idade)}%')
        print(f'Percentual de mulheres fumantes acima de 40 anos em relação ao número total de mulheres entrevistadas: {percentual_mulheres(arquivo_pesquisa, idade)}%')
    else:
        print('Erro, arquivo da pesquisa, não existente')

main()