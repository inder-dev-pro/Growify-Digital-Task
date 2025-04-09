import requests
from bs4 import BeautifulSoup
import json

brands = {
    "Brand1": "https://hmgroup.com/",
    "Brand2": "https://www.nykaa.com/"
}

data = {}

for name, url in brands.items():
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        about_us = ""
        for link in soup.find_all('a', href=True):
            if "about" in link['href'].lower():
                about_url = link['href']
                if not about_url.startswith("http"):
                    about_url = url.rstrip("/") + "/" + about_url.lstrip("/")
                break
        else:
            about_us = "No 'About Us' page found."
            data[name] = {"url": url, "about": about_us}
            continue

        about_res = requests.get(about_url, timeout=10)
        about_soup = BeautifulSoup(about_res.text, 'html.parser')
        paragraphs = about_soup.find_all('p')
        about_us = "\n".join(p.get_text() for p in paragraphs[:5])

        data[name] = {"url": url, "about": about_us}

    except Exception as e:
        data[name] = {"url": url, "about": f"Error fetching: {e}"}

with open("python-scripts/output/brand_info.json", "w") as f:
    json.dump(data, f, indent=4)
