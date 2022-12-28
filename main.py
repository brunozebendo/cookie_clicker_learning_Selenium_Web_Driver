"""o objetivo do código é automatizar o jogo do biscoito, onde se clica em um cookie e se ganha
recompensas, essas recompensas mudam, por isso é preciso verificar de forma atualizada quais foram as
recompensas."""
"""importadas as bibliotecas selenium, para a automatização e time, para lidar com o tempo de espera de cada
coisa"""
from selenium import webdriver
import time
"""aqui, a sintaxe básica do driver que vai lidar com o navegador escolhido, e o endereço de e-mail que se 
vai lidar"""
chrome_driver_path = "C:\chromedriver\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
"""aqui o código para encontrar o elemento, nesse caso, pelo ID (nome de identificação)"""
#Get cookie to click on.
cookie = driver.find_element(By.ID, 'cookie')
"""aqui o programa vai encontrando os itens de upgrade pelo CSS deles, depois, um list comprehension
guarda em um dicionário os itens encontrados"""
#Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]
"""aqui são as constantes iniciais para lidar com o tempo, usando a função time da biblioteca time, para
especificar o cinco segundos para verificação dos itens e cinco minutos para cada partida"""
timeout = time.time() + 5
five_min = time.time() + 60*5 # 5minutes
"""aqui as regras do jogo são iniciadas com um while e a função click, depois o código verifica se o tempo
atual é maior que o timeout, ou seja, como o timeout acumula o tempo atual mais 5, é justamente o intervalo
necessário. Se for maior, ele vai guardar todos os preços dos upgrades no dicionário item_prices"""
while True:
    cookie.click()

    #Every 5 seconds:
    if time.time() > timeout:

        #Get all upgrade <b> tags
        all_prices = driver.find_elements (By.CSS_SELECTOR, '#store b')
        item_prices = []
"""aqui se converte o preço em um texto, substituindo a string , pelo divisor de int , . O if diz
que se o element for diferente de vazio, o cost vai receber um inteiro(int) que será o resultado da string
dividida (split) e com a subistituição(replace), ou seja, a string trabalhada para ficar no formato certo dentro do dicionário. 
Por fim, usa-se o append para adicionar o item"""
#Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)
"""cria um dicionário iterando pelo comprimento do item_prices, ou seja, acima ele cria o dicionário e aqui
passa a regra para preenche-lo, """
        #Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]
"""aqui, se pega o elemento id money, que é o número de cliques, em formato de texto, se ele 
vier com uma vírgula, ela será substituída, aqui me parece o caso de substituir uma string
por uma vírgula de separação de um int"""
        #Get current cookie count
        money_element = driver.find_element(By.id, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)
"""aqui o código verifica se a contagem de biscoito é maior do que o preço do item, se for, ele guarda
o id do item"""
        #Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id
"""depois de guardar os itens acessíveis, o programa usa a função mas para guardar o item mais caro"""
        #Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
"""aqui é o comando de clicar no item"""
        driver.find_element(By.id, to_purchase_id).click()
"""aqui o comando novamente de clicar após cinco segundos"""
        #Add another 5 seconds until the next check
        timeout = time.time() + 5

    #After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.id, 'cps').text
        print(cookie_per_s)
        break

