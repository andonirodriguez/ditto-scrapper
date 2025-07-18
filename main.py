#!/usr/bin/env python3
"""
Punto de entrada principal para el Ditto Scraper
"""

from src.scraper import DittoScraper

def main():
    """Función principal"""
    scraper = DittoScraper()
    
    # Ejemplo 1: Extraer contenido de un artículo específico
    print("=== Extrayendo contenido de artículo específico ===")
    try:
        # URL de ejemplo - puedes cambiarla por cualquier artículo de theobjective.com
        article_url = "https://theobjective.com/economia/energia/2025-07-13/cnmc-directiva-apagon/"
        article_data = scraper.run(article_url, extract_content=True)
        
        # Mostrar resumen del contenido extraído
        print(f"\n📰 ARTÍCULO EXTRAÍDO:")
        print(f"🔗 URL: {article_data['url']}")
        print(f"📝 Título: {article_data['title']}")
        print(f"👤 Autor: {article_data['author']}")
        print(f"📅 Fecha: {article_data['date']}")
        print(f"📂 Categoría: {article_data['category']}")
        print(f"📊 Longitud del contenido: {len(article_data['content'])} caracteres")
        print(f"🏷️ Tags: {', '.join(article_data['tags']) if article_data['tags'] else 'No encontrados'}")
        
        # Mostrar primeros 300 caracteres del contenido
        if article_data['content']:
            print(f"\n📄 Contenido (primeros 300 caracteres):")
            print(f"{article_data['content'][:300]}...")
        
    except Exception as e:
        print(f"Error extrayendo artículo: {e}")
    
    print("\n" + "="*60)
    
    # Ejemplo 2: Listar artículos de una sección (modo anterior)
    print("=== Listando artículos de una sección ===")
    try:
        section_url = "https://theobjective.com/economia/"
        articles = scraper.run(section_url, extract_content=False)
        
        print(f"\n📋 ARTÍCULOS ENCONTRADOS: {len(articles)}")
        for i, article in enumerate(articles[:3]):  # Mostrar solo los primeros 3
            print(f"{i+1}. {article.get('title', 'Sin título')} - {article.get('link', 'Sin enlace')}")
        
    except Exception as e:
        print(f"Error listando artículos: {e}")
    
    print("\n" + "="*60)
    
    # Ejemplo 3: Validación de dominio (debería fallar)
    print("=== Prueba de validación de dominio ===")
    try:
        invalid_url = "https://elpais.com/economia/2024/01/01/ejemplo/"
        scraper.run(invalid_url, extract_content=True)
    except Exception as e:
        print(f"✅ Validación correcta - Error esperado: {e}")

if __name__ == "__main__":
    main() 