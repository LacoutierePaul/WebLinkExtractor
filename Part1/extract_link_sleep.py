#!/usr/bin/env python3
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import sys
import time
import sys
def extract_links(url):
    """
    Récupère tous les liens href sur la page URL.
    Retourne une liste d'URLs absolues.
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Construire l'URL absolue
        abs_url = urljoin(url, href)
        links.add(abs_url)
    return list(links)

def main():
    parser = argparse.ArgumentParser(description="Extract links from URLs")
    parser.add_argument('-u', '--url', action='append', required=True, help="URL(s) to extract links from")
    parser.add_argument('-o', '--output', choices=['stdout', 'json'], default='stdout', help="Output format")
    args = parser.parse_args()

    if args.output == 'stdout':
        # Affiche chaque URL absolue sur une ligne
        for url in args.url:
            links = extract_links(url)
            for link in links:
                print(link)
    else:
        # Sortie JSON : { base_url: [paths_relative] }
        result = {}
        for url in args.url:
            links = extract_links(url)
            base = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
            paths = []
            for link in links:
                parsed_link = urlparse(link)
                # Vérifier que le domaine est le même
                if f"{parsed_link.scheme}://{parsed_link.netloc}" == base:
                    paths.append(parsed_link.path or '/')
                else:
                    # Optionnel: Ignorer ou gérer les liens externes
                    pass
            result[base] = list(set(paths))  # unique paths
        print(json.dumps(result, indent=2))

    print("[INFO] Script completed, now sleeping to keep pod alive.")
    while True:
        time.sleep(3600)  # sleeps one hour in loop, so forever

if __name__ == '__main__':
    main()
