import requests
from pathlib import Path

URL = "https://collectionapi.metmuseum.org"
SEARCH_STR = "woman+statue"
DOWNLOAD_DIR = 'images'

def download_image(img_url):
    remove_https = img_url.replace('https://', '')
    file_name = Path(remove_https).name
    file_path = Path(f'./{DOWNLOAD_DIR}/{file_name}')
    image_data = requests.get(img_url).content
    print(f'Checking if {file_path} exists...')
    if not file_path.exists():
        print(f'Downloading from {img_url}...')
        with open(file_path, 'wb') as f:
            f.write(image_data)

def image_url(id):
    response = requests.get(f"{URL}/public/collection/v1/objects/{id}")
    response_json = response.json()
    primary_url = response_json.get('primaryImage', None)
    if not primary_url:
        print(f'No primary URL found for id: {id}')
    return primary_url

def search_objs():
    response = requests.get(f"{URL}/public/collection/v1/search", 
                           params={'q': SEARCH_STR, 'medium': 'Sculpture'})
    response_json = response.json()
    obj_ids = response_json['objectIDs']
    print(f'Found {len(obj_ids)} object IDs from API')
    return obj_ids

if __name__ == "__main__":
    ids = search_objs()
    for id in ids:
        url = image_url(id)
        if url:
            download_image(url)
