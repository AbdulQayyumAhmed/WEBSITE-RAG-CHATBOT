import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def scrape_website(start_url, max_pages=20):
    """
    Scrape the main page and follow internal links up to max_pages
    Returns concatenated text of all pages
    """
    visited = set()
    queue = deque([start_url])
    all_texts = []

    domain = urlparse(start_url).netloc

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            # Remove unwanted tags
            for tag in soup(["script", "style", "nav", "footer", "header", "form", "aside"]):
                tag.decompose()

            text = soup.get_text(separator=" ")
            text = " ".join(text.split())
            if text:
                all_texts.append(text)

            # Add internal links to queue
            for link in soup.find_all("a", href=True):
                abs_url = urljoin(url, link['href'])
                if urlparse(abs_url).netloc == domain and abs_url not in visited:
                    queue.append(abs_url)

            visited.add(url)

        except Exception as e:
            print(f"Skipping {url}: {e}")

    return "\n".join(all_texts)