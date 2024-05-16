'''
/*******************************************************************************
Autor: Rhian Pablo A Almeida
Componente Curricular: Algoritmos I
Concluido em: 02/06/2022
Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
trecho de código de outro colega ou de outro autor, tais como provindos de livros e
apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
******************************************************************************************/
'''
import os
import sys
import pickle


'''LE O QUE TEM NO CAMINHO DOS ARQUIVOS QUE O USUARIO MANDOU E ADD NUMA LISTA'''
'''SO FUNCIONA CASO SEJA UM DIRETORIO'''
def ler_caminhos(local, indice):
    cont = int(indice)
    lista_arquivos = []
    with os.scandir(fr'{local}') as diretorios:
        for entry in diretorios:
            if not entry.name.startswith('.') and entry.is_file() and entry.name.endswith('.txt'):
                cont+=1
                aux=str(fr'{os.path.normcase(os.path.abspath(entry.path))}')
                lista_arquivos.append(fr'{cont},{entry.path}')
    return lista_arquivos


'''============================================================================='''
'''=================FUNÇÕES DE PEGAR O QUE TEM NO TXT==========================='''
'''============================================================================='''

'''PEGA O ULTIMO INDICE DOS ARQUIVOS JA LIDOS'''
def ler_index():
    final = 0
    aux = os.path.abspath(str(r'cache/arquivos.txt'))
    with open(f'{aux}', 'r', encoding='utf-8') as lista:
        linhas = lista.readlines()
    if len(linhas)>=1 and not '\n' in linhas:
        for a in range(len(linhas),(len(linhas)-1),-1):
            aux=linhas[a-1].split(',',1)
            final=aux[0]
    return final


'''RETORNA LISTA COM TODOS OS CAMINHOS JA LIDOS SEM O INDICE'''
def adicionados():
    internos =[]
    with open(r'cache/arquivos.txt', 'r', encoding='utf-8') as arquivo:
        for add in arquivo.readlines():
            aux = add.strip('\n').split(',',1)
            if len(aux)>1:
                internos.append(aux[1])
    return internos


'''ABRE O ARQUIVO DE INDEXADOS E RETORNA A LISTA COM OS INDICES DELES'''
def abrir_cacheDir():
    lista_atual=[]
    with open(fr'cache/arquivos.txt', 'r') as locais:
        for linha in locais.readlines():
            lista_atual.append(linha)
    return lista_atual


'''ABRE A LISTA DE CAMINHOS E RETORNA O INDICE E CAMINHO'''
def abrir_caminhos():
    caminhos=[]
    identificadores=[]
    with open(fr'cache/arquivos.txt', 'r') as locais:
        for linha in locais.readlines():
            aux = linha.split(',',1)
            if len(aux)>1:
                caminhos.append(aux[1].strip('\n'))
                identificadores.append(aux[0])
    return caminhos, identificadores

'''============================================================================='''
'''=================FUNÇÕES DE MAIS EFEITO DENTRO DO PROG======================='''
'''============================================================================='''


'''CONFERE SE JA TEM AQUELE LOCAL, E ESCREVE SE NAO TIVER'''
def adicionar_locais(lista_arquivos, lista_salva):
    novos_caminhos=[]
    novos_indices=[]
    
    with open(r'cache/arquivos.txt', 'a+', encoding='utf-8') as arquivo:
        for arq in lista_arquivos: #PERCORRE OS QUE TEM PARA ENTRAR
            aux = arq.strip('\n').split(',',1)
            if len(lista_salva)>=1:
                for salvo in lista_salva: #PERCORRE OS JA INDEXADOS
                    if os.path.normpath(aux[1]) not in lista_salva :
                        aux1=f'{aux[0]},{aux[1]}\n'
                        arquivo.write(aux1)
                        lista_salva.append(aux[1])
                        novos_caminhos.append(aux[1])
                        novos_indices.append(aux[0])
            elif len(lista_salva)==0 and len(aux)==2:
                aux1=f'{aux[0]},{aux[1]}\n'
                arquivo.write(aux1)
                novos_caminhos.append(aux[1])
                novos_indices.append(aux[0])
    return novos_caminhos, novos_indices


'''REMOVER CAMINHOS JA INDEXADOS'''
def remover_locais(arg, arquivos_atuais):
    #PEGA O CAMINHO ABSOLUTO PASSADO
    aux_loc= os.path.abspath(arg)
    #SALVA PARA REMOVER APOS PERCORRER O FOR DOS ARQUIVOS
    remocao=[] 
    #LISTA COM VALOR DE INDICE
    removidos=[] 
    
    if os.path.isdir(aux_loc): #CASO TENHA PASSADO PASTA
        
        lista_arq = ler_caminhos(aux_loc,0) #PEGA LISTA QUE VAI REMOVER

        for atual in arquivos_atuais: #ARQUIVOS INDEXADOS
            aux_atual = atual.split(',',1)
            for remover in lista_arq: #ARQUIVOS QUE QUER REMOVER
                aux_rem=remover.split(',',1)
                
                if aux_atual[1].strip('\n')==aux_rem[1].strip('\n'):
                    remocao.append(atual)
                    removidos.append(aux_atual[0])

    elif aux_loc.endswith('.txt'): #ARQUIVOS INDEXADOS
    
        for atual in arquivos_atuais:
            aux_atual = atual.split(',',1)
            
            if aux_atual[1].strip('\n')==aux_loc:
                
                remocao.append(atual)
                removidos.append(aux_atual[0])
        
    return remocao, removidos


'''ALGORITMO PARA PEGAR PALAVRAS E NUMEROS PRESENTES EM UM TXT'''
def pega_palavras(arquivo, parcial_palavras, parcial_numeros, palavras_total):
    cont=0
    
    for linha in arquivo:
        cont+=1
        for term in linha:    
            if term.isalpha() or term == "'":
                parcial_palavras.append(term)
            elif term.isdigit():
                parcial_numeros.append(term)
            
            if (not term.isalpha() and len(parcial_palavras)>=1 and term!="'"):
                palavras_total.append((''.join(parcial_palavras)).lower())
                parcial_palavras=[]
            
            elif not term.isalnum() and not term.isdigit() and len(parcial_numeros)>=1:
                palavras_total.append(''.join(parcial_numeros))
                parcial_numeros=[]
        
        #VERIFICA SE JA ACABOU O FOR E SE SIM, ADICIONA OS ULTIMOS ELEMENTOS;
        #SERVE PARA EVITAR NAO PEGAR O ULTIMO ELEMENTO DE UM TXT SE O MESMO ACABAR
        #EM IS ALPHA OU EM IS DIGIT
        if cont==len(arquivo):
            if len(parcial_palavras)>1:
                palavras_total.append((''.join(parcial_palavras)).lower())
            if len(parcial_numeros)>1:
                palavras_total.append((''.join(parcial_numeros)))


'''ATUALIZA O INDICE INVERTIDO'''
def indice(caminhos, ident, ind_ivt):
    cont = 0
    #IDENT SE REFERE AO INDICE DO CAMINHO
    #SO É FEITO O ARMAZENAMENTO DELE NO DICIONARIO

    for caminho in caminhos: #PERCORRE A LISTA DE CAMINHOS DE ARQUIVOS
        palavras=abrir_txt(caminho)
        for palavra in palavras: #PERCORRE AS PALAVRAS DE CADA ARQUIVO
            if palavra in ind_ivt:
                if str(fr'{ident[cont]}') in ind_ivt[palavra]:
                    ind_ivt[palavra][str(fr'{ident[cont]}')]+=1
                    
                    aux_total = ind_ivt[palavra]['total']
                    aux_total+=1
                    ind_ivt[palavra]['total']=aux_total
                elif str(fr'{ident[cont]}') not in ind_ivt[palavra]:
                    ind_ivt[palavra][str(fr'{ident[cont]}')]=1
                    '''ANALISAR NECESSIDADE DESSA VERIFICAÇÃO'''
                    if 'total' in ind_ivt[palavra]:
                        aux_total = ind_ivt[palavra]['total']
                        aux_total+=1
                        ind_ivt[palavra]['total']=aux_total
                    else:
                        ind_ivt[palavra]['total']=1
            elif palavra not in ind_ivt:
                ind_ivt[palavra]={str(fr'{ident[cont]}'): 1, 'total': 1}
        cont+=1
    return ind_ivt


'''VERIFICA SE ALGUM DOS ARQUIVO DENTRE OS PASSADOS JÁ FOI INDEXADO'''
'''SE FOR TRUE, ELE AUTORIZA A CHAMAR O MODULO DE ATUALIZAÇÃO'''
def devo_atualizar(slv, arqs_passados):
    for arq in arqs_passados: #PERCORRE OS ARQUIVOS PARA ENTRAR
        ajudante = arq.strip('\n').split(',',1)[1]
        if ajudante in slv: #VERIFICA SE JA FORAM INDEXADOS
            return True


'''REALIZA O PROCEDIMENTO DE ATUALIZAÇÃO DO INDICE'''
def atualizar(argumentos):
    lista_atualizar, cam_atualizar =oque_atualizar(argumentos)
    '''ATUALIZA NO INDICE INVERTIDO'''
    '''REMOVE E DEPOIS RE-ADICIONA NO INDICE'''
    if len(lista_atualizar)>=1:
        indice_invertido = abrir_indice()
        indice_invertido=remover_indice(indice_invertido, lista_atualizar) #TIRAR DO INDICE
        indice_invertido = indice(cam_atualizar, lista_atualizar, indice_invertido)
        salvar_indice(indice_invertido)


'''ATUALIZAR O DICIONARIO - REMOVENDO ARQUIVOS'''
def remover_indice(ind_ivt, tirar): #PARA ATUALIZAR REMOVENDO CAMINHOS
    copia=ind_ivt.copy()
    #VAI PERCORRER AS CHAVES DO DICIONARIO
    for palavra in copia: 
        copia_loc = copia[palavra].copy()
        #VAI PERCORRER AS CHAVES DO SUBDICIONARIO
        for local in copia_loc: 
            if local != 'total':
                #VAI PERCORRER LISTA DE INDICES QUE TEM QUE REMOVER
                #QUANDO FOR IGUAL ELE REMOVE
                for indices in tirar: 
                    if local == indices:
                        aux = ind_ivt[palavra][local]
                        ind_ivt[palavra].pop(local)
                        aux_total = int(ind_ivt[palavra]['total'])
                        aux_total -=aux
                        ind_ivt[palavra]['total'] =aux_total

                if ind_ivt[palavra]['total'] ==0:
                    ind_ivt.pop(palavra)
    return ind_ivt


'''RECEBE O CAMINHO QUE O USUARIO PASSOU, E SELECIONA O QUE VAI SER ATUALIZADO OU NAO'''
def oque_atualizar(argumentos):
    ultimo_indice = ler_index()
    caminhos, indentificador = abrir_caminhos()
    lista_atualizar = []
    cam_atualizar = []
    if os.path.isdir(argumentos[1]):
        '''PEGA UMA LISTA COM TODOS OS ARQUIVOS PRESENTES DENTRO DAQUELA PASTA'''
        arquivos_passados = ler_caminhos(str(fr'{argumentos[1]}'), ultimo_indice)

        for arquivo in arquivos_passados: #PERCORRE OS ARQUIVOS DENTRO DAQUELA PASTA
            auxiliar = arquivo.strip('\n').split(',',1)
            '''
            VE SE AQUELE CAMINNHO JA FOI INDEXADO, SE SIM, ELE ADICIONA NA LISTA DOS QUE
            VAO SER ATUALIZADOS
            ESSA ROTINA SE REPETE SE O USER PASSOU ARQUIVO, MAS SEM O FOR PARA PERCORRER 
            ARQUIVOS
            '''
            if auxiliar[1] in caminhos:
                indice_fake= caminhos.index(auxiliar[1])
                indice = indentificador[int(indice_fake)]
                lista_atualizar.append(indice)
                cam_atualizar.append(auxiliar[1])
    elif os.path.isfile(argumentos[1]):
        aux = os.path.abspath(argumentos[1])
        
        if aux in caminhos:
            indice_fake= caminhos.index(aux)
            indice = indentificador[int(indice_fake)]
            lista_atualizar.append(indice)
            cam_atualizar.append(aux)
    return lista_atualizar, cam_atualizar


'''REALIZA A BUSCA DE PALAVRAS DENTRO DO DICIONARIO'''
'''FORMATA A SAÍDA DA ESTRUTURA PARA MELHOR APRESENTAÇÃO'''
def busca(argumento, ind_ivt):
    caminho, identificador = abrir_caminhos()
    if argumento in ind_ivt:
        dicio_especifico = ind_ivt[argumento]
        #NESSE MOMENTO É USADO CODIGO PARA PODER ORDENAR O DICIONARIO COM BASE NO VALOR DE SUAS CHAVES
        #ESSE ORDENAMENTO OCORRE NO DICIONARIO DAQUELE TERMO BUSCADO
        organizado = {k: v for k, v in sorted(dicio_especifico.items(), key=lambda item: item[1], reverse=True)}
        print('Apareceu em:')
        for local in organizado:
            if local != 'total':
                indice = identificador.index(local)
                arquivo = os.path.basename(caminho[indice])
                localizacao = os.path.dirname(caminho[indice])
                
                print(fr'{arquivo} com recorrencia de {organizado[local]} vezes')
                print(fr'no local {localizacao}','\n')
            elif local == 'total':
                valor_total = organizado['total']
        print(f'O total de vezes em que apareceu: {valor_total}')
    else:
        print('Não foi encontrada nenhuma aparição desse termo')


'''VERIFICA SE HÁ EXISTENCIA DE ARQUIVOS DELETADOS, OU ALTERAÇÕES
DENTRO DOS ARQUIVOS INDEXADOS, SE HOUVER RETORNA LISTA COM OS ANTIGOS CAMINHOS'''
def apagados(arquivos):
    apagados = []
    cont =0
    while cont <len(arquivos):
        try:
            with open(fr'{arquivos[cont]}','r',errors='ignore') as arquivo:
                leitura = arquivo.readlines()
        except:
            apagados.append(arquivos[cont])
        cont+=1
    return apagados


'''VALIDACAO'''
'''RECEBE AS ENTRADAS DO USUARIO E VALIDA'''
'''PARA CADA CASO, RETORNA UM CODIGO PARA EXIBIR UMA MENSAGEM PERSONALIZADA'''
def valida(argumentos):
    validos = ['ler', 'remover', 'buscar', 'listar', 'help', 'ver', 'delete']
    print('Aguarde, eu(o programa) estou carregando recursos\n')
    if not os.path.isfile(fr'cache/indice.rp11') or not os.path.isfile(fr'cache/arquivos.txt'):
        try:
            with open(fr'cache/arquivo.rp11', 'rb') as dicionario:
                indice = pickle.load(dicionario)
            locais= open(fr'cache/arquivos.txt', 'r')
            locais.close()
        except:
            return 1 #ARQUIVOS DE CACHE APAGADOS OU CONROMPIDOS
    
    if argumentos[0] not in validos:
        return 2 #COMANDO INVALIDO

    if argumentos[0] == 'listar' or argumentos[0]=='help' or argumentos[0]=='ver' or argumentos[0]=='delete':
        #VERIFICA SE DIGITOU MAIS DOQ NECESSARIO PARA FUNCIONAR

        if len(argumentos)>2 or len(argumentos[1])>0:
            
            return 3 #COMANDO INVALIDO
            
    if len(argumentos)>2:
        return 4 #COMANDO INVALIDO

    if argumentos[0]=='ler' or argumentos[0]=='remover':
        if not os.path.isdir(fr'{argumentos[1]}') or not os.path.isfile(fr'{argumentos[1]}'):
            if os.path.isfile(fr'{argumentos[1]}') and not argumentos[1].endswith('.txt'):
                return 10 #ARQUIVO PASSADO NÃO É SUPORTADO

            elif os.path.isfile(fr'{argumentos[1]}') and argumentos[1].endswith('.txt'):
                try:
                    teste = open(fr'{argumentos[1]}', 'r')
                    teste.close() 
                except:
                    return 11 #ARQUIVO PASSADO CONROMPIDO

            if not os.path.isdir(fr'{argumentos[1]}') and not os.path.isfile(fr'{argumentos[1]}'):   
                return 5 #NÃO É NEM PASTA NEM ARQUIVO

        if not os.access(fr'{argumentos[1]}', os.R_OK):
            return 6 #NÃO TEM ACESSO A PASTA PARA REALIZAR LEITURA

        if os.path.isdir(fr'{argumentos[1]}'):
            if argumentos[0]=='ler':
                index_final = ler_index()
                passados=ler_caminhos(fr'{argumentos[1]}', index_final)
                passar=[]
                for quebra in passados:
                    aux=quebra.strip('\n').split(',',1)[1]
                    passar.append(aux)
                sumiu=apagados(passar)
                if len(sumiu)>=1:
                    '''CASO TENHA ALGUM PROBLEMA COM ALGUM DOS ARQUIVOS PASSADOS
                    QUE NAO SEJA POSSIVEL LER, RETORNA UMA LISTA COM ELES'''    
                    return (sumiu, 13) 

    arquivos = adicionados()
    sumiram=apagados(arquivos)
    if argumentos[0]=='delete' and len(sumiram)==0:
        #CASO QUEIRA DELETAR, MAS NÃO TENHA AQUIVOS PARA PERMITIR ISSO
        return 15

    if len(sumiram)>=1:
        #RETORNA LISTA COM OS ARQUIVOS QUE SUMIRAM/DERAM ERRO PARA MOMENTO
        #DO AVISO
        return (sumiram,14)

    if argumentos[0] == 'remover' or argumentos[0]=='atualizar':
        
        if os.path.isfile(fr'{argumentos[1]}') and argumentos[1] not in arquivos and not argumentos[1].endswith('.txt'):   
            return 7 #ARQUIVO NAO FOI INDEXADO AINDA PARA REALIZAR A REMOÇÃO OU ATUALIZAÇÃO
        
        if os.path.isdir(fr'{argumentos[1]}'):
            index_final = ler_index()
            passados=ler_caminhos(fr'{argumentos[1]}', index_final)
            for passado in passados:
                aux = passado.strip('\n').split(',',1)
                if aux[1] not in arquivos:
                    #UM DOS ARQUIVOS PRENSETES NO DIRETORIO NAO FOI INDEXADO AINDA
                    return 12 
    

    if argumentos[0] != 'ler' and argumentos[0]!='help' and len(arquivos)==0:
        #NAO TEM ARQUIVOS INDEXADOS E QUER REALIZAR AÇÃO QUE PEDE ISSO
        return 9 
    
    else:
        #RETORNO AFIRMANDO QUE ESTA TUDO CORRETO
        return 16 

'''===================================================================================='''
'''=========================FUNÇÕES DE ABRIR E FECHAR ARQ=============================='''
'''===================================================================================='''


'''VAI CRIAR A PASTA SE TIVER SIDO APAGADA, OU OS ARQUIVOS SE
TIVEREM SIDO APAGADOS'''
def cria_cache():
    dicionario={}
    if not os.path.isdir('cache'):
        os.mkdir('cache')
    retirar_indexados([])
    salvar_indice(dicionario)
    

'''SALVAR DICIONARIO DO INDICE INVERTIDO'''
def salvar_indice(indice_invertido):
    with open(fr'cache/indice.rp11', 'wb') as dicio:
        pickle.dump(indice_invertido, dicio)


'''ABRE O BINARIO DO DICIONARIO DO INDICE INVERTIDO'''
def abrir_indice():
    if os.path.isfile(fr'cache/indice.rp11'):
        with open(fr'cache/indice.rp11', 'rb') as dicionario:
            indice = pickle.load(dicionario)
        return indice
    else:
        return 'arquivo inexistente'


'''ABRE O TXT E DEVOLVE UMA LISTA DE PALAVRAS'''
def abrir_txt(caminho):
    parcial_palavras=[]
    parcial_numeros=[]
    palavras_total=[]
    try:
        with open(fr'{caminho}', 'r', encoding='utf-8') as arquivos:
            arquivo=arquivos.readlines()
            
            pega_palavras(arquivo, parcial_palavras, parcial_numeros, palavras_total)
    #CASO OCORRA EXCEÇÃO POR TER TENTADO LER UTF-8
    except UnicodeDecodeError:
        with open(fr'{caminho}', 'r', errors='ignore') as arquivos:
            arquivo=arquivos.readlines()
            pega_palavras(arquivo, parcial_palavras, parcial_numeros, palavras_total)
    return palavras_total


'''RECRIA O ARQUIVO COM OS INDEXADOS, E ESCREVE APENAS OS ARQUIVOS QUE SE
MANTIVERAM'''
def retirar_indexados(restaram):
    with open(fr'cache/arquivos.txt', 'w') as locais:
        for ficaram in restaram:
            locais.write(ficaram)


'''===================================================================================='''
'''===============================FUNÇÕES DE PRINT====================================='''
'''===================================================================================='''


'''VAI PRINTAR O INDICE INVERTIDO DE MANEIRA FORMATADA PARA MELHOR
VISUALIZAÇÃO DO MESMO'''
def print_indice(ind_ivt):
    print('Formato:')
    print('-> Palavra/numero presente no indice')
    print('  |')
    print('  -->', end='')
    print('   indice do local em que está --- incidencia de ---> valor(quantidade em que apareceu ali) vezes')
    print('')
    cam, ident = abrir_caminhos()
    for palavra in ind_ivt:
        print(f'-> {palavra}')
        for referencia in ind_ivt[palavra]:
            print('  |')
            print('  -->', end='')
            arquivo=referencia
            if referencia != 'total':
                arquivo = os.path.basename(cam[int(ident.index(referencia))])
            print(f'   {arquivo} --- incidencia de ---> {ind_ivt[palavra][referencia]} vezes')
    print('')
    print('Formato:')
    print('-> Palavra/numero presente no indice')
    print('  |')
    print('  -->', end='')
    print('   indice do local em que está --- incidencia de ---> valor(quantidade em que apareceu ali) vezes')


'''APRESENTA TODOS OS ARQUIVOS QUE JA FORAM INDEXADOS'''
def print_indexados():
    locais=adicionados()
    for local in locais:
        print(local)


'''FORMATAÇÃO DE SEPARAÇÃO DE SETORES PARA USO DENTRO DOS PRINTS'''
def separador_dup():
    print('')
    print('='*90)
    print('')


'''PRINTA UMA LISTA DE COMANDOS COM SUAS FUNÇÕES E COMO REALIZAR USO'''
def ajuda():
    #VER SE FICA MELHOR
    #CRIAR UMA LISTA E DEPOIS COLOCAR UM FOR AQUI
    caminhos_val =[r'E:\ATIVIDADES\3 PROBLEMA\SESSÕES\SECRETARIO DE MESA',r'SESSÕES\SECRETARIO DE MESA']
    separador_dup()
    print(' '*30,'LISTA DE COMANDOS VALIDOS:')
    separador_dup()
    print('LER', end='========== ')
    print('Serve para indexar novos arquivos, ou diretorios para uso durante a busca')
    print('    Quando usado indicando um caminho, ou arquivo ja indexado, ele realiza atualização destes\n    no indice invertido de busca')
    print('    Formatação adequada para realização: "ler caminho"')
    print('    Exemplos de caminhos:')
    for caminho_val in caminhos_val:
        print('        ',caminho_val)
    separador_dup()
    
    print('VER',end='========== ')
    print('Serve para visualizar o indice invertido')
    print('    Formatação adequada para realização: "ver"')
    separador_dup()
    
    print('REMOVER', end='========== ')
    print('Serve para realizar a remoção seja de um arquivo ou de um diretorio completo')
    print('    É necessário que o caminho indicado seja valido, e já esteja indexado')
    print('    Para conferir a lista de arquivos indexados digite o comando: "LISTAR"')
    print('    Este comando remove o caminho da lista de indexados, além de atualizar o indice de palavra')
    print('    Formatação adequada para realização: "remover caminho"')
    separador_dup()
    
    print('LISTAR', end='========== ')
    print('Serve para apresentar todos os arquivos que estão indexados')
    print('    Formatação adequada para realização: "listar"')
    separador_dup()
    
    print('BUSCAR', end='========== ')
    print('Serve para realizar a busca de um termo dentro dos arquivos que foram indexados')
    print('    Para uso desse comando, deve-se chamar junto com o termo desejado')
    print('    É possível realizar a busca por palavra ou número')
    print('    Ele retorna o(s) arquivo(s) em que aparece, a incidencia nele(s), e a quantidade total')
    print('    Formatação adequada para realização: "buscar termo"')
    separador_dup()
    
    print('DELETE', end='========== ')
    print('Serve para remover os arquivos que foram indexados e ocorreu algo que os modificou')
    print('    Os arquivos podem estar nessa lista decorrente:')
    motivos_delete=['         -Mudança de nome;','         -Mudança de local de armazenamento;','         -Arquivo conrompido;','         -Arquivo apagado pelo usuario;','    Ação só possivel realizar havendo arquivos para remover']
    for motivo in motivos_delete:
        print(motivo)
    print('    Só pode ocorrer caso tenha arquivos para apagar')
    print('    Arquivos encontrados para retirar do index, são avisados assim que encontrados')
    print('    Formatação adequada para realização: "delete"')


'''APENAS PARA FORMATAR O PRINT INDICANDO QUE DEVE CHAMAR AJUDA'''
def print_help():
    print('Para ajuda digite o comando "HELP"')


'''PRINT QUE VARIA DECORRENTE CODIGO PASSADO PELA FUNÇÃO DE VALIDAÇÃO'''
def print_ajuda(codigo):
    if codigo==1:
        print('Por favor não apagar arquivos e/ou pasta cache do programa')
        cria_cache()
        print('Arquivos de cache criados, pode retornar a utilizar o programa')
    elif codigo==2:
        print('Comando digitado é invalido')
        print_help()
    elif codigo==3:
        print('Estes comandos não requerem argumentos adicionais além deles')
        print_help()
    elif codigo==4:
        print('Detectado mais de 2 argumentos inseridos')
        print('Para funcionamento destes argumentos, basta digitar ele e outro argumento equivalente')
        print_help()
    elif codigo==5:
        print('O local inserido não se refere a um diretorio ou arquivo')
        print_help()
    elif codigo==6:
        print('O diretorio ou arquivo referido, não pode ser acessado')
        print('Por favor verifique as permissões deste, ou insira outro local')
    elif codigo==7:
        print('O arquivo inserido ainda não foi indexado')
        print('Não há como realizar a operação de remoção ou atualização')
    # elif codigo==8:
    #     print('')
    elif codigo==9:
        print('Nenhum local indexado, por favor primeiro indexe um local ou arquivo')
        print_help()
    elif codigo==10:
        print('O arquivo inserido, não é valido para uso no programa')
        print('Programa tem suporte apenas a leitura de arquivos de texto, ".txt"')
    elif codigo==11:
        print('O arquivo inserido está corrompido, sendo impossibilitada a leitura')
    elif codigo==12:
        print('O diretorio inserido contém arquivo(s) que ainda não foi/foram indexado(s)')
        print('Não há como realizar a operação de remoção ou atualização')
    elif codigo==15:
        print('Não há arquivos para permitir esse comando continuar a execução')
        print('Em caso de dúvidas, por facor consulte a ajuda')
        print_help()
    #ESSES ULTIMOS RECEBEM TUPLAS, SE POSTOS EM ORDEM
    #DA ERRO NA VERIFICAÇÃO DO ELIF
    elif codigo[1]==13:
        print('Um dos arquivos presentes no diretorio está corrompido, sendo impossibilitada a leitura deste')
        for nome in codigo[0]:
            print(f'Nome do arquivo: {os.path.basename(nome)}')
    elif codigo[1]==14:
        print('Há arquivo(s) indexado(s) que foi(ram) apagado(s), ou movido(s) de lugar')
        print('Arquivo(s):')
        for apagado in codigo[0]:
            print(fr'{apagado}')
        print("Para remove-los do indice, use o comando:")
        print('delete')
        separador_dup()
    