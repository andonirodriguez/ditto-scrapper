# Ditto Scrapper

POC para scrapear contenido de theobjetive.com con interfaz web interactiva

## 🌟 Características

- ✅ **Extracción completa de artículos**: títulos, autores, fechas, contenido
- ✅ **Validación de dominio**: solo permite URLs de theobjetive.com
- ✅ **Interfaz web moderna**: aplicación Streamlit responsive y atractiva
- ✅ **Múltiples modos**: línea de comandos y interfaz gráfica
- ✅ **Estadísticas de sesión**: seguimiento de extracciones exitosas/fallidas
- ✅ **Extracción inteligente**: detecta automáticamente elementos del artículo

## 📋 Requisitos

- Python 3.10+
- Poetry (para gestión de dependencias)

## 🚀 Instalación Rápida

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd ditto-scrapper

# Instalar dependencias
poetry install

# Ejecutar la aplicación web
poetry run streamlit run streamlit_app.py
```

## 💻 Modos de Uso

### 1. 🌐 Aplicación Web (Streamlit) - **¡RECOMENDADO!**

La forma más fácil y visual de usar el scraper:

```bash
# Opción 1: Usando Poetry
poetry run streamlit run streamlit_app.py

# Opción 2: Usando el script helper
poetry run python run_streamlit.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

**Características de la interfaz web:**
- 📱 Interfaz responsive y moderna
- 🎯 URLs de ejemplo pre-configuradas
- 📊 Métricas en tiempo real
- 🔧 Modo debug opcional
- 📄 Vista previa del contenido extraído

### 2. 📟 Línea de Comandos

#### Extracción de artículo específico:
```bash
# Usando el script simple
poetry run python extract_article.py "https://theobjective.com/tu-articulo/"

# Usando el script principal
poetry run python main.py
```

#### Uso programático:
```python
from src.scraper import DittoScraper

scraper = DittoScraper()

# Extraer contenido de un artículo
article_data = scraper.scrape_article_content("https://theobjective.com/economia/...")

print(f"Título: {article_data['title']}")
print(f"Autor: {article_data['author']}")
print(f"Contenido: {article_data['content']}")
```

## 🏗️ Estructura del Proyecto

```
ditto-scrapper/
├── .streamlit/
│   └── config.toml           # Configuración de Streamlit
├── src/
│   ├── __init__.py
│   └── scraper.py           # Lógica principal del scraper
├── streamlit_app.py         # 🌟 Aplicación Streamlit (PRINCIPAL)
├── main.py                  # Ejemplos de uso en terminal
├── extract_article.py       # Script simple de extracción
├── run_streamlit.py         # Helper para ejecutar Streamlit
├── requirements.txt         # Dependencias para Streamlit Cloud
├── pyproject.toml          # Configuración del proyecto
├── .gitignore              # Archivos a ignorar
└── README.md               # Este archivo
```

## 🌐 Deploy en Streamlit Cloud

### Preparación para Deploy:

1. **Sube tu código a GitHub**
2. **Ve a [share.streamlit.io](https://share.streamlit.io)**
3. **Conecta tu repositorio de GitHub**
4. **Configura el deploy:**
   - **Repository**: `tu-usuario/ditto-scrapper`
   - **Branch**: `main`
   - **Main file path**: `app.py`

### Variables de entorno (opcional):
Si necesitas configuraciones específicas, puedes agregar en Streamlit Cloud:
```
STREAMLIT_THEME_PRIMARY_COLOR=#2e86ab
```

## 🛠️ Desarrollo

### Agregar nuevas dependencias:
```bash
# Dependencia principal
poetry add nombre-paquete

# Dependencia de desarrollo
poetry add --group dev nombre-paquete
```

### Ejecutar tests (cuando los agregues):
```bash
poetry run pytest
```

### Activar entorno virtual:
```bash
poetry shell
```

## 📊 API del Scraper

### `DittoScraper.scrape_article_content(url)`

Extrae el contenido completo de un artículo.

**Parámetros:**
- `url` (str): URL del artículo de theobjetive.com

**Retorna:**
```python
{
    'url': 'https://theobjective.com/...',
    'title': 'Título del artículo',
    'subtitle': 'Subtítulo si existe',
    'author': 'Nombre del autor',
    'date': 'Fecha de publicación',
    'content': 'Contenido completo del artículo',
    'tags': ['tag1', 'tag2', ...],
    'category': 'categoría'
}
```

### Validación automática:
- ✅ Solo acepta URLs de `theobjective.com`
- ✅ Maneja URLs relativas y absolutas
- ✅ Limpia y normaliza el texto extraído
- ✅ Filtra contenido irrelevante

## 🎯 URLs de Ejemplo

Para probar la aplicación, puedes usar estas URLs:

1. **Artículo de Economía**: `https://theobjective.com/economia/energia/2025-07-13/cnmc-directiva-apagon/`
2. **Sección Economía**: `https://theobjective.com/economia/`
3. **Página Principal**: `https://theobjective.com/`

## ⚠️ Consideraciones Éticas

- 🤝 **Respeta el robots.txt** del sitio web
- ⏱️ **Implementa delays** entre requests para no sobrecargar el servidor
- 📜 **Respeta los términos de servicio** de theobjetive.com
- 🎯 **Uso responsable**: solo para propósitos educativos y de investigación

## 🐛 Solución de Problemas

### Error: "URL no permitida"
- ✅ Verifica que la URL pertenezca a theobjetive.com
- ✅ Incluye `https://` al inicio de la URL

### Error de conexión:
- 🌐 Verifica tu conexión a internet
- 🔄 La página podría estar temporalmente no disponible

### Contenido no extraído:
- 🔍 La estructura HTML de la página podría haber cambiado
- 🛠️ Activa el modo debug en Streamlit para más información

## 🔄 Futuras Mejoras

- [ ] Soporte para más sitios web de noticias
- [ ] Exportar datos a CSV/JSON
- [ ] Sistema de caché para evitar scraping repetido
- [ ] Análisis de sentimientos del contenido
- [ ] API REST para integración con otros sistemas

## 📝 Licencia

MIT

---

<div align="center">

**🚀 ¡Desarrollado con ❤️ para extraer contenido de forma inteligente!**

</div> 