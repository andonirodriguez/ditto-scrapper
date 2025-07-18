#!/usr/bin/env python3
"""
Aplicación Streamlit para el Ditto Scraper
Extrae contenido de artículos de theobjetive.com
"""

import streamlit as st
from src.scraper import DittoScraper
import time
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Ditto Scraper - theobjetive.com",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar el diseño
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #1f4e79, #2e86ab);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .article-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
        margin: 1rem 0;
    }
    
    .error-message {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación Streamlit"""
    
    # Header principal
    st.markdown('<h1 class="main-header">📰 Ditto Scraper</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Extractor de contenido de theobjetive.com</p>', unsafe_allow_html=True)
    
    # Sidebar con información y configuración
    with st.sidebar:
        st.header("ℹ️ Información del Proyecto")
        st.markdown("""
        **Ditto Scraper** es una POC para extraer contenido de artículos de theobjetive.com de forma automatizada.
        
        ### Características:
        - ✅ Extrae títulos, autores y fechas
        - ✅ Obtiene el contenido completo del artículo
        - ✅ Identifica categorías y tags
        - ✅ Validación de dominio
        - ✅ Interfaz web interactiva
        
        ### Tecnologías:
        - Python 3.10+
        - BeautifulSoup4
        - Requests
        - Streamlit
        """)
        
        st.divider()
        
        st.header("🔧 Configuración")
        show_debug = st.checkbox("Mostrar información de debug", value=False)
        
        st.divider()
        
        st.header("🚀 URLs de Ejemplo")
        example_urls = [
            "https://theobjective.com/economia/energia/2025-07-13/cnmc-directiva-apagon/",
            "https://theobjective.com/economia/",
            "https://theobjective.com/"
        ]
        
        for i, url in enumerate(example_urls, 1):
            if st.button(f"Ejemplo {i}", key=f"example_{i}", use_container_width=True):
                st.session_state.url_input = url
    
    # Contenido principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🔍 Extraer Contenido de Artículo")
        
        # Input para la URL
        url_input = st.text_input(
            "Introduce la URL del artículo de theobjetive.com:",
            value=st.session_state.get('url_input', ''),
            placeholder="https://theobjective.com/...",
            help="Pega aquí la URL completa del artículo que quieres scrapear"
        )
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            extract_button = st.button("🚀 Extraer Contenido", type="primary", use_container_width=True)
        
        with col_btn2:
            clear_button = st.button("🗑️ Limpiar", use_container_width=True)
        
        if clear_button:
            st.session_state.clear()
            st.rerun()
    
    with col2:
        st.header("📊 Estadísticas de Sesión")
        
        # Inicializar estadísticas en session_state si no existen
        if 'stats' not in st.session_state:
            st.session_state.stats = {
                'total_extractions': 0,
                'successful_extractions': 0,
                'failed_extractions': 0
            }
        
        stats = st.session_state.stats
        success_rate = (stats['successful_extractions'] / stats['total_extractions'] * 100) if stats['total_extractions'] > 0 else 0
        
        st.metric("Total Extracciones", stats['total_extractions'])
        st.metric("Exitosas", stats['successful_extractions'], 
                 delta=f"{success_rate:.1f}% tasa de éxito")
        st.metric("Fallidas", stats['failed_extractions'])
    
    # Procesamiento de la extracción
    if extract_button and url_input.strip():
        
        st.session_state.stats['total_extractions'] += 1
        
        with st.spinner('🔄 Extrayendo contenido del artículo...'):
            try:
                # Crear instancia del scraper
                scraper = DittoScraper()
                
                # Extraer contenido
                start_time = time.time()
                article_data = scraper.scrape_article_content(url_input.strip())
                end_time = time.time()
                
                # Verificar si se extrajo contenido útil
                if article_data['title'] or article_data['content']:
                    st.session_state.stats['successful_extractions'] += 1
                    
                    # Mensaje de éxito
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ <strong>¡Contenido extraído exitosamente!</strong><br>
                        Tiempo de procesamiento: {end_time - start_time:.2f} segundos
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar información del artículo
                    st.header("📋 Información del Artículo")
                    
                    # Métricas principales
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📝 Caracteres", len(article_data['content']))
                    
                    with col2:
                        word_count = len(article_data['content'].split()) if article_data['content'] else 0
                        st.metric("💬 Palabras", word_count)
                    
                    with col3:
                        st.metric("🏷️ Tags", len(article_data['tags']))
                    
                    with col4:
                        reading_time = max(1, word_count // 200)  # ~200 palabras por minuto
                        st.metric("⏱️ Lectura", f"{reading_time} min")
                    
                    # Información detallada
                    st.subheader("📄 Detalles del Artículo")
                    
                    # Crear dos columnas para la información
                    info_col1, info_col2 = st.columns(2)
                    
                    with info_col1:
                        st.markdown("**🔗 URL:**")
                        st.code(article_data['url'])
                        
                        st.markdown("**📰 Título:**")
                        st.markdown(f"*{article_data['title']}*" if article_data['title'] else "*No encontrado*")
                        
                        st.markdown("**👤 Autor:**")
                        st.markdown(article_data['author'] if article_data['author'] else "*No encontrado*")
                    
                    with info_col2:
                        st.markdown("**📅 Fecha:**")
                        st.markdown(article_data['date'] if article_data['date'] else "*No encontrada*")
                        
                        st.markdown("**📂 Categoría:**")
                        st.markdown(article_data['category'] if article_data['category'] else "*No encontrada*")
                        
                        if article_data['tags']:
                            st.markdown("**🏷️ Tags:**")
                            tags_text = ", ".join(article_data['tags'])
                            st.markdown(f"*{tags_text}*")
                    
                    # Subtítulo si existe
                    if article_data['subtitle']:
                        st.subheader("📑 Subtítulo")
                        st.markdown(f"*{article_data['subtitle']}*")
                    
                    # Contenido del artículo
                    if article_data['content']:
                        st.subheader("📖 Contenido del Artículo")
                        
                        # Opción para mostrar contenido completo o resumen
                        show_full_content = st.checkbox("Mostrar contenido completo", value=True)
                        
                        if show_full_content:
                            st.markdown(article_data['content'])
                        else:
                            # Mostrar solo los primeros 500 caracteres
                            preview = article_data['content'][:500] + "..." if len(article_data['content']) > 500 else article_data['content']
                            st.markdown(preview)
                            st.info("💡 Marca la casilla arriba para ver el contenido completo")
                    
                    # Información de debug si está habilitada
                    if show_debug:
                        st.subheader("🔧 Información de Debug")
                        st.json(article_data)
                
                else:
                    st.session_state.stats['failed_extractions'] += 1
                    st.error("⚠️ No se pudo extraer contenido útil del artículo. Verifica que la URL sea correcta y que contenga un artículo.")
                
            except ValueError as e:
                st.session_state.stats['failed_extractions'] += 1
                st.markdown(f"""
                <div class="error-message">
                    ❌ <strong>Error de validación:</strong><br>
                    {str(e)}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.session_state.stats['failed_extractions'] += 1
                st.error(f"❌ Error inesperado: {str(e)}")
                
                if show_debug:
                    st.exception(e)
    
    elif extract_button and not url_input.strip():
        st.warning("⚠️ Por favor, introduce una URL antes de extraer el contenido.")
    
    # Footer
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            <p>🚀 <strong>Ditto Scraper</strong> - POC desarrollado para extraer contenido de theobjetive.com</p>
            <p>Creado con ❤️ usando Python, BeautifulSoup y Streamlit</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 