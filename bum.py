import requests
import hashlib
from urllib.parse import urlparse,  parse_qs
from time import sleep
from loguru import logger

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'authorization': 'Bearer false',
    'cache-control': 'no-cache',
    'origin': 'https://app.bums.bot',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.bums.bot/'
}
def compute_md5(amount ,seq):
    prefix = str(amount) + str(seq) + "7be2a16a82054ee58398c5edb7ac4a5a"
    return hashlib.md5(prefix.encode()).hexdigest() 

def genToken(initData):
    query_params = parse_qs(urlparse(initData).fragment)
    tgWebAppData = query_params.get('tgWebAppData', [None])[0]
    data = {
        'invitationCode':  '',
        'initData': tgWebAppData,
    }
    response = requests.post('https://api.bums.bot/miniapps/api/user/telegram_auth', headers=headers, data=data)
    return (response.json())
    
def mine_bums(cred):
    headers['authorization'] = 'Bearer ' +  cred['data']['token']
    data = ''
    #daily check in Api call
    #response = requests.post('https://api.bums.bot/miniapps/api/sign/sign', headers=headers, data=data)
    data = {'count':  '1', 'propId':  '500010001'}
    #spin APi call
    response = requests.post('https://api.bums.bot/miniapps/api/game_spin/Start', headers=headers, data=data)
    params = {'blumInvitationCode': ''}
    response = requests.get('https://api.bums.bot/miniapps/api/user_game_level/getGameInfo', params=params, headers=headers)
    Seq = response.json()['data']['tapInfo']['collectInfo']['collectSeqNo']
    hsh = compute_md5('10000000000000000',Seq)
    params = {
        'collectAmount':'10000000000000000' ,
        'hashCode': hsh,
        'collectSeqNo': str(Seq),
    }
    response = requests.post('https://api.bums.bot/miniapps/api/user_game/collectCoin', headers=headers,data=params)
    logger.info(response.json())
    
if __name__ == '__main__':  
    query = ('https://app.bums.bot/#tgWebAppData=user%3D%257B%2522id%2522%253A5203820046%252C%2522first_name%2522%253A%2522Ymx%2520haxor%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Ymxhaxor%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252Fz7MApv-o-JLTHEsup7BsTe7u-hdH1OpRJqHqKSJZE3mzUDptYO58qUNe0NJheL5A.svg%2522%257D%26chat_instance%3D-3890727516480938454%26chat_type%3Dsender%26auth_date%3D1731855924%26signature%3DF_W72lp5N7L1eMQUz0htIalPgQ4EzugmKyA12bKWqsGECCYZH-kvE8rRffVOCxpOWdBteKAQjMBAw4FTA-PeCQ%26hash%3Dbc1f0c34ffe04a3eefc02802e12fcd6b16db0fb91c0462d608242593dc39dc23&tgWebAppVersion=7.10&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23ffffff%22%2C%22section_bg_color%22%3A%22%23ffffff%22%2C%22secondary_bg_color%22%3A%22%23f0f0f0%22%2C%22text_color%22%3A%22%23222222%22%2C%22hint_color%22%3A%22%23a8a8a8%22%2C%22link_color%22%3A%22%232678b6%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23527da3%22%2C%22accent_text_color%22%3A%22%231c93e3%22%2C%22section_header_text_color%22%3A%22%233a95d5%22%2C%22subtitle_text_color%22%3A%22%2382868a%22%2C%22destructive_text_color%22%3A%22%23cc2929%22%2C%22section_separator_color%22%3A%22%23d9d9d9%22%2C%22bottom_bar_bg_color%22%3A%22%23f0f0f0%22%7D')
    re = genToken(query)
    while True:    
        mine_bums(re)
        sleep(10)
