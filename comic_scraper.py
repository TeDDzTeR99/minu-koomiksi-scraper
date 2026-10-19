import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_smbc(num_comics=5):
    """
    Scrapes the latest comic images from Saturday Morning Breakfast Cereal (SMBC).
    """
    base_url = "https://smbc-comics.com"
    current_url = base_url
    
    os.makedirs("smbc_comics", exist_ok=True)
    print("Starting SMBC comic scraping...")

    for i in range(num_comics):
        try:
            response = requests.get(current_url)
            if response.status_code != 200:
                print(f"Error loading page: {current_url}")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the comic image element
            comic_img = soup.find('img', id='cc-comic')
            if not comic_img:
                print(f"Comic image not found on page: {current_url}")
                break

            img_url = comic_img.get('src')
            if not img_url.startswith('http'):
                img_url = urljoin(base_url, img_url)

            # Find the previous comic button / link
            prev_link = soup.find('a', class_='cc-prev')
            
            # Download the image
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                # Get the image name from the URL
                img_name = os.path.basename(img_url.split('?')[0])
                file_path = os.path.join("smbc_comics", f"{i+1}_{img_name}")
                
                with open(file_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Saved: {file_path}")
            else:
                print(f"Failed to download image: {img_url}")

            if prev_link and prev_link.get('href'):
                current_url = prev_link.get('href')
                if not current_url.startswith('http'):
                    current_url = urljoin(base_url, current_url)
            else:
                print("Previous comic not found. Reached the beginning.")
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    print("Scraping finished!")

if __name__ == "__main__":
    scrape_smbc(5)
