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
    query = ('https://app.bums.bot/#tgWebAppData=query_id%3DAAEO_is2AgAAAA7-KzZeQXqs%26user%3D%257B%2522id%2522%253A5203820046%252C%2522first_name%2522%253A%2522Ymx%2520haxor%2522%252C%2522last_name%2522%253A%2522%2522%252C%2522username%2522%253A%2522Ymxhaxor%2522%252C%2522language_code%2522%253A%2522en%2522%252C%2522allows_write_to_pm%2522%253Atrue%252C%2522photo_url%2522%253A%2522https%253A%255C%252F%255C%252Ft.me%255C%252Fi%255C%252Fuserpic%255C%252F320%255C%252Fz7MApv-o-JLTHEsup7BsTe7u-hdH1OpRJqHqKSJZE3mzUDptYO58qUNe0NJheL5A.svg%2522%257D%26auth_date%3D1732634971%26signature%3DY5bwyIhjlQAQQ6-EDJ1BWxTdFgtVVQf4u9cFs_-wvckRptjj8ik-54ebaJZf1AZGY6RlxTu0-A2Pkc7FmqK5DA%26hash%3Da1efd6840c3966ee70daa773e05cfa68bf4071d7b486808b09c3198e1993fca2&tgWebAppVersion=7.8&tgWebAppPlatform=android&tgWebAppThemeParams=%7B%22bg_color%22%3A%22%23212d3b%22%2C%22section_bg_color%22%3A%22%231d2733%22%2C%22secondary_bg_color%22%3A%22%23151e27%22%2C%22text_color%22%3A%22%23ffffff%22%2C%22hint_color%22%3A%22%237d8b99%22%2C%22link_color%22%3A%22%235eabe1%22%2C%22button_color%22%3A%22%2350a8eb%22%2C%22button_text_color%22%3A%22%23ffffff%22%2C%22header_bg_color%22%3A%22%23242d39%22%2C%22accent_text_color%22%3A%22%2364b5ef%22%2C%22section_header_text_color%22%3A%22%2379c4fc%22%2C%22subtitle_text_color%22%3A%22%237b8790%22%2C%22destructive_text_color%22%3A%22%23ee686f%22%2C%22section_separator_color%22%3A%22%230d1218%22%7D')
    re = genToken(query)
    while True:    
        mine_bums(re)
        sleep(10)
