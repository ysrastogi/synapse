import asyncio
import aiohttp
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from urllib.parse import urlparse, urljoin, urldefrag
from urllib.robotparser import RobotFileParser
import logging
import time
import warnings
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import Pipeline
from connections.db import setup_url_cache_database

# Suppress the specific warning
warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

class EnhancedURLContentExtractor:
    def __init__(self, base_url=None, html_content=None, tags=['h1', 'h2', 'h3', 'p', 'div', 'section', 'body', 'span', 'article', 'main', 'ul', 'ol', 'li'], max_depth=2, max_pages=100, db_file='url_cache.db'):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.base_url = base_url
        self.html_content = html_content
        self.tags = tags
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.pages_fetched = 0
        # self.setup_content_classifier()

        if base_url:
            self.base_parsed_url = urlparse(base_url)
            self.robots_parser = RobotFileParser()
            self.robots_parser.set_url(urljoin(base_url, 'robots.txt'))
            try:
                self.robots_parser.read()
            except Exception as e:
                print(f"Error reading robots.txt: {e}")

    # def setup_content_classifier(self):
    #     self.classifier = Pipeline([
    #         ('tfidf', TfidfVectorizer()),
    #         ('clf', MultinomialNB())
    #     ])
    #     # You would typically train this classifier on a labeled dataset
    #     # For demonstration, we'll use a very simple mock training
    #     X = ["This is an article about AI", "Buy our new product now!", "Breaking news: New discovery"]
    #     y = ["article", "product", "news"]
    #     self.classifier.fit(X, y)

    async def fetch_html(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    # self.cache_url(url, content)
                    return content
                else:
                    logging.error(f"Error fetching {url}: HTTP {response.status}")
                    return None
        except Exception as e:
            logging.error(f"Error fetching {url}: {str(e)}")
            return None

    def cache_url(self, url, content):
        self.cursor.execute('''
            INSERT OR REPLACE INTO url_cache (url, content, last_fetched)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (url, content))
        self.conn.commit()

    def get_cached_content(self, url):
        self.cursor.execute('SELECT content FROM url_cache WHERE url = ?', (url,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def classify_content(self, text):
        return self.classifier.predict([text])[0]

    async def process_url(self, session, url, depth=0):
        if depth > self.max_depth or self.pages_fetched >= self.max_pages:
            return []

        # cached_content = self.get_cached_content(url)
        # if cached_content:
        #     html_content = cached_content
        # else:
        html_content = await self.fetch_html(session, url)
        if not html_content:
            return []

        # Log the html_content to debug
        logging.debug(f"Fetched HTML content for {url}: {html_content[:100]}...")  # Log first 100 characters

        soup = BeautifulSoup(html_content, 'lxml')
        segments = self.process_soup(soup)
        self.pages_fetched += 1

        # Classify the content of the page
        full_text = ' '.join([seg['text'] for seg in segments])
        # classification = self.classify_content(full_text)
        # for segment in segments:
        #     segment['classification'] = classification

        # Extract and process links
        links = self.extract_links(soup, url)
        for link in links:
            if self.pages_fetched < self.max_pages:
                segments.extend(await self.process_url(session, link, depth + 1))

        return segments

    def process_soup(self, soup):
        segments = []
        for tag in soup.find_all(self.tags):
            segment = {
                'tag': tag.name,
                'text': tag.get_text(strip=True),
                'attributes': dict(tag.attrs)
            }
            segments.append(segment)
        return segments

    def extract_links(self, soup, base_url):
        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = urljoin(base_url, a_tag['href'])
            link = urldefrag(link)[0]
            if self.is_valid_url(link):
                links.add(link)
        return links

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return (parsed.netloc == self.base_parsed_url.netloc and
                parsed.scheme in ('http', 'https'))

    async def crawl(self):
        async with aiohttp.ClientSession() as session:
            return await self.process_url(session, self.base_url)

    def run(self):
        if self.base_url:
            return asyncio.run(self.crawl())
        elif self.html_content:
            soup = BeautifulSoup(self.html_content, 'lxml')
            return self.process_soup(soup)
        else:
            raise ValueError("Either base_url or html_content must be provided.")

# Usage example:
# extractor = EnhancedURLContentExtractor(base_url="https://python-client.qdrant.tech/")
# results = extractor.run()
# for result in results:
#     print(f"Tag: {result['tag']}, Classification: {result['classification']}")
#     print(f"Text: {result['text'][:100]}...")  # Print first 100 characters
#     print("---")