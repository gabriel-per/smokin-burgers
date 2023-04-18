import random
import time
from playsound import playsound

days = 0
size = 0

# função para o pedido do cliente
def makeOrder(size):
    ing = {0: 'burger', 1: 'cheese', 2: 'lettuce', 3: 'tomato', 4: [0, 0, 0, 0]}
    
    for _ in range(size):
        ing[4][random.randint(0, 3)] += 1
    
    print(ing[4])
    print('\n\o/ <-- customer \nyo i wanna a burger with:')
    
    for ind, val in enumerate(ing[4]):
        if (val > 0):
            print(f'{val} {ing[ind]}')
    
    input('The customer will be waiting! Press any key to continue... ')

    return ing[4]


## :samueL: # noice
def fryBurger(numberOfBurguersToFry):

    #####################################################################
    # ideia de funcionamento pra funcao assincrona
    # a variavel global conteria o numero do hamburguer e a acao a ser tomada nele
    #####################################################################

    async def burgerTimeCounter():
        burgerSide = 0 ## 0 para o lado de baixo e 1 para o lado de cima
        tempoPraAssar = 30 # variável temporária
        ## em outro lugar do código o usuário teria a opção de virar o hambúrguer ou tirá-lo da chapa
        ## 0 para virar o hambúrguer, 1 para tirar da chapa
        for c in range(tempoPraAssar):
            if variavelGlobal == 0:
                if burgerSide:
                    burgerSide = 0
                else:
                    burgerSide = 1
            else:
                return mediaDeCozimento
                ## média de cozimento seria a média de cozimento entre o lado de cima e o de baixo
                ## quanto mais perto de 50%, melhor
            time.sleep(1)

    print('=-'*30, end='=\n')
    print(f'{"GRILLING PHASE!!!!!!!!!!!!!!!!!!!!!!!!!":^61}')
    print(f'{"HORA DO SHOW PORRA!":^61}')
    print('watch the fuckin burgar u idiot')
    print("""0: colocar hamburguer
    1: virar hamburguer
    2: tirar hamburguer""")

    grill = [] # here goes the burgers via .append # while len(grill) > 0: esquenta ai
    #heatup_rate = 1.5
    
    comando = input('> ')
    ## e aq se ele pedir pra virar o burguer por exemplo se tiver mais de um ele vai pedir
    ## qual hambúrguer pra tirar da chapa e dizer a porcentagem de cozimento dele e tal e pá
    if comando == 0:
        ## chamar a função assíncrona
        pass
    elif comando == 1:
        if len(grill) > 1:
            for i in len(grill):
                print(f"{i}: {grill[i]}")

            blegh1 = input('which burger do you want to remove?\n> ')

    else:
        if len(grill) > 1:
            for i in len(grill):
                print(f"{i}: {grill[i]}")
                
            blegh = input('which burger do you wanna flip?\n> ')


    # incrementar a taxa de aquecimento do hamburguer 1.5x a cada segundo enquanto no grill
    # saindo de 0% ate possivelmente 100 em ambos os lados
    # vou ver como e no jogo original a cada quantos seg esquenta 1%
    ## ok
    ## é uma boa acho

    pass


# função para a montagem do pedido
def assembleBurger():
    asmbIng = {0: 'down-bread', 1: 'top-bread', 2: 'burger', 3: 'cheese', 4: 'lettuce', 5: 'tomato', 6: [0, 0, 0, 0, 0, 0]}
    burguer = ''
    
    print('\n-=-=-=-=-=-\nMOUNT (idk how to say this in english) THE BURGER TIME!')
    print('\n0: down-bread, 1: top-bread, 2: burger, 3: cheese, 4: lettuce, 5: tomato')
    print('the assembling ends when you put the top-bread.\n')

    while (asmbIng[6][1] == 0): ## while top-bread hasn't been put down
        try:
            put = int(input('> '))
            asmbIng[6][put] += 1 ## increments to appropriate ingredient counter

            if (asmbIng[6][0] == 0 and put != 0): ## if down-bread hasn't been put down and player put down something else (error condition)
                if put == 1: ## player tries to put down top-bread first (tries to complete the burger even though it has nothing)
                    asmbIng[6][1] = 0
                    raise Exception("where's the burger you dumbass?")
                raise Exception('is the plate the new down-bread?') ## player put down an ingredient other than top-bread
            
            if (asmbIng[6][0] > 1): ## player tried to put down more than one down-bread
                asmbIng[6][0] = 1
                raise Exception("this ain't no big mac, so don't put more than one down-breads, ok? (it'd be harder to code y'know)")

            burguer = f'{asmbIng[put]:^10}\n{burguer}'

            print(burguer)
            
        except Exception as e: # prints the exception
            print(f'wth is possibly out of the desired behaviour within you, kindly? {e}')
    
    input("Done! Now let's give it... ")

    return asmbIng[6], burguer


# função para a entrega e avaliação do pedido
def rateBurger(order, burger, wait_secs):
    prices = {0: 3, 1: 2.25, 2: 1.50, 3: 1.75} ## preço de cada ingrediente (hamburguer, queijo, alface e tomate; respectivamente)
    final_price = 0
    penalty = 0
    satisfaction_level = 100 ## level de satisfacao maximo
    wait_secsfull = 60 # tempo de espera padrao - tempo de espera, quanto mais proximo de 0, pior
    rate = 5

    burgerArr = burger[0] ## asmbIng[6]
    burgerArr.pop(0)
    burgerArr.pop(1) ## removes top-bread and down-bread (they will not be taken into account for the rating)
    print(burgerArr)

    for ind, val in enumerate(burgerArr): ## calcula o preço do hambúrguer de acordo com os ingredientes
        final_price += prices[ind] * val
        ## se a quantidade de um tipo de ingrediente n for igual à pedida;
        if order[ind] > val: ## se o pedido queria mais de um ingrediente
            penalty += (order[ind] - val)*2
        elif order[ind] < val: ## se queria menos
            penalty += val - order[ind] # pensar em algo melhor dps ## adicionar a penalty a quantidade de ingredientes errados.
    
    final_price += 2 # bread's expenses

    # aviso: tudo o que envolve o algoritmo de satisfação do cliente nessa função está wip ou é placeholder, ou seja: completamente bugado
    ## finalsatisfaction = penalidade (número de ingredientes incorretos) menos o tempo remanescente de espera
    print(penalty)
    dissatisfaction = (penalty * 15) + (wait_secsfull - wait_secs) # atual formula de penalidade, apenas placeholder, pensar em uma melhor dps
    final_stats = satisfaction_level - dissatisfaction ## satisfacao total (satisfacao maxima - quantidade de satisfacao perdida)
    if final_stats < 0:
        final_stats = 0

    print(f"\o/ <-- customer\nhere's your bitch lasagna sir\n {burger[1]}")
    time.sleep(1)
    print('...')
    time.sleep(random.randint(1,3))

    ratings = {
        90: "Very nice!",
        75: "good",
        50: "run of the mill. good'nuff",
        25: "it sucks, but i'll pay",
        10: "tf? i won't pay for this crap",
        0: "BLEGH"
    }
    for k in ratings:
        if final_stats >= k:
            print(ratings[k])
            break
    
    print(f'cash earned: {final_price}')
    print(final_stats)

    return final_price, rate




def startGame():
    global size
    global days
    if days % 2 == 0: size += 1
    
    clients = random.randint(2, 4) # ideia: clientes proporcionais ao nível de avaliação do restaurante (relacionado a variavel rate da func acima)

    print(f'DAY {days + 1}')

    for _ in range(clients + 1):
        print('...')
        time.sleep(random.randint(1, 5))
        ## aqui o player começa no caixa e pode navegar para a build station 
        ## (onde monta os hamburgueres) ou cozinha (onde frita) 

        ## para criar um bolo de funções assíncronas:
            # funcao1 = loop.create_task(nome_da_funcao())
            # funcao2 = loop.create_task(nome_da_funcao())
            # await asyncio.wait([funcao1, funcao2])

        order = makeOrder(2**size)
        counter_start = time.time()
        burger = assembleBurger()
        counter_end = time.time()

        cash_n_rate = rateBurger(order, burger, int(counter_start - counter_end))
    
    days += 1
    if days < 6:
        startGame()
    
    
while True:
    startGame()
    if input('quer jogar dnv?') == 1: 
        days, size = 0
        break

# loop = asyncio.get_event_loop()
# loop.run_until_complete(startGame())