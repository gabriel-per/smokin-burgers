###########
# MODULES #
###########

import random
import time
from threading import Thread
from math import floor

##############################################################################################################

#######################
# ACCESSORY FUNCTIONS #
#######################
### miscellaneous functions that are repeated throughout the code ###

def ingameTimeToClockTime(): ## usando 9:00 como início do dia e 17:00 como fim (8 horas de turno no total)
    global ingameTime

    timePassedInHours = 8 * (ingameTime / 240) ## 240 is the day duration
    hoursInt = floor(timePassedInHours)
    minutesInt = round((timePassedInHours - hoursInt) * 60)

    clockTime = f"{hoursInt + 9:0>2}:{minutesInt:0>2}"
    return clockTime


def loadAnimation(duration):
    duration /= 10
    for _ in range(10):
        print('.', end=' ', flush=True)
        time.sleep(duration)
    print()


def printStationMessage(station, topMessage, commands=False):
    global ingameTime, notifications, showCommands

    stationASCII = {
        "a": """\033[1;32m                         ▌ ▐` █
                         █  █ ▐▌
                       ,,▄▄▄▄▄▄▄,
                    ▄▀▀-▄ ▄▐▌▄ ▄ █▀█
                    █▄█ ▀ ▀▐▌▀▌▀ █▄█'
                  ▀▀▀▄▄▄█▀▀▀▀▀▀██▄▄▀▀▀
                      ▀██████████▀'
                       ▄▀`▀▀▀▀▀▀▄
                     ▄▀          ▀▄\033[m""", 

        "b": """\033[1;35m                         ,▄▄▄▄,
                    ▄A▀ª▀`     ▀▄,
                  ▄▀            --`▀▀▄
                  █                  █
                   █,               ▄▀
                     ▀▌ ,    , , ▐▀▀
                      ▌ █ ▐  ▌ █ ▐⌐
                      █∞∞∞∞∞∞∞∞∞∞█⌐
                      ▀▀▀▀▀▀▀▀▀▀▀▀\033[m""", 

        "c": """\033[1;34m                             ▄▄▄▄▄▄
                      ▄MMMN▄ █    █
                    ▄4▌ⁿ▀▀ █ ██████▄
                   ▐▌ ▌▄▄▄ █ █▀▀▀▀█ ▌
                   █  █▄▄▄▄█ ▀▀▀▀▀▀ █
                   █         ▀"▀▀╙▀ ▐
                  ▐▌         ▀`▀▀▐▀ ¬▌
                  █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
                  █        ▀▀        █
                   ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\033[m"""
    } 
    ## a for grill, b for build, c for checkout
    ## this will store the ASCII art in the future
    stationColor = {"a": "2", "b": "5", "c": "4"}


    print('\n'*40)

    print(stationASCII[station])
    print(f'\n\033[1m{ingameTimeToClockTime():^57}\033[m')
    print(f'\n\033[1;3{stationColor[station]}m-=-=-=-=-=-=-=-=-=-=-=- {topMessage:^9} -=-=-=-=-=-=-=-=-=-=-=-\033[m')

    if (showCommands):

        print(f"\033[1;36m{'-=- NAVEGAÇÃO -=-':^57}\033[m")
        print(f"\033[37m{'A: Chapa / B: Montagem / C: Caixa':^57}\033[m")
        print(f"\033[1;36m{'-=- AÇÕES -=-':^57}\033[m")

        commands = commands.split("\n")
        for command in commands:
            print(f'{command:^57}')

        print(f'{"v: visualizar pedidos":^57}')

    print(f'{"cmds: mostrar/esconder comandos":^57}')
    print(f'\033[1;3{stationColor[station]}m' + '=-'*28, end='=\033[m\n\n')

    print(f"\033[1;31m------------------ 🔔 NOTIFICAÇÕES ({len(notifications)}) ------------------\033[m")
    for notif in notifications:
        print(f"\033[33m{notif:^57}\033[m")
        time.sleep(1)
    print('\033[1;31m-'*57, end='\033[m\n\n')

    notifications.clear()


def navigation(currentStation, command):
    stations = {"a": grillStation, "b": buildStation, "c": checkoutStation}
    if command not in 'abc':
        print('Comando inválido!')
        input('\n>> OK <<')
        stations[currentStation]()
    else:
        loadAnimation(0.5)
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

def burgerTimeCounter(pattyID): ## burgerID is now pattyID
    """
    this function handles:
    - writing to global var "grill" the cook percentage of each side
    - removing the patty
    - flipping the patty
    - counts time spent on grill and sets random time for ideal cook percentage
    """
    global comandoChapa, grill
    patty = grill[pattyID]
    pattySide = 0 ## 0 para o lado de baixo e 1 para o lado de cima
    tempoPraAssar = 30 * (random.randint(8, 12) / 10)

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
    ingameTime = 0

    while(ingameTime < 240):

        if customerArrivalTimes and customerArrivalTimes[0] <= ingameTime:
            notifications.append('Um cliente chegou para fazer um pedido!')
            customersWaiting += 1
            customerArrivalTimes.pop(0)

        time.sleep(0.25)
        ingameTime += 0.25

    notifications.append(f'\033[1;34m{"O seu turno acabou!":^57}\n{"Insira `fechar` (sem aspas) no Caixa para finalizar o dia.":^57}\033[m')


##############################################################################################################

############################
# CUSTOMER ORDER FUNCTIONS #
############################

def viewOrders(currentStation):
    global orders
    ing = {0: 'hambúrguer', 1: 'queijo', 2: 'alface', 3: 'tomate'}

    ## o nome do cliente está em order[1], e o seu pedido em order[0]
    for orderNumber, order in enumerate(orders):
        print(f'- Pedido n° {orderNumber}, de {order[1]}, diz:')

        for ingIndex, ingQuantity in enumerate(order[0]):
            if ingQuantity > 0:
                print(f'---> {ingQuantity} {ing[ingIndex]}')

        time.sleep(1)
    
    if len(orders) == 0:
        print('Nenhum pedido para visualizar no momento.')

    input('\n>> OK <<')
    currentStation()


# função para o pedido do cliente
## modifiquei essa função de forma que ela é apenas responsável por gerar um pedido aleatório, ficou mais como um acessório
## para outras funções
def makeOrder():
    global customersWaiting, orders, size
    names = ['sussy oliveira', 'ednalva', 'lula', 'big smoke', 'walter white', 'jesse pinkman', 'davi', 'joão', 'samuel', 'xandao cabeça de p']
    ing = [0, 0, 0, 0]
    
    for _ in range(2**size):
        ing[random.randint(0, 3)] += 1

    orders.append([ing, random.choice(names), ingameTime]) 


def rateBurger(order, burger, wait_secs):
    prices = {0: 3, 1: 2.25, 2: 1.50, 3: 1.75} ## preço de cada ingrediente (hamburguer, queijo, alface e tomate; respectivamente)
    final_price = 0
    penalty = 0
    satisfaction_level = 100 ## level de satisfacao maximo
    wait_secs -= 15 ## a partir de 15 segundos de espera o cliente começa a ficar insatisfeito
    if (wait_secs < 0):
        wait_secs = 0
    elif (wait_secs > 60):
        wait_secs = 60

    for ind, val in enumerate(burger[0:4]): ## calcula o preço do hambúrguer de acordo com os ingredientes
        final_price += prices[ind] * val
        ## se a quantidade de um tipo de ingrediente n for igual à pedida;
        if order[0][ind] > val: ## se o pedido queria mais de um ingrediente
            penalty += (order[0][ind] - val) * 2
        elif order[0][ind] < val: ## se queria menos
            penalty += val - order[0][ind] # pensar em algo melhor dps ## adicionar a penalty a quantidade de ingredientes errados.
    
    final_price += 2 # bread's expenses

    # aviso: tudo o que envolve o algoritmo de satisfação do cliente nessa função está wip ou é placeholder, ou seja: completamente bugado
    ## finalsatisfaction = penalidade (número de ingredientes incorretos) menos o tempo remanescente de espera
    dissatisfaction = (penalty * 15) + (wait_secs * 1.15) # atual formula de penalidade, apenas placeholder, pensar em uma melhor dps
    final_stats = satisfaction_level - dissatisfaction ## satisfacao total (satisfacao maxima - quantidade de satisfacao perdida)

    if (final_stats <= 10):
        final_price = 0
        if (final_stats < 0):
            final_stats = 0

    elif (final_stats > 100):
        final_stats = 100

    print('\n'*40)
    print(f"\n\o/ <-- {order[1]}\nAqui está o seu hambúrguer, senhor: \n{burger[5]}")
    loadAnimation(3)
    print('\n'*40)

    ratings = {
        90: "Incrível!",
        75: "Bãum.",
        50: "Dá pro gasto.",
        25: "Tá meio bosta, mas vou pagar...",
        10: "Quê? Me recuso a pagar por essa merda.",
        0: "BLEGH"
    }
    for k in ratings:
        if final_stats >= k:
            print(f'\033[1;32m{order[1]}\033[m: {ratings[k]}')
            break
    
    time.sleep(2)
    print('=-'*28, end='=\n')
    print(f'Valor final: R${final_price:.2f}')
    time.sleep(1)
    print(f'Nota: {final_stats}%')
    time.sleep(1)
    input('\n>> OK <<')


##############################################################################################################

#####################
# STATION FUNCTIONS #
#####################


def grillStation():
    global comandoChapa, grill, burgerIDGenerator, showCommands
    pattyToActOn = "0"

    printStationMessage("a", "Chapa", """0: Colocar hambúrguer
1: Virar hambúrguer
2: Tirar hambúrguer
3: Atualizar status dos hambúrgueres""")

    print('\033[1;32m><><><><><><><><>< -=- INFORMAÇÕES -=- ><><><><><><><><><\033[m')
    for id in grill:
        print(f'- Hambúrguer {id}:')
        print(f'---> Topo: {grill[id][1]}%')
        print(f'---> Fundo: {grill[id][0]}%')

    if (len(grill) == 0):
        print('Não há hambúrgueres cozinhando na chapa.')
    print('\033[1;32m><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\033[m\n')
    

    command = input('> ').strip().lower()
    print('\n'*40)


    if (command.isnumeric()):

        if (command == "0"):
            grill[burgerIDGenerator] = [0, 0]
            makeThreadForFunction(burgerTimeCounter, burgerIDGenerator)
            burgerIDGenerator = str(int(burgerIDGenerator) + 1)

        elif (command == "1" or command == "2"):

            if (len(grill) > 0):
                for id in grill:
                    print(f'- Status do hambúrguer {id}:')
                    print(f'---> Topo: {grill[id][1]}%')
                    print(f'---> Fundo: {grill[id][0]}%')
                    print('+-----+-----+')

                print('Digite o número do hambúrguer a ser virado:' if command == "1" else 'Digite o número do hambúrguer a ser removido:')
                pattyToActOn = input('\n> ')
                comandoChapa = f'{pattyToActOn}{command}'
                loadAnimation(0.3) ## allow time for ingameTimeCounter() to update burger status

            else:
                print('Você gira sua espátula no ar. Não há hambúrgueres na chapa...')
                input('\n>> OK <<')
                
        else:
            if command != "3":
                print('Comando inválido!')
                input('\n>> OK <<')

        grillStation()

    else:

        if (command == "v"):
            viewOrders(grillStation)

        elif (command == "cmds"):
            showCommands = not showCommands
            grillStation()

        else:
            navigation("a", command)


def buildStation():
    ## player can only assemble one burger at a time
    ## but they can have multiple assembled burgers in storage.
    global days, burger, burgers, asmbIng, cookedPatties, showCommands
    pattyToAdd = 0
    
    printStationMessage("b", "Montagem", """0: Pão-de-baixo
1: Pão-de-cima
2: Hambúrguer
3: Queijo
4: Alface
5: Tomate""")
    print('\033[1mA montagem acaba quando você coloca o pão-de-cima.\n')
    print('\033[1;35m><><><><><><><><>< -=- INFORMAÇÕES -=- ><><><><><><><><><\033[m\n')
    print(burger)
    print('\033[1;35m><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\033[m\n')


    command = input('> ').strip().lower()
    print('\n'*40)


    if (command.isnumeric()):

        try:

            command = int(command)

            if (asmbIng[6][0] == 0 and command != 0): ## if down-bread hasn't been put down and player put down something else (error condition)
                if command == 1: ## player tries to put down top-bread first (tries to complete the burger even though it has nothing) 
                    raise Exception("Cadê o resto do hambúrguer jumento?") ## merely cosmetical though, the line in the code below would be enough for this if -- davidf
                raise Exception('O prato é o pão-de-baixo agora?') ## player put down an ingredient other than top-bread

            if (asmbIng[6][0] > 1): ## player tried to put down more than one down-bread
                raise Exception("Isso não é um big mac, então por favor não tente colocar mais de um pão-de-baixo (seria mais difícil de programar tlgd).")


            if (command == 2):

                if (len(cookedPatties) > 0):

                    for index, somaDeCozimento in enumerate(cookedPatties):
                        print(f'Hambúrguer {index}: {somaDeCozimento}% cozido')

                    if (len(cookedPatties) > 1):
                        print("\nDigite o número do hambúrguer que você deseja adicionar:")
                        pattyToAdd = int(input('\n> '))

                    asmbIng[6][6] = somaDeCozimento
                    cookedPatties.pop(pattyToAdd)

                else:
                    raise Exception("Não há hambúrguers cozidos disponíveis!")

            asmbIng[6][command] += 1 ## increments to appropriate ingredient counter

            burger = f'{asmbIng[command]}\n{burger}'

            if (asmbIng[6][1] == 1):

                asmbIng[6][7] = burger
                burgers.append(asmbIng[6][2:])

                burger = ""
                asmbIng[6] = [0, 0, 0, 0, 0, 0, 0, ""]

                print('Hambúrguer completo com sucesso! Ele está disponível para ser servido no \033[1;34mCaixa\033[m.')
                input('\n>> OK <<')

        except Exception as e: ## prints the exception
            print(f'Erro!: {e}')
            input('\n>> OK <<')

        finally:
            buildStation()

    else:

        if (command == "v"):
            viewOrders(buildStation)

        elif (command == "cmds"):
            showCommands = not showCommands
            buildStation()

        else:
            navigation("b", command)


def checkoutStation():
    global orders, burgers, customersWaiting, showCommands
    ing = {0: 'hambúrguer', 1: 'queijo', 2: 'alface', 3: 'tomate', 4: [0, 0, 0, 0]}
    customerToGiveBurgerTo = 0
    burgerToGive = 0

    printStationMessage("c", "Caixa", """0: Entregar pedido do cliente
    1: Atender cliente""")

    print('\033[1;34m><><><><><><><><>< -=- INFORMAÇÕES -=- ><><><><><><><><><\033[m')
    if (customersWaiting):
        print(f'\033[1;31m{"Há um cliente esperando ser atendido!":^57}\033[m' if customersWaiting == 1 else f'\033[1;31m{f"Há {customersWaiting} clientes esperando serem atendidos!":^57}\033[m')
    else:
        print('Nenhum cliente esperando ser atendido até o momento.')
    print('\033[1;34m><><><><><><><><><><><><><><><><><><><><><><><><><><><><>\033[m\n')


    command = input('> ').strip().lower()
    print('\n'*40)

    if (command.isnumeric()):

        if (command == "0"):

            if (len(orders) > 0 and len(burgers) > 0):

                print('Há um cliente esperando o seu pedido:' if len(orders) == 1 else f'Há {len(orders)} clientes esperando o seu pedido:')
                time.sleep(1)

                for orderIndex, order in enumerate(orders):
                    print(f'\n- \033[1m{orderIndex}\033[m: Pedido do cliente \033[1;32m{order[1]}\033[m, contendo:')

                    for ingIndex, ingQuantity in enumerate(order[0]):
                        if (ingQuantity > 0):
                            print(f'---> {ingQuantity} {ing[ingIndex]}')

                if (len(orders) > 1):
                    print("\nDigite o número do cliente que você servirá:")
                    customerToGiveBurgerTo = int(input("\n> "))

                if (len(burgers) > 1):
                    time.sleep(1)
                    for i in range(len(burgers)):
                        print(f'- \033[1m{i}\033[m: Hambúrguer contendo:')
                        for ingIndex, ingQuantity in enumerate(burgers[i][:4]):
                            if (ingQuantity > 0):
                                print(f'---> {ingQuantity} {ing[ingIndex]}')

                    print(f"\nHá mais de um hambúrguer pronto! Digite o número do hambúrguer que você dará para \033[1;32m{orders[customerToGiveBurgerTo][1]}\033[m.")
                    burgerToGive = int(input("\n> "))

                loadAnimation(2)
                rateBurger(orders[customerToGiveBurgerTo], burgers[burgerToGive], ingameTime - orders[customerToGiveBurgerTo][2]) 
                orders.pop(customerToGiveBurgerTo)
                burgers.pop(burgerToGive)

            else:

                if (len(orders)) == 0:
                    print('Nenhum cliente está esperando o seu pedido.')

                else:
                    print("Você não tem hambúrguers prontos. Vá montar alguns!")

                input('\n>> OK <<')

            checkoutStation()

        elif (command == "1"):

            if (customersWaiting):

                customersWaiting -= 1
                makeOrder()
                print(f'\n\o/ <--- \033[1;32m{orders[-1][1]}\033[m \n- yo eu quero um hambúrguer com:')
                print('=-'*28, end='=\n')

                for ind, val in enumerate(orders[-1][0]):
                    if (val > 0):
                        print(f'---> {val} {ing[ind]}')

                print('=-'*28, end='=\n')
                print('\nO cliente estará esperando!')

            else:
                print('Nenhum cliente está esperando ser atendido.')

            input('\n>> OK <<')
            checkoutStation()

    else:

        if (command == "v"):
            viewOrders(checkoutStation)

        elif (command == "cmds"):
            showCommands = not showCommands
            checkoutStation()

        elif (command[0] == "f"):

            if (ingameTime >= 240):
                print(f'\033[1mFim do dia {days + 1}!\033[m\n')
                ## ideia: aqui imprimiria as stats do jogador pro dia
                input('\033[36m>> Dia seguinte <<\033[m')

            else:
                print('O seu turno de trabalho ainda não acabou...')
                input('\n>> OK <<')
                checkoutStation()

        else:
            navigation("c", command)


##############################################################################################################

########
# MAIN #
########

def startGame():

    global size, days

    ################################################################################
    ## resets all other global variables
    global comandoChapa, asmbIng, burgerIDGenerator, burger, ingameTime, customersWaiting, orders, burgers, cookedPatties, customerArrivalTimes, grill
    comandoChapa = "XX"
    asmbIng = {
        0: '\033[33m                ⢸⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿\n                ⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠧⠤⠾⠿⠿⠿⠿⠿⠷⠶⠾⠟\033[m', 
        1: '\033[33m                    ⣀⣤⣶⣶⣿⣿⣿⣿⣿⣿⠿⠷⣶⣦⣄⡀\n                 ⢀⣴⣿⣿⣿⣿⣯⣀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄\n                ⢠⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣈⣽⣿⣷⡀\n                ⣿⣿⣶⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣧\n                ⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠧⠤⠾⠿⠿⠿⠿⠿⠷⠶⠾⠟\033[m', 
        2: '\033[31m                ⣠⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣄\n                ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[m', 
        3: '\033[1;33m                ⠈⢷⣤⣴⠟⠉⠻⣄⣠⡾⠋⠙⠳⣤⣴⠟⠉⠳⣦⣠⡾⠃⠙⢷⡄\033[m', 
        4: '\033[1;32m                ⠈⢷⣤⣴⠟⠉⠻⣄⣠⡾⠋⠙⠳⣤⣴⠟⠉⠳⣦⣠⡾⠃⠙⢷⡄\033[m', 
        5: '\033[1;31m                ⣠⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀  ⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣄\n                ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[m', 
        6: [0, 0, 0, 0, 0, 0, 0, ""]
    }
    burgerIDGenerator = "0"
    burger = ""
    ingameTime = 0
    customersWaiting = 0
    orders = []
    burgers = []
    cookedPatties = []
    customerArrivalTimes = [0]
    grill = {}
    ################################################################################

    if (days % 2 == 0): 
        size += 1
    
    nCustomers = random.randint(2, 3) ## plus the first customer
    for _ in range(nCustomers):
        customerArrivalTimes.append(random.randint(20, 220)) # ideia: clientes proporcionais ao nível de avaliação do restaurante (relacionado a variavel rate da func acima)


    print('\n'*40)
    print(f'\033[1mDIA {days + 1}\033[m')
    loadAnimation(3)

    time.sleep(random.randint(1, 5))
    makeThreadForFunction(ingameTimeCounter)
    time.sleep(1)

    checkoutStation()
    
    days += 1
    if (days < 6):
        startGame()


##############################################################################################################
    
#### SETTINGS #####
showCommands = True
###################

while True:
    days = 0
    size = 0

    comandoChapa = 'XX' ## o primeiro índice referencia o hamburguer, o segundo a ação a ser tomada

    asmbIng = {
        0: '\033[33m                ⢸⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿\n                ⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠧⠤⠾⠿⠿⠿⠿⠿⠷⠶⠾⠟\033[m', 
        1: '\033[33m                    ⣀⣤⣶⣶⣿⣿⣿⣿⣿⣿⠿⠷⣶⣦⣄⡀\n                 ⢀⣴⣿⣿⣿⣿⣯⣀⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄\n                ⢠⣿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣁⣈⣽⣿⣷⡀\n                ⣿⣿⣶⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⢿⣧\n                ⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠧⠤⠾⠿⠿⠿⠿⠿⠷⠶⠾⠟\033[m', 
        2: '\033[31m                ⣠⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣄\n                ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[m', 
        3: '\033[1;33m                ⠈⢷⣤⣴⠟⠉⠻⣄⣠⡾⠋⠙⠳⣤⣴⠟⠉⠳⣦⣠⡾⠃⠙⢷⡄\033[m', 
        4: '\033[1;32m                ⠈⢷⣤⣴⠟⠉⠻⣄⣠⡾⠋⠙⠳⣤⣴⠟⠉⠳⣦⣠⡾⠃⠙⢷⡄\033[m', 
        5: '\033[1;31m                ⣠⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀  ⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣄\n                ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿  ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\033[m', 
        6: [0, 0, 0, 0, 0, 0, 0, ""]
    }
    ## update! asmbIng[6][6] is how well the burger is cooked (ranges from 0 to 200)
    ## for exclusive use by buildStation()! using asmbIng anywhere else will potentially break the code.

    ## asmbIng update 2: since the words contained within asmbIng (down-bread, top-bread etc.)  
    ## are only used for displaying the burger graphically in the build station, i have replaced 
    ## them with their respective ascii arts.

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

    notifications.append("\033[1;36mBem-vindo ao Smokin' Burgers!\033[m")
    notifications.append("\033[mAqui no \033[1;34mCaixa\033[m, você pode atender clientes que chegam e entregar hambúrgueres prontos.")
    notifications.append("\033[mPara montar os sanduíches, vá para \033[1;35mMontagem\033[m.")
    notifications.append("\033[mPara fritar hambúrgueres, dirija-se à \033[1;32mChapa\033[m.")
    notifications.append("\033[mO seu turno termina de \033[1m17:00\033[m. Boa sorte!")

    startGame()

    print('\n'*40)
    print('\033[1mFim de jogo!\033[m Gostaríamos de extender encarecidamente os nossos agradecimentos e congratulações pela sua participação nesta experiência e esperamos solenemente que Vossa Senhoria volte a executar o arquivo desta obra novamente no futuro. :moyai: :wine_glass:\n')

    if (input('Quer jogar denovo? (s/n)\n> ').strip().lower() == 'n'): 
        days, size = 0
        break