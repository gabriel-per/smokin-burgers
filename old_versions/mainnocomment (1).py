import random
import time
from playsound import playsound
import asyncio

days = 0
size = 0

variavelGlobal = 'XX' ## o primeiro índice referencia o hamburguer, o segundo a ação a ser tomada

asmbIng = {0: 'down-bread', 1: 'top-bread', 2: 'burger', 3: 'cheese', 4: 'lettuce', 5: 'tomato', 6: [0, 0, 0, 0, 0, 0]}

orders = []
customersWaiting = 0
burgers = []
grill = [] 


##############################################################################################################


#######################
# ACCESSORY FUNCTIONS #
#######################
### miscellaneous functions that are repeated throughout the code ###

def printStationMessage(station, topMessage, commands=False):
    stationASCII = {"a": "alguma arte ascii", "b": "blah", "c": "blegh"} ## a for grill, b for build, c for checkout | this will store the ASCII art in the future
    print(stationASCII[station])
    print(topMessage)
    print('=-'*30, end='=\n')
    print("""-=- NAVIGATION -=-
    A: GRILL STATION
    B: BUILD STATION
    C: CHECKOUT COUNTER""")
    if commands:
        print('-=- ACTIONS -=-')
        print(commands)
        print('v: view current orders')
        print('=-'*30, end='=\n')

def navigation(currentStation, command):
    stations = {"a": grillStation, "b": buildStation, "c": checkoutStation}
    command = command.strip().lower()
    if command not in 'abc':
        print('YOU PICKED THE WRONG COMMAND, FOOL!')
        stations[currentStation]()
    stations[command]()


##############################################################################################################


###################
# ASYNC FUNCTIONS #
###################
### the counter functions! they run asynchronously. ###

async def burgerTimeCounter(burgerID):
    global variavelGlobal
    global grill
    burgerSide = 0 ## 0 para o lado de baixo e 1 para o lado de cima
    tempoPraAssar = 16 * (random.randint(8, 12) / 10) ## hambúrguer pode levar de 12.8s até 19.2s para assar (intervalo muito largo?)
    ## em outro lugar do código o usuário teria a opção de virar o hambúrguer ou tirá-lo da chapa
    ## 0 para virar o hambúrguer, 1 para tirar da chapa
    while(variavelGlobal[0] != burgerID):
        grill[burgerID][burgerSide] += 50 / (tempoPraAssar * 4)
        ## supondo q cada lado do hambúrguer demora em torno de 16.5s pra assar
        ## portanto, a cada meio segundo assa 1.5%
        ## introduzir aleatoriedade ao tempo de cozimento do hamburguer talvez?
        time.sleep(0.25)
    
    if variavelGlobal[1] == '0':
        if burgerSide:
            burgerSide = 0
        else:
            burgerSide = 1
    elif variavelGlobal[1] == '1':
        return sum(grill[burgerID]) / 2
        ## média de cozimento seria a média de cozimento entre o lado de cima e o de baixo
        ## quanto mais perto de 50%, melhor

async def ingameTimeCounter():
    ## this function is responsible for keeping track of ingame time and
    ## handles async customer arrivals. the times at which the customers arrive were
    ## pre-determined before the day starts.
    print('Um cliente chegou para fazer um pedido!')
    orders.append(makeOrder())


##############################################################################################################


############################
# CUSTOMER ORDER FUNCTIONS #
############################

def viewOrders():
    global orders
    ing = {0: 'burger', 1: 'cheese', 2: 'lettuce', 3: 'tomato'}
    ## o nome do cliente está em order[1], e o seu pedido em order[0]
    for orderNumber, order in enumerate(orders):
        print(f'Order number {orderNumber}, from {order[1]}, says:')
        for ingIndex, ingQuantity in enumerate(order[0]):
            if ingQuantity > 0:
                print(ingQuantity, ing[ingIndex])

    if len(orders) == 0:
        print('no customer orders to view... for now. no slacking ou vou você será avisado.')


# função para o pedido do cliente
## modifiquei essa função de forma que ela é apenas responsável por gerar um pedido aleatório, ficou mais como um acessório
## para outras funções.
def makeOrder(size):
    names = ['sussy oliveira', 'ednalva', 'lula', 'big smoke', 'walter white', 'jesse pinkman', 'davi', 'joão', 'samuel', 'xandao cabeça de p']
    global orders
    ing = {0: 'burger', 1: 'cheese', 2: 'lettuce', 3: 'tomato', 4: [0, 0, 0, 0]}
    
    for _ in range(size):
        ing[4][random.randint(0, 3)] += 1

    return [ing[4], random.choice(names)]


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

    print(f"\o/ <-- customer\nhere's your bitch lasagna sir\n{burger[1]}")
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


##############################################################################################################


#####################
# STATION FUNCTIONS #
#####################


def grillStation():
    global variavelGlobal
    global grill

    #####################################################################
    # ideia de funcionamento pra funcao assincrona
    # a variavel global conteria o numero do hamburguer e a acao a ser tomada nele
    #####################################################################

    printStationMessage("a", "WELCOME TO DA GRILLIN' STATION!!!", """0: colocar hamburguer
    1: virar hamburguer
    2: tirar hamburguer""")
    
    command = input('> ')
    ## e aq se ele pedir pra virar o burguer por exemplo se tiver mais de um ele vai pedir
    ## qual hambúrguer pra tirar da chapa e dizer a porcentagem de cozimento dele e tal e pá
    if command.isnumeric():
        if command == "0":
            mediaDeCozimento = burgerTimeCounter() ## placeholder
            pass
        elif command == "1" or command == "2":
            if len(grill) > 1:
                for i in len(grill):
                    print(f"{i}: {grill[i]}")
                burgerToActOn = input('which burger do you want to flip?\n> ' if command == 1 else 'which burger do you want to remove?\n> ')
                variavelGlobal = f'{burgerToActOn}{command}'
        else:
            print('invalid command you fucking donkey')
            grillStation()
    else:
        if command == "v":
            viewOrders()
        else:
            navigation("a", command)


    # incrementar a taxa de aquecimento do hamburguer 1.5x a cada segundo enquanto no grill
    # saindo de 0% ate possivelmente 100 em ambos os lados
    # vou ver como e no jogo original a cada quantos seg esquenta 1%
    ## ok
    ## é uma boa acho


def buildStation():
    burger = ''
    
    printStationMessage("b", "MOUNT (idk how to say this in english) THE BURGER TIME!\nWELCOME TO DA BUILDIN' STATION!!!", """0: down-bread
    1: top-bread
    2: burger
    3: cheese
    4: lettuce
    5: tomato""")
    print('the assembling ends when you put the top-bread.\n')
    command = input('> ')

    if command.isnumeric():
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

            burger = f'{asmbIng[put]:^10}\n{burger}'

            print(burger)
            
        except Exception as e: ## prints the exception
            print(f'wth is possibly out of the desired behaviour within you, kindly? {e}')
        buildStation()
    else:
        navigation("b", command)
        return
    
    return asmbIng[6], burger


def checkoutStation():
    global orders
    global burgers
    global customersWaiting
    ing = {0: 'burger', 1: 'cheese', 2: 'lettuce', 3: 'tomato', 4: [0, 0, 0, 0]}


    printStationMessage("c", "yo welcome to where we store the day's dolla dolla bills", """0: entregar pedido do cliente
    """)
    if customersWaiting > 0:
        print(f'There are customers WAITING FOR SERVICE YOU MORON! {customersWaiting}, to be exact.')
        print(f'1: serve customer')
    else:
        print('No customers waiting to be served. *For now*.')

    command = input('> ')
    if command == "1":
        if customersWaiting:
            orders.append(makeOrder())
            print(orders)
            print('\n\o/ <-- customer \nyo i wanna a burger with:')
            
            for ind, val in enumerate(ing[4]):
                if (val > 0):
                    print(f'{val} {ing[ind]}')
            
            input('The customer will be waiting! Press any key to continue... ')
            checkoutStation()
        else:
            print('i said no customers were waiting to be served you dumbass')
    else:
        navigation("c", command)


##############################################################################################################


########
# MAIN #
########

def startGame():
    global size
    global days
    if days % 2 == 0: 
        size += 1
    
    nCustomers = random.randint(2, 4)
    for _ in range(nCustomers):
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
        burger = buildStation()
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

##############################################################################################################

# loop = asyncio.get_event_loop()
# loop.run_until_complete(startGame())