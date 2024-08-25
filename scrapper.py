from pymongo import MongoClient
from config import MONGO_DB_CLIENT_URI

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from typing import List,NamedTuple

client = MongoClient(MONGO_DB_CLIENT_URI)
db = client.personal_project
pokemon_collection = db.pokemon

scraped_pokemon_data = []



class Pokemon(NamedTuple):
    id: int
    name: str
    avatar: str
    details_path: str
    types: List[str]
    total: int
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: str
    

url =  'https://pokemondb.net/pokedex/all'
request = Request(
    url,
    headers={'User-Agent': 'Mozilla/5.0'}
    
)
page = urlopen(request)
page_content_bytes = page.read()
page_html = page_content_bytes.decode('utf-8')

soup = BeautifulSoup(page_html, "html.parser")

pokemon_rows = soup.find_all("table", id="pokedex")[0].find_all("tbody")[0].find_all("tr")

scraped_count = 0
for pokemon in pokemon_rows[0:10]:
    pokemon_data = pokemon.find_all("td")
    id = pokemon_data[0]['data-sort-value']
    avatar = pokemon_data[0].find_all("picture")[0].find_all("img")[0]['src']
    if pokemon_data[1].find_all("small"):
        name = pokemon_data[1].find_all("small")[0].getText()
    else:
        name = name = pokemon_data[1].find_all("a")[0].getText()
 
    types = []
    for pokemon_type in pokemon_data[2].find_all("a"):
        types.append(pokemon_type.getText())
    
    details_uri = pokemon_data[1].find_all("a")[0]['href']
    total = pokemon_data[3].getText()
    hp =  pokemon_data[4].getText()
    attack = pokemon_data[5].getText()
    defense = pokemon_data[6].getText()
    sp_attack = pokemon_data[7].getText()
    sp_defense = pokemon_data[8].getText()
    speed = pokemon_data[9].getText()
    
    typed_pokemon = Pokemon(
        id = int(id),
        name = name,
        avatar= avatar,
        details_path = details_uri,
        types = types,
        total = int(total),
        hp = int(hp),
        attack=int(attack),
        defense=int(defense),
        sp_attack=int(sp_attack),
        sp_defense=int(sp_defense),
        speed=int(speed),
        
    )
    
    scraped_pokemon_data.append(typed_pokemon)
    
    
    pokemon_collection.insert_one(
        {
            "id": typed_pokemon.id,
            "name": typed_pokemon.name,
            "avatar": typed_pokemon.avatar,
            "details_path": typed_pokemon.details_path,
            "types": typed_pokemon.types,
            "total": typed_pokemon.total,
            "hp": typed_pokemon.hp,
            "attack": typed_pokemon.attack,
            "defense": typed_pokemon.defense,
            "sp_attack": typed_pokemon.sp_attack,
            "sp_defense": typed_pokemon.sp_defense,
            "speed": typed_pokemon.speed,

        }
    )
    
    
    
