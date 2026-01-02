import requests
from bs4 import BeautifulSoup

def extract_layout(url):
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    structure = {
        "header": bool(soup.find("header")),
        "nav": bool(soup.find("nav")),
        "sections": len(soup.find_all("section")),
        "main": bool(soup.find("main")),
        "footer": bool(soup.find("footer")),
    }

    return structure
