import random
import copy
def GeraMatrizSudoku (npp): #Gera uma matriz 9x9 com npp's espaços preenchidos de forma aleatória
    if npp > 81 or npp < 0:
        raise IndexError("Valor npp incorreto, npp deve ser maior que 0 ou menor que 81")
    matriz = [[0 for _ in range(9)] for _ in range(9)]
        
    solucoes = Sudoku(matriz, max_solucoes=1)

    if not solucoes:
        raise RuntimeError("Não foi capaz de gerar uma matriz")
    
    matriz_completa = solucoes[0]

    posicoes = [(linha, coluna) for linha in range(9) for coluna in range(9)]

    random.shuffle(posicoes)

    for i in range(81 - npp):
        linha, coluna = posicoes[i]
        matriz_completa[linha][coluna] = 0

    return matriz_completa

def matriz_valida(matriz):
        matriz_tres = []
        erro_encontrado = False   
        #Verifica se há elementos iguais na linha
        for i in range(len(matriz)):
            for j in range(len(matriz)-1):
                if matriz[i][j] == 0:
                    continue
                for k in range(j+1, len(matriz)):
                    if matriz[i][j] == matriz[i][k]:
                        erro_encontrado = True
                        break
                if erro_encontrado: break
            if erro_encontrado: break

        if erro_encontrado: return False

        #Verifica se há elementos iguais na coluna
        for i in range(len(matriz)):
            for j in range(len(matriz)):
                if matriz[j][i] == 0:
                    continue
                for k in range(j+1, len(matriz)):
                    if matriz[j][i] == matriz[k][i]:
                        erro_encontrado = True
                        break
                if erro_encontrado: break
            if erro_encontrado: break
        
        if erro_encontrado: return False

        #Verifica se há elementos repetidos no bloco 3x3
        for i in range(0, len(matriz), 3):
            for j in range(0, len(matriz), 3):
                #Quebrei nossa matriz 9x9 em matrizes 3x3 para ficar mais simples a verificação
                matriz_quebrada = [[0 for _ in range(3)] for _ in range(3)]

                for linha in range(3):
                    for coluna in range(3):
                        matriz_quebrada[linha][coluna] = matriz[i + linha][j + coluna]
                matriz_tres.append(matriz_quebrada)
        #Aqui é onde faço a verificação se há elementos repetidos dentro de cada bloco 3x3, transformando a matriz em uma lista e verificando essa lista
        for indice in range(len(matriz_tres)):
            lista_dos_elementos = []
            for i in range(len(matriz_tres[indice])):
                for j in range(len(matriz_tres[indice])):
                    lista_dos_elementos.append(matriz_tres[indice][i][j])
            lista_filtrada = []
            for x in lista_dos_elementos:
                if x != 0:
                    lista_filtrada.append(x)
            if len(lista_filtrada) != len(set(lista_filtrada)):
                erro_encontrado = True
        
        if erro_encontrado: return False

#Função que encontra zeros numa matriz 
def encontrar_zero(matriz):

    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if matriz[i][j] == 0:
                return [i, j]
    return False

def posicao_valida(matriz, num, linha, coluna): #Diferente da função 'matriz_valida' essa não verifica a matriz inteira, verifica apenas a posicao em questao, fiz para otimizar o algoritmo
        erro_encontrado = False
    #Verifica se há elementos iguais na linha
        for i in range(len(matriz)):
            if matriz[linha][i] == num and coluna != i:
                erro_encontrado = True
                break

        if erro_encontrado: return False

        #Verifica se há elementos iguais na coluna
        for i in range(len(matriz)):
            if matriz[i][coluna] == num and linha != i:
                erro_encontrado = True
                break
        
        if erro_encontrado: return False

        #Verifica se há elementos iguais no bloco 3x3 em questão

        bloco_x = coluna // 3
        bloco_y = linha // 3

        # Itera sobre as 9 células do bloco
        for i in range(bloco_y * 3, bloco_y * 3 + 3):
            for j in range(bloco_x * 3, bloco_x * 3 + 3):
                if matriz[i][j] == num and (i, j) != (linha, coluna):
                    erro_encontrado = True
                    break
                if erro_encontrado: break
            if erro_encontrado: break
        
        if erro_encontrado: return False

        return True

def Sudoku(matriz_inicial, max_solucoes=15): #Defini o máximo de soluções igual a 15
    solucoes_encontradas = []
    # Criei uma cópia da matriz para não modificar a original
    tabuleiro = copy.deepcopy(matriz_inicial)
    
    _resolver_recursivo(tabuleiro, solucoes_encontradas, max_solucoes)
    
    return solucoes_encontradas

def _resolver_recursivo(matriz, solucoes, limite):
    #Se já atingi o limite (15), paramos a busca
    if len(solucoes) >= limite:
        return

    posicao_encontrada = encontrar_zero(matriz)

    #Caso base: não há mais zeros
    if not posicao_encontrada:
        #Guarda cópia da solução
        solucoes.append(copy.deepcopy(matriz))
        return

    linha, coluna = posicao_encontrada
        
    for num in range(1, 10):
        if posicao_valida(matriz, num, linha, coluna):
            matriz[linha][coluna] = num
            
            _resolver_recursivo(matriz, solucoes, limite)
            matriz[linha][coluna] = 0
            
            #Se já atingi o liite
            if len(solucoes) >= limite:
                return
            
def matriz_organi(matriz):
    vazio = ''

    for linha in matriz:
        linha_organizada = "".join([f"{elemento:>{2}}" for elemento in linha])
        vazio = vazio + linha_organizada + '\n'
    return vazio



def imprimir_sudoku():
    while True:
        posicoes_preenchidas = input('Entre com o número de posições a preencher inicialmente: ')

        if posicoes_preenchidas.lower() == 'fim':
            break

        matriz_inicial = GeraMatrizSudoku(int(posicoes_preenchidas))
        matriz_resolvida = Sudoku(matriz_inicial)

        if len(matriz_resolvida) == 0: return "Não há solução"

        print(f'Matriz inicial: \n{matriz_organi(matriz_inicial)}')

        for i in range(len(matriz_resolvida)):
            print(f"Matriz completa - Solução {i} \n{matriz_organi(matriz_resolvida[i])} \n Linhas OK \n Colunas OK \n Quadrados OK")
        


imprimir_sudoku()
