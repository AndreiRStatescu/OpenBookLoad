import requests
from bs4 import BeautifulSoup
from typing import List

from models.novel import Novel, Chapter


class HoneyFeed:
    BASE_URL = "https://www.honeyfeed.fm/novels"
    
    @staticmethod
    def scrape_novel(novel_id: str, chapter_numbers: List[int] = None, start_chapter: int = None, end_chapter: int = None) -> Novel:
        try:
            url = f"{HoneyFeed.BASE_URL}/{novel_id}/chapters"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            title = HoneyFeed._extract_title(soup)
            chapters = HoneyFeed._extract_chapters(soup, chapter_numbers, start_chapter, end_chapter)
            
            return Novel(
                title=title,
                chapters=chapters,
                novel_id=novel_id,
                url=url
            )
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch novel page: {e}")
    
    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
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
                if tag == 'title':
                    title = title.split('|')[0].strip()
                    title = title.split('-')[0].strip()
                return title
        
        raise ValueError("Could not find novel title on page")
    
    @staticmethod
    def _extract_chapters(soup: BeautifulSoup, chapter_numbers: List[int] = None, start_chapter: int = None, end_chapter: int = None) -> List[Chapter]:
        chapters = []
        
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
            chapter_links = soup.find_all('a', href=lambda x: x and '/chapters/' in x)
        else:
            chapter_links = chapter_container.find_all('a')
        
        for idx, link in enumerate(chapter_links, 1):
            should_scrape = True
            
            if chapter_numbers is not None:
                should_scrape = idx in chapter_numbers
            elif start_chapter is not None or end_chapter is not None:
                if start_chapter is not None and idx < start_chapter:
                    should_scrape = False
                if end_chapter is not None and idx > end_chapter:
                    should_scrape = False
            
            if not should_scrape:
                continue
            
            chapter_title = link.get_text(strip=True)
            chapter_url = link.get('href', '')
            
            if chapter_url.startswith('/'):
                chapter_url = f"https://www.honeyfeed.fm{chapter_url}"
            
            if chapter_title and chapter_url:
                content = HoneyFeed._fetch_chapter_content(chapter_url)
                
                chapters.append(Chapter(
                    number=idx,
                    title=chapter_title,
                    url=chapter_url,
                    content=content
                ))
        
        return chapters
    
    @staticmethod
    def _fetch_chapter_content(chapter_url: str) -> str:
        try:
            response = requests.get(chapter_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            chapter_body = soup.find('div', id='chapter-body')
            if chapter_body:
                wrap_body = chapter_body.find('div', class_='wrap-body')
                if wrap_body:
                    pages_container = wrap_body.find('div')
                    if pages_container:
                        page_divs = pages_container.find_all('div', id=lambda x: x and x.startswith('page-'))
                        if page_divs:
                            all_paragraphs = []
                            for page in page_divs:
                                paragraphs = page.find_all('p')
                                all_paragraphs.extend(paragraphs)
                            
                            if all_paragraphs:
                                return HoneyFeed._simplify_html(all_paragraphs)
            
            content_selectors = [
                ('div', {'class': 'chapter-content'}),
                ('div', {'class': 'content'}),
                ('article', {}),
            ]
            
            for tag, attrs in content_selectors:
                content_element = soup.find(tag, attrs)
                if content_element:
                    paragraphs = content_element.find_all('p')
                    if paragraphs:
                        return HoneyFeed._simplify_html(paragraphs)
            
            return ""
        except requests.RequestException as e:
            print(f"Warning: Failed to fetch chapter content from {chapter_url}: {e}")
            return ""
    
    @staticmethod
    def _simplify_html(elements) -> str:
        allowed_tags = {'p', 'br', 'b', 'i', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'}
        result = []
        
        for element in elements:
            simplified = HoneyFeed._process_element(element, allowed_tags)
            if simplified:
                result.append(simplified)
        
        return ''.join(result)
    
    @staticmethod
    def _process_element(element, allowed_tags):
        if element.name is None:
            text = str(element).strip()
            return text if text else ''
        
        if element.name not in allowed_tags:
            processed_children = ''.join(HoneyFeed._process_element(child, allowed_tags) for child in element.children)
            return processed_children
        
        if element.name == 'br':
            return '<br/>'
        
        processed_children = ''.join(HoneyFeed._process_element(child, allowed_tags) for child in element.children)
        
        if not processed_children.strip():
            return ''
        
        return f'<{element.name}>{processed_children}</{element.name}>'
