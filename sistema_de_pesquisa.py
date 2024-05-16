
import os
import sys
from funcoes import *
argumentos=[]
argumento =sys.argv[1:]
valor=0
codigo=0

comando = argumento[0].lower()
resto=' '.join(argumento[1:])

argumentos.append(comando.lower())
argumentos.append(resto)
#MOMENTO DA VALIDAÇÃO
codigo=valida(argumentos)
if type(codigo) == tuple:
    valor=codigo[1]
'''CASO SEJA UMA TUPLA ELE USA VALOR COMO VARIAVEL AUXILIAR
PARA VERIFICAR SE ESTÁ ALI DENTRO DA LISTA DE CODIGOS DE ERRO
'''

codigos_erro=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

#VERIFICA SE O CODIGO É DE ERRO E SE FOR OPERARIONALIZA
if codigo in codigos_erro or valor in codigos_erro:
    print_ajuda(codigo)
    arquivos=adicionados()
    sumiram=apagados(arquivos)
    '''PARA CASO TENHA ARQUIVOS PARA DELETAR, PERMITIR O PROGRAMA CONTINUAR A RODAR'''
    if len(sumiram) and argumentos[0]=='delete' or valor==14:
        codigo=valor=16
    #MUDA O VALOR POIS DEU ERRO E JA ENTROU AQUI, NÃO DEVE ENTRAR NOS OUTROS LOCAIS
    else:
        argumentos.insert(0,'pula acoes')
        codigo=valor=16


'''INSTRUMENTOS PARA REALIZAÇÃO DA BUSCA'''
if argumentos[0] == 'buscar':
    indice_invertido = abrir_indice()
    busca(argumentos[1].lower(), indice_invertido)

#CHAMA A FUNÇÃO PARA MOSTRAR ELES'''
elif argumentos[0] == 'listar':
    print_indexados()

#APRESENTA O INDICE INVERTIDO DE MANEIRA ARRUMADA
elif argumentos[0] == 'ver':
    indice_invertido = abrir_indice()
    print_indice(indice_invertido)

#REALIZA INDEXAÇÃO OU ATUALIZAÇÃO DE ARQUIVOS
elif argumentos[0] == 'ler':
    ultimo_indice = ler_index()
    #print(ultimo_indice)
    salvos=adicionados()
    #FUNCIONAMENTO PARA DIRETORIOS
    if os.path.isdir(argumentos[1]):
        arquivos_passados = ler_caminhos(str(fr'{argumentos[1]}'), ultimo_indice)
        '''VERIFICA SE TEM AUTORIZAÇÃO PARA ATUALIZAR SE NÃO SO FAZ O PROCESSO
        DE INDEXAÇÃO COMUM'''
        if devo_atualizar(salvos, arquivos_passados):
            atualizar(argumentos)
            print_indexados()


        if len(salvos)!=len(arquivos_passados):
            new_dir, new_id =adicionar_locais(arquivos_passados, salvos)
            print_indexados()
            indice_invertido = abrir_indice()
            indice_invertido=indice(new_dir, new_id, indice_invertido)
            #print(indice_invertido)
            salvar_indice(indice_invertido)

    #FUNCIONAMENTO PARA ARQUIVOS
    elif os.path.isfile(argumentos[1]):
        teste_indexacao = os.path.abspath(fr'{argumentos[1]}')
        '''VERIFICAÇÃO SE PODE ATUALIZAR OU NAO'''
        if teste_indexacao in salvos:
            atualizar(argumentos)
            
        else:
            aux =fr'{int(ultimo_indice)+1},{os.path.abspath(argumentos[1])}'
            new_dir, new_id =adicionar_locais([aux], salvos)
            print_indexados()
            indice_invertido = abrir_indice()
            indice_invertido=indice(new_dir, new_id, indice_invertido)
            #print(indice_invertido)
            salvar_indice(indice_invertido)

#REALIZA O SCRIPT DE REMOCAO DO PASSADO PELO USER
elif argumentos[0]=='remover':
    arquivos_atuais=abrir_cacheDir()
    remocao, tirar = remover_locais(argumentos[1], arquivos_atuais)
    #TIRAR DA LISTA DE INDEXADOS
    for teste in remocao:
        arquivos_atuais.remove(teste)
    retirar_indexados(arquivos_atuais) 
    indice_invertido = abrir_indice()
    indice_invertido=remover_indice(indice_invertido, tirar) #TIRAR DO INDICE
    salvar_indice(indice_invertido)

#REALIZA PROCEDIMENTO PARA PODER TIRAR OS CONROMPIDOS OU APAGADOS
elif argumentos[0]=='delete':
    arquivos=adicionados()
    sumiram=apagados(arquivos)
    #cam, ident = abrir_caminhos()
    remocao=set()
    tirar=[]
    arquivos_atuais=abrir_cacheDir()
    #PERCORRE A LISTA RECEBIDA DOS ARQUIVOS APAGADOS/MOVIDOS/ALTERADOS NOMES
    for sumiu in sumiram:
        
        mantem, sai = remover_locais(sumiu, arquivos_atuais)
        #print(sai)
        for mant in mantem:
            remocao.add(mant)
        if len(sai)>=1:
            tirar.append(sai[0])
    #print(remocao)
    for teste in remocao:
        arquivos_atuais.remove(teste)
        
    retirar_indexados(arquivos_atuais) 
    indice_invertido = abrir_indice()
    #TIRAR DO INDICE
    indice_invertido=remover_indice(indice_invertido, tirar) 
    salvar_indice(indice_invertido)

#MOSTRA O PRINT DE AJUDA
elif argumentos[0]=='help':
    ajuda()
