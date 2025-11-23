"""HoneyFeed scraping service."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

from models.novel import Novel, Chapter


class HoneyFeedScraper:
    """Service class for scraping novel data from HoneyFeed."""
    
    BASE_URL = "https://www.honeyfeed.fm/novels"
    
    def __init__(self, novel_id: str):
        """
        Initialize the HoneyFeed scraper.
        
        Args:
            novel_id: The ID of the novel to scrape
        """
        self.novel_id = novel_id
        self.url = f"{self.BASE_URL}/{novel_id}"
    
    def scrape_novel(self) -> Novel:
        """
        Scrape novel information from HoneyFeed.
        
        Returns:
            Novel object containing the novel title and list of chapters
            
        Raises:
            requests.RequestException: If the request fails
            ValueError: If the page structure is unexpected
        """
        try:
            # Fetch the page
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract chapters
            chapters = self._extract_chapters(soup)
            
            return Novel(
                title=title,
                chapters=chapters,
                novel_id=self.novel_id,
                url=self.url
            )
            
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch novel page: {e}")
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the novel title from the page."""
        # Try common selectors for novel title
        title_selectors = [
            ('h1', {'class': 'novel-title'}),
            ('h1', {}),
            ('div', {'class': 'title'}),
            ('title', {})
        ]
        
        for tag, attrs in title_selectors:
            element = soup.find(tag, attrs)
            if element:
                title = element.get_text(strip=True)
                # Clean up title if it comes from <title> tag
                if tag == 'title':
                    title = title.split('|')[0].strip()
                    title = title.split('-')[0].strip()
                return title
        
        raise ValueError("Could not find novel title on page")
    
    def _extract_chapters(self, soup: BeautifulSoup) -> List[Chapter]:
        """Extract the list of chapters from the page."""
        chapters = []
        
        # Try to find chapter list containers
        chapter_selectors = [
            ('div', {'class': 'chapter-list'}),
            ('ul', {'class': 'chapters'}),
            ('div', {'class': 'chapters'}),
        ]
        
        chapter_container = None
        for tag, attrs in chapter_selectors:
            chapter_container = soup.find(tag, attrs)
            if chapter_container:
                break
        
        if not chapter_container:
            # Try to find all links that look like chapters
            chapter_links = soup.find_all('a', href=lambda x: x and '/chapters/' in x)
        else:
            chapter_links = chapter_container.find_all('a')
        
        for idx, link in enumerate(chapter_links, 1):
            chapter_title = link.get_text(strip=True)
            chapter_url = link.get('href', '')
            
            # Make URL absolute if it's relative
            if chapter_url.startswith('/'):
                chapter_url = f"https://www.honeyfeed.fm{chapter_url}"
            
            if chapter_title and chapter_url:
                chapters.append(Chapter(
                    number=idx,
                    title=chapter_title,
                    url=chapter_url
                ))
        
        return chapters
