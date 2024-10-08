import ast, threading
import re,ast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

coloumb_data = {0:'ID',1:'Egg',2:'Accessories',3:'Backs',4:'Body',5:'Card',6:'Element',7:'Eyes',8:'Face Details',9:'Glasses',10:'Hats',11:'Mouth',12:'Moves',13:'Moves',14:'Moves',15:'Moves',16:'Tails',17:'Wings',18:'Price'}

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=chrome_options)

def get_source_code(asset_id):
    # browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get(f"https://opensea.io/assets/0x4e76c23fe2a4e37b5e07b5625e17098baab86c18/{asset_id}")
    html = browser.page_source
    # browser.quit()
    return html.replace('\u0393','')

def get_traits(data):
    regex = r'"traitType":".{1,15}","value":".{1,15}","traitCount"'
    results = re.findall(regex, data)
    stripped = [s.replace(',"traitCount"','') for s in set(results)]
    traits = []
    for i in stripped:
        dict = ast.literal_eval('{'+i+'}')
        traits.append(dict)
    return traits

def get_price(data):
    regex = r'<div class="Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Price--amount" tabindex="-1">.{0,6}<!-- --> <span class="Price--raw-symbol">'
    before = '<div class="Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Price--amount" tabindex="-1">'
    after = '<!-- --> <span class="Price--raw-symbol">'
    results = re.findall(regex, data)
    if results:
        print(results)
        price = results[0].strip(before).strip(after)
    else:
        price = ' '
    return price



def write_to_file(asset_id,traits,price):
    line = []
    with open('data.csv','a+', encoding="utf-8") as f:
        for coloumb in coloumb_data:
            if coloumb == 0:
                data = asset_id
            if coloumb == 18:
                data = price
            for trait in traits:
                if trait['traitType'] == coloumb_data[coloumb] and trait['value'] != ' ':
                    data = trait['value']
                    traits.remove(trait)
            if not data:
                data = ' '
            line.append(data)
            data = None
        line = str(line)[1:-1].replace("'","")
        f.write(line+'\n')



def get_properties(asset_id):
    data = get_source_code(asset_id)
    traits = get_traits(data)
    price = get_price(data)
    if price != ' ':
        write_to_file(asset_id,traits,price)

threads = []
for i in range(2000,10000):
    if i % 10 == 0:
        for thread in threads:
            thread.join()
        threads = []
    thread = threading.Thread(target=get_properties, args=(i,))
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()



