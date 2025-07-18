#!/usr/bin/env python3
"""
Ejemplo simple para extraer contenido de un artículo de theobjetive.com
"""

from src.scraper import DittoScraper
import sys

def extract_article_content(url: str):
    """
    Extrae y muestra el contenido de un artículo
    
    Args:
        url: URL del artículo de theobjetive.com
    """
    scraper = DittoScraper()
    
    try:
        print(f"🔍 Extrayendo contenido de: {url}")
        print("-" * 60)
        
        # Extraer contenido del artículo
        article_data = scraper.scrape_article_content(url)
        
        # Mostrar resultados
        print(f"📰 TÍTULO: {article_data['title']}")
        print(f"👤 AUTOR: {article_data['author']}")
        print(f"📅 FECHA: {article_data['date']}")
        print(f"📂 CATEGORÍA: {article_data['category']}")
        
        if article_data['subtitle']:
            print(f"📄 SUBTÍTULO: {article_data['subtitle']}")
        
        if article_data['tags']:
            print(f"🏷️ TAGS: {', '.join(article_data['tags'])}")
        
        print(f"\n📝 CONTENIDO ({len(article_data['content'])} caracteres):")
        print("-" * 60)
        print(article_data['content'])
        
        return article_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Función principal"""
    
    # Si se proporciona una URL como argumento, úsala
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # URL de ejemplo por defecto
        url = "https://theobjective.com/economia/energia/2025-07-13/cnmc-directiva-apagon/"
        print(f"ℹ️ Usando URL de ejemplo. Para usar tu propia URL, ejecuta:")
        print(f"   python extract_article.py 'https://theobjective.com/tu-articulo'")
        print()
    
    extract_article_content(url)

if __name__ == "__main__":
    main() 