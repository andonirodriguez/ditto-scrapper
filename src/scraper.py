"""
Scraper principal para theobjetive.com
"""

import requests
from bs4 import BeautifulSoup
import time
import logging
from urllib.parse import urlparse, urljoin
from datetime import datetime
import re

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DittoScraper:
    """Scraper para extraer información de theobjetive.com"""
    
    def __init__(self):
        self.base_url = "https://theobjective.com"
        self.allowed_domain = "theobjective.com"
        self.session = requests.Session()
        # Headers para simular un navegador real
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def _validate_url(self, url: str) -> str:
        """
        Valida que la URL pertenezca al dominio permitido
        
        Args:
            url: URL a validar
            
        Returns:
            URL completa y validada
            
        Raises:
            ValueError: Si la URL no pertenece al dominio permitido
        """
        # Si es una URL relativa, la convertimos a absoluta
        if not url.startswith(('http://', 'https://')):
            url = urljoin(self.base_url, url)
        
        parsed_url = urlparse(url)
        
        # Verificar que el dominio sea theobjective.com o un subdominio
        if not (parsed_url.netloc == self.allowed_domain or 
                parsed_url.netloc.endswith(f'.{self.allowed_domain}')):
            raise ValueError(f"URL no permitida. Debe pertenecer al dominio {self.allowed_domain}. URL recibida: {url}")
        
        return url
    
    def get_page(self, url: str) -> BeautifulSoup:
        """
        Obtiene el contenido de una página web
        
        Args:
            url: URL de la página a scrapear
            
        Returns:
            BeautifulSoup object con el contenido parseado
            
        Raises:
            ValueError: Si la URL no pertenece al dominio permitido
            requests.RequestException: Si hay errores en la petición HTTP
        """
        try:
            # Validar la URL antes de hacer la petición
            validated_url = self._validate_url(url)
            
            logger.info(f"Scrapeando: {validated_url}")
            response = self.session.get(validated_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except ValueError as e:
            logger.error(f"Error de validación de URL: {e}")
            raise
        except requests.RequestException as e:
            logger.error(f"Error al acceder a {url}: {e}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Limpia y normaliza texto extraído"""
        if not text:
            return ""
        # Eliminar espacios extra y saltos de línea
        text = re.sub(r'\s+', ' ', text.strip())
        return text
    
    def _extract_date(self, soup: BeautifulSoup) -> str:
        """Extrae la fecha de publicación del artículo"""
        date_patterns = [
            # Meta tags
            {'name': 'meta', 'attrs': {'property': 'article:published_time'}},
            {'name': 'meta', 'attrs': {'name': 'date'}},
            {'name': 'meta', 'attrs': {'name': 'publish_date'}},
            # Time elements
            {'name': 'time', 'attrs': {'datetime': True}},
            {'name': 'time', 'attrs': {}},
            # Class patterns
            {'name': ['div', 'span', 'p'], 'attrs': {'class': lambda x: x and any(
                keyword in ' '.join(x).lower() for keyword in ['date', 'time', 'published', 'fecha']
            )}}
        ]
        
        for pattern in date_patterns:
            elements = soup.find_all(pattern['name'], pattern['attrs'])
            for elem in elements:
                if pattern['name'] == 'meta':
                    date_text = elem.get('content', '')
                elif pattern['name'] == 'time':
                    date_text = elem.get('datetime', '') or elem.get_text(strip=True)
                else:
                    date_text = elem.get_text(strip=True)
                
                if date_text:
                    return self._clean_text(date_text)
        
        return ""
    
    def scrape_article_content(self, url: str) -> dict:
        """
        Extrae el contenido completo de un artículo específico
        
        Args:
            url: URL del artículo a scrapear
            
        Returns:
            Diccionario con el contenido del artículo
        """
        soup = self.get_page(url)
        article_data = {
            'url': url,
            'title': '',
            'subtitle': '',
            'author': '',
            'date': '',
            'content': '',
            'tags': [],
            'category': ''
        }
        
        try:
            # Extraer título
            title_selectors = [
                'h1',
                '[class*="title"]',
                '[class*="headline"]',
                '.entry-title',
                'article h1'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    article_data['title'] = self._clean_text(title_elem.get_text())
                    break
            
            # Extraer subtítulo
            subtitle_selectors = [
                '[class*="subtitle"]',
                '[class*="summary"]',
                '[class*="excerpt"]',
                '.entry-summary'
            ]
            
            for selector in subtitle_selectors:
                subtitle_elem = soup.select_one(selector)
                if subtitle_elem:
                    article_data['subtitle'] = self._clean_text(subtitle_elem.get_text())
                    break
            
            # Extraer autor
            author_selectors = [
                '[class*="author"]',
                '[class*="byline"]',
                '[rel="author"]',
                '.entry-author'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    article_data['author'] = self._clean_text(author_elem.get_text())
                    break
            
            # Extraer fecha
            article_data['date'] = self._extract_date(soup)
            
            # Extraer contenido principal
            content_selectors = [
                'article',
                '[class*="content"]',
                '[class*="article-body"]',
                '[class*="entry-content"]',
                '.post-content',
                'main'
            ]
            
            content_text = []
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    # Buscar párrafos dentro del contenido
                    paragraphs = content_elem.find_all('p')
                    for p in paragraphs:
                        p_text = self._clean_text(p.get_text())
                        if len(p_text) > 20:  # Filtrar párrafos muy cortos
                            content_text.append(p_text)
                    
                    if content_text:
                        break
            
            article_data['content'] = '\n\n'.join(content_text)
            
            # Extraer tags/etiquetas
            tag_selectors = [
                '[class*="tag"]',
                '[class*="label"]',
                '[class*="category"]'
            ]
            
            tags = []
            for selector in tag_selectors:
                tag_elems = soup.select(selector)
                for tag_elem in tag_elems:
                    tag_text = self._clean_text(tag_elem.get_text())
                    if tag_text and tag_text not in tags:
                        tags.append(tag_text)
            
            article_data['tags'] = tags[:10]  # Limitar a 10 tags
            
            # Extraer categoría desde la URL o breadcrumbs
            url_parts = url.split('/')
            if len(url_parts) > 3:
                potential_category = url_parts[3]
                if potential_category != 'www':
                    article_data['category'] = potential_category
            
            logger.info(f"Artículo extraído exitosamente: {article_data['title'][:50]}...")
            
        except Exception as e:
            logger.error(f"Error extrayendo contenido del artículo: {e}")
            
        return article_data
    
    def scrape_articles(self, url: str = None) -> list:
        """
        Extrae artículos de una página específica o de la página principal
        
        Args:
            url: URL específica a scrapear. Si es None, usa la página principal
            
        Returns:
            Lista de diccionarios con información de los artículos
        """
        target_url = url if url else self.base_url
        soup = self.get_page(target_url)
        articles = []
        
        # Ejemplo básico: buscar elementos que podrían ser artículos
        try:
            # Buscar posibles contenedores de artículos
            potential_articles = soup.find_all(['article', 'div'], class_=lambda x: x and any(
                keyword in x.lower() for keyword in ['article', 'post', 'news', 'story', 'content']
            ))
            
            for article_elem in potential_articles:
                article_data = {}
                
                # Intentar extraer título
                title_elem = article_elem.find(['h1', 'h2', 'h3', 'h4'], class_=lambda x: x and any(
                    keyword in x.lower() for keyword in ['title', 'heading', 'headline']
                ))
                if title_elem:
                    article_data['title'] = title_elem.get_text(strip=True)
                
                # Intentar extraer enlace
                link_elem = article_elem.find('a', href=True)
                if link_elem:
                    article_data['link'] = urljoin(target_url, link_elem['href'])
                
                # Solo agregar si tiene al menos título o enlace
                if article_data.get('title') or article_data.get('link'):
                    articles.append(article_data)
            
            logger.info(f"Extracción básica completada. Elementos potenciales encontrados: {len(articles)}")
            
        except Exception as e:
            logger.warning(f"Error durante la extracción básica: {e}")
        
        return articles
    
    def run(self, url: str = None, extract_content: bool = False):
        """
        Ejecuta el scraper
        
        Args:
            url: URL específica a scrapear. Si es None, usa la página principal
            extract_content: Si True, extrae el contenido completo del artículo
        """
        target_url = url if url else self.base_url
        logger.info(f"Iniciando scraper para: {target_url}")
        
        try:
            if extract_content:
                # Modo extracción de contenido de artículo
                article_data = self.scrape_article_content(target_url)
                logger.info(f"Contenido extraído del artículo:")
                logger.info(f"Título: {article_data['title']}")
                logger.info(f"Autor: {article_data['author']}")
                logger.info(f"Fecha: {article_data['date']}")
                logger.info(f"Categoría: {article_data['category']}")
                logger.info(f"Contenido: {len(article_data['content'])} caracteres")
                logger.info(f"Tags: {', '.join(article_data['tags'])}")
                
                return article_data
            else:
                # Modo extracción de listado de artículos
                articles = self.scrape_articles(url)
                logger.info(f"Se encontraron {len(articles)} artículos")
                
                # Mostrar algunos resultados para verificar
                for i, article in enumerate(articles[:5]):  # Mostrar máximo 5
                    logger.info(f"Artículo {i+1}: {article}")
                
                return articles
                
        except Exception as e:
            logger.error(f"Error durante el scraping: {e}")
            raise


if __name__ == "__main__":
    scraper = DittoScraper()
    # Ejemplo de uso para extraer contenido de artículo
    article_url = "https://theobjective.com/economia/energia/2025-07-13/cnmc-directiva-apagon/"
    scraper.run(article_url, extract_content=True) 