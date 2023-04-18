###########
# MODULES #
###########

import random
import time
from threading import Thread

##############################################################################################################

# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠁⠀⠀⠀ ⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀ ⠀⠘⢿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⠀ ⠀⠀⣾⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⠋⠈⠀⠀⠀⠀⠐⠺⣖⢄⠀⠀⠀⠀⠀  ⠀⠀⠀⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⡏⢀⡆⠀⠀⠀⢋⣭⣽⡚⢮⣲⠆⠀⠀⠀ ⠀⠀ ⠀⢹⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⡇⡼⠀⠀⠀⠀⠈⠻⣅⣨⠇⠈⠀ ⠰⣀⣀⣀⡀⠀⢸⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⡇⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⣟⢷⣶⠶⣃⢀⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⢿⠀⠈⠓⠚⢸⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⢀⡠⠀⡄⣀⠀⠀  ⠀⢻⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠐⠉⠀⠀⠙⠉⠀ ⠠⡶⣸⠁⠀⣠⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣦⡆⠀⠐⠒⠢⢤⣀⡰⠁⠇ ⠈⠘⢶⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠠⣄⣉⣙⡉⠓ ⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄ ⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⣀⠀⣀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿

##############################################################################################################

#######################
# ACCESSORY FUNCTIONS #
#######################
### miscellaneous functions that are repeated throughout the code ###

def printStationMessage(station, topMessage, commands=False):
    global ingameTime ## to be used in the future for implementing a clock mechanic to the station message
    global notifications

    stationASCII = {"a": "**ASCII PLACEHOLDER**", "b": "**ASCII PLACEHOLDER**", "c": "**ASCII PLACEHOLDER**"} ## a for grill, b for build, c for checkout
    ## this will store the ASCII art in the future
    print('=-'*30, end='=\n')
    print(stationASCII[station])
    print('--'*30, end='-\n')
    print(topMessage)
    print('=-'*30, end='=\n')
    print("-=- NAVIGATION -=-")
    print("A: Grill Station / B: Build Station / C: Checkout Counter")

    if commands:
        print('-=- ACTIONS -=-')
        print(commands)
        print('v: view current orders')
        print('=-'*30, end='=\n')

    for notif in notifications:
        print(notif)
    notifications.clear()


def navigation(currentStation, command):
    stations = {"a": grillStation, "b": buildStation, "c": checkoutStation}
    command = command.strip().lower()
    if command not in 'abc':
        print('YOU PICKED THE WRONG COMMAND, FOOL!')
        stations[currentStation]()
    else:
        stations[command]()

def makeThreadForFunction(asyncFunction, burgerID=None):
    if burgerID != None:
        thread = Thread(target=asyncFunction, args=([burgerID]))
    else:
        thread = Thread(target=asyncFunction, args=())
    thread.start()

##############################################################################################################

###################
# ASYNC FUNCTIONS #
###################
### the counter functions! they run asynchronously. ###

def burgerTimeCounter(pattyID):
    """
    this function handles:
    - writing to global var "grill" the cook percentage of each side
    - removing the patty
    - flipping the patty
    - counts time spent on grill and sets random time for ideal cook percentage
    """
    global comandoChapa
    global grill
    patty = grill[pattyID]
    pattySide = 0 ## 0 para o lado de baixo e 1 para o lado de cima
    tempoPraAssar = 16 * (random.randint(8, 12) / 10) ## hambúrguer pode levar de 12.8s até 19.2s para assar (aumentar dps)

    while(comandoChapa != f'{pattyID}2'):
        if (patty[pattySide] < 200):
            patty[pattySide] += 200 / (tempoPraAssar * 4)
            patty[pattySide] = float(f'{patty[pattySide]:.2f}')
        else:
            patty[pattySide] = 200
        time.sleep(0.25)
    
        if comandoChapa == f'{pattyID}1':
            if (pattySide):
                pattySide = 0
            else:
                pattySide = 1
            comandoChapa = 'XX'

    cookedPatties.append(sum(grill[pattyID]) / 2)
    grill.pop(pattyID)


def ingameTimeCounter():
    """
    this function handles:
    - keeping track of ingame time
    - async customer arrivals
    """
    global ingameTime
    global customerArrivalTimes
    global customersWaiting

    while(ingameTime < 180):

        if customerArrivalTimes and customerArrivalTimes[0] <= ingameTime:
            notifications.append('Um cliente chegou para fazer um pedido!')
            customersWaiting += 1
            customerArrivalTimes.pop(0)

        time.sleep(1)
        ingameTime += 1

    notifications.append('\033[30;44mYour work shift is over! You may close anytime by writing "fechar"\033[m')


##############################################################################################################

############################
# CUSTOMER ORDER FUNCTIONS #
############################

def viewOrders(currentStation):
    global orders
    ing = {0: 'burger', 1: 'cheese', 2: 'lettuce', 3: 'tomato'}
    ## o nome do cliente está em order[1], e o seu pedido em order[0]
    for orderNumber, order in enumerate(orders):
        print(f'Order number {orderNumber}, from {order[1]}, says:')
        for ingIndex, ingQuantity in enumerate(order[0]):
            if ingQuantity > 0:
                print(ingQuantity, ing[ingIndex])
        time.sleep(1)
    time.sleep(2)

    if len(orders) == 0:
        print('no customer orders to view... for now. no slacking or você será avisado.')

    currentStation()


# função para o pedido do cliente
## modifiquei essa função de forma que ela é apenas responsável por gerar um pedido aleatório, ficou mais como um acessório
## para outras funções
def makeOrder():
    global customersWaiting
    global orders
    global size
    names = ['sussy oliveira', 'ednalva', 'lula', 'big smoke', 'walter white', 'jesse pinkman', 'davi', 'joão', 'samuel', 'xandao cabeça de p']
    ing = [0, 0, 0, 0]
    
    for _ in range(2**size):
        ing[random.randint(0, 3)] += 1

    orders.append([ing, random.choice(names), ingameTime]) 

def rateBurger(order, burger, wait_secs):

    #########
    # TO-DO #
    #########
    # - finish up penalty formula
    # - include somaDeCozimento in the penalty formula
    # - add sfx (this applies to the entire code)

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
    global comandoChapa
    global grill
    global burgerIDGenerator
    pattyToActOn = "0"

    printStationMessage("a", "WELCOME TO DA GRILLIN' STATION!!!", """0: colocar hamburguer
1: virar hamburguer
2: tirar hamburguer
3: atualizar status dos hamburgueres""")
    for id in grill:
        print(f'Status do burgão {id}:')
        print(f'- Topo: {grill[id][1]}%')
        print(f'- Fundo: {grill[id][0]}%')
        print('+-----+-----+')

    if (len(grill) == 0):
        print('Não há hambúrgueres cozinhando na chapa')
    
    command = input('> ')

    if (command.isnumeric()):

        if (command == "0"):
            grill[burgerIDGenerator] = [0, 0]
            makeThreadForFunction(burgerTimeCounter, burgerIDGenerator)
            burgerIDGenerator = str(int(burgerIDGenerator) + 1)

        elif (command == "1" or command == "2"):
            if (len(grill) > 0):
                for id in grill:
                    print(f'Status do burgão {id}:')
                    print(f'- Topo: {grill[id][1]}%')
                    print(f'- Fundo: {grill[id][0]}%')
                    print('+-----+-----+')

                pattyToActOn = input('which burger do you want to flip?\n> ' if command == "1" else 'which burger do you want to remove?\n> ')

            else:
                print('You flip your spatula in the air. There are no patties on the grill...')

            comandoChapa = f'{pattyToActOn}{command}'
                
        else:
            if command != "3":
                print('invalid command you fucking donkey')

        grillStation()

    else:
        if (command == "v"):
            viewOrders(grillStation)
        else:
            navigation("a", command)


def buildStation():
    ## player can only assemble one burger at a time
    ## but they can have multiple assembled burgers in storage.
    global burger
    global burgers
    global asmbIng
    global cookedPatties
    pattyToAdd = 0
    
    printStationMessage("b", "MOUNT (idk how to say this in english) THE BURGER TIME!\nWELCOME TO DA BUILDIN' STATION!!!", """0: down-bread
1: top-bread
2: burger
3: cheese
4: lettuce
5: tomato""")
    print('the assembling ends when you put the top-bread.\n')
    print('><><><>< -=- BURGER -=- ><><><><\n')
    print(burger)
    print('><><><><><><><><><><><><><><><><')

    command = input('> ')

    if (command.isnumeric()):

        try:
            command = int(command)
            if (asmbIng[6][0] == 0 and command != 0): ## if down-bread hasn't been put down and player put down something else (error condition)
                if command == 1: ## player tries to put down top-bread first (tries to complete the burger even though it has nothing) 
                    raise Exception("where's the burger you dumbass?") ## merely cosmetical though, the line in the code below would be enough for this if -- davidf
                raise Exception('is the plate the new down-bread?') ## player put down an ingredient other than top-bread
            if (asmbIng[6][0] > 1): ## player tried to put down more than one down-bread
                raise Exception("this ain't no big mac, so don't put more than one down-breads, ok? (it'd be harder to code y'know)")

            if (command == 2):
                if (len(cookedPatties) > 0):
                    for index, somaDeCozimento in enumerate(cookedPatties):
                        print(f'patty {index}: {somaDeCozimento}% cozido')
                    if (len(cookedPatties) > 1):
                        pattyToAdd = int(input('which patty do you want to add to the burger?\n> '))
                    asmbIng[6][6] = somaDeCozimento
                    cookedPatties.pop(pattyToAdd)
                else:
                    raise Exception("i sense a stifling lack of COOKED PATTIES in this build station...")

            asmbIng[6][command] += 1 ## increments to appropriate ingredient counter

            burger = f'{asmbIng[command]:^32}\n{burger}'

            if (asmbIng[6][1] == 1):
                burgers.append(asmbIng[6][2:])
                print(burgers)
                burger = ""
                asmbIng[6] = [0, 0, 0, 0, 0, 0, 0]
                print('Burger successfully assembled! It is ready for serving at the Checkout Counter.')

        except Exception as e: ## prints the exception
            print(f'wth is possibly out of the desired behaviour within you, kindly? {e}')

        finally:
            buildStation()
    else:
        if (command == "v"):
            viewOrders(buildStation)
        else:
            navigation("b", command)


def checkoutStation():
    global orders
    global burgers
    global customersWaiting
    ing = {0: 'burger', 1: 'cheese', 2: 'lettuce', 3: 'tomato', 4: [0, 0, 0, 0]}
    customerToGiveBurgerTo = 0
    burgerToGive = 0

    printStationMessage("c", "yo yo yo 148 welcome to the checkout counter i'm out of ideas for messages", "0: entregar pedido do cliente")
    if (customersWaiting > 0):
        print(f'There are customers WAITING FOR SERVICE YOU MORON! {customersWaiting}, to be exact.')
        print(f'1: serve customer')
    else:
        print('No customers waiting to be served. *For now*.')

    command = input('> ')


    if (command == "0"):

        if (len(orders) > 0):

            print('there is 1 order waiting for your utterly incompetent ass:' if len(orders) == 1 else f'there are {len(orders)} waiting for your utterly incompetent ass:')

            for orderIndex, order in enumerate(orders):
                print(f'{orderIndex}: Pedido do cliente {order[1]}, contendo:')

                for ingIndex, ingQuantity in enumerate(order[0]):
                    if (ingQuantity > 0):
                        print(f'{ingQuantity} {ing[ingIndex]}')

            if (len(orders) > 1):
                customerToGiveBurgerTo = int(input("which customer do you want to give the burger to?\n> "))

            if (len(burgers) > 1):
                for i in range(len(burgers)):
                    print(f'Burger {i}:')
                    for ingIndex, ingQuantity in enumerate(burgers[i]):
                        if (ingQuantity > 0 and ingIndex != 4): ## index 4 of "burgers[i]" is cook percentage
                            print(f'{ingQuantity} {ing[ingIndex]}')

                burgerToGive = int(input(f"you have more than one burger ready to go! which one do you want to give to {orders[customerToGiveBurgerTo][1]}?"))

            rateBurger(orders[customerToGiveBurgerTo], burgers[burgerToGive], ingameTime - orders[customerToGiveBurgerTo][2]) 
            orders.pop(customerToGiveBurgerTo)
            burgers.pop(burgerToGive)

        else:
            print('no customers waiting for their burger jackass')
        checkoutStation()


    elif (command == "1"):
        if (customersWaiting):
            customersWaiting -= 1
            makeOrder()
            print('\n\o/ <-- customer \nyo i wanna a burger with:')
            for ind, val in enumerate(orders[-1][0]):
                if (val > 0):
                    print(f'{val} {ing[ind]}')
            input('The customer will be waiting! Press any key to continue... ')
        else:
            print('i said no customers were waiting to be served you dumbass')
        checkoutStation()

    elif (command == "v"):
        viewOrders(checkoutStation)

    else:
        navigation("c", command)


##############################################################################################################

########
# MAIN #
########

def startGame():
    global size
    global days
    global customersWaiting
    if (days % 2 == 0): 
        size += 1
    
    nCustomers = random.randint(1, 3) ## plus the first customer
    for _ in range(nCustomers):
        customerArrivalTimes.append(random.randint(20, 160)) # ideia: clientes proporcionais ao nível de avaliação do restaurante (relacionado a variavel rate da func acima)


    print(f'DAY {days + 1}')
    print('...')

    time.sleep(random.randint(1, 5))
    makeThreadForFunction(ingameTimeCounter)
    time.sleep(1)

    checkoutStation()
    
    days += 1
    if (days < 6):
        startGame()
    
    
while True:
    days = 0
    size = 0

    comandoChapa = 'XX' ## o primeiro índice referencia o hamburguer, o segundo a ação a ser tomada
    asmbIng = {0: 'down-bread', 1: 'top-bread', 2: 'burger', 3: 'cheese', 4: 'lettuce', 5: 'tomato', 6: [0, 0, 0, 0, 0, 0, 0]}
    ## update! asmbIng[6][6] is how well the burger is cooked (ranges from 0 to 200)
    ## for exclusive use by buildStation()! using asmbIng anywhere else will potentially break the code.

    burgerIDGenerator = "0"
    burger = ""
    ingameTime = 0
    customersWaiting = 0
    orders = []
    burgers = []
    cookedPatties = []
    notifications = []
    customerArrivalTimes = [0]
    grill = {}
    inputActive = False

    startGame()

    if (input('quer jogar dnv? (y/n): ').strip().lower() == 'n'): 
        days, size = 0
        break