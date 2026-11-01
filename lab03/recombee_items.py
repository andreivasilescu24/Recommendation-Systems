import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException
import os
from dotenv import load_dotenv

load_dotenv()

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
DB_NAME = os.getenv('DB_NAME')
PRIVATE_TOKEN = os.getenv('PRIVATE_TOKEN')

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region.EU_WEST)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = '../books.csv'

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")
    
    requests = []
    
    for index, row in df.iterrows():
        # TODO 3: Extrageti ID-ul unic al produsului din coloana corespunzatoare din CSV
        item_id = str(row['isbn13'])
        
        # TODO 4: Mapati proprietatile definite anterior cu valorile din randul curent
        # Exemplu:
        properties = {
            "title": str(row['title']),
            "subtitle": str(row['subtitle']),
            "authors": str(row['authors']),
            "categories": str(row['categories']),
            "description": str(row['description']),
            "average_rating": float(row['average_rating']),
            "thumbnail": str(row['thumbnail'])
        }

        if pd.notna(row['published_year']):
            properties["published_year"] = int(row['published_year'])
        if pd.notna(row['num_pages']):
            properties["num_pages"] = int(row['num_pages'])
        if pd.notna(row['ratings_count']):
            properties["ratings_count"] = int(row['ratings_count'])
        
        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))
        
        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            client.send(Batch(requests))
            requests = []
            print("S-a trimis un lot de 100 item-uri...")
            
    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        client.send(Batch(requests))
        print("S-a trimis ultimul lot de item-uri.")
        
    print("Toate item-urile au fost trimise cu succes!")

if __name__ == "__main__":
    send_items()
