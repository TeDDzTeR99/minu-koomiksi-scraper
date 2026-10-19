import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_smbc(num_comics=5):
    """
    Scrapes the latest comic images from Saturday Morning Breakfast Cereal (SMBC).
    """
    base_url = "https://www.smbc-comics.com/"
    current_url = base_url
    
    os.makedirs("smbc_comics", exist_ok=True)
    print(f"Alustatakse SMBC koomiksite scrapimist...")

    for i in range(num_comics):
        try:
            response = requests.get(current_url)
            if response.status_code != 200:
                print(f"Viga lehe laadimisel: {current_url}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Otsi koomiksi pildi element
            comic_img = soup.find('img', id='cc-comic')
            if not comic_img:
                print(f"Koomiksi pilti ei leitud lehelt: {current_url}")
                break

            img_url = comic_img.get('src')
            if not img_url.startswith('http'):
                img_url = urljoin(base_url, img_url)

            # Otsi eelmise koomiksi nupp / link
            prev_link = soup.find('a', class_='cc-prev')
            
            # Laadi pilt alla
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # Võta pildi nimi URL-ist
                img_name = os.path.basename(img_url.split('?')[0])
                file_path = os.path.join("smbc_comics", f"{i+1}_{img_name}")
                
                with open(file_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Salvestatud: {file_path}")
            else:
                print(f"Pildi allalaadimine ebaõnnestus: {img_url}")

            if prev_link and prev_link.get('href'):
                current_url = prev_link.get('href')
                if not current_url.startswith('http'):
                    current_url = urljoin(base_url, current_url)
            else:
                print("Eelmist koomiksit ei leitud. Jõuti algusesse.")
                break

        except Exception as e:
            print(f"Tekkis viga: {e}")
            break

    print("Scrapimine lõpetatud!")

if __name__ == "__main__":
    scrape_smbc(5)
