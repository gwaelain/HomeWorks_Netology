import requests
url_for_heroes = 'https://akabab.github.io/superhero-api/api/all.json'
our_heroes_list = ['Hulk', 'Captain America', 'Thanos']

def search_heroes(url, heroes_list):
    response = requests.get(url).json()
    cleverest_hero = ''
    best_intell = 0
    for name in heroes_list:
        for item in response:
            if name == item['name']:
                intell = item['powerstats']['intelligence']
                if intell > best_intell:
                    cleverest_hero = item['name']
                    best_intell = item['powerstats']['intelligence']
    return f'Самый умный герой - {cleverest_hero}, с интеллектом: {best_intell}.'

if __name__ == '__main__':
      print(search_heroes(url_for_heroes, our_heroes_list))