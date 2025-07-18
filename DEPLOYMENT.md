# 🚀 Deployment Guide - Ditto Scraper

## 📋 Pre-requisitos

✅ Repositorio subido a GitHub  
✅ Archivos `requirements.txt` y `app.py` en la raíz  
✅ Configuración de Streamlit en `.streamlit/config.toml`  

## 🌐 Deploy en Streamlit Cloud

### Paso 1: Acceder a Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub

### Paso 2: Crear nueva aplicación
1. Haz clic en **"New app"**
2. Selecciona **"From existing repo"**

### Paso 3: Configurar la aplicación
```
Repository: tu-usuario/ditto-scrapper
Branch: main
Main file path: app.py
App URL (opcional): ditto-scraper-tu-usuario
```

### Paso 4: Configuraciones avanzadas (opcional)
```bash
# Variables de entorno (si es necesario)
STREAMLIT_THEME_PRIMARY_COLOR=#2e86ab
STREAMLIT_SERVER_HEADLESS=true
```

### Paso 5: Deploy
1. Haz clic en **"Deploy!"**
2. Espera 2-3 minutos para el primer deployment
3. Tu app estará disponible en: `https://tu-app.streamlit.app`

## 🔧 Configuración automática incluida

- ✅ **requirements.txt**: Dependencias específicas para Streamlit Cloud
- ✅ **.streamlit/config.toml**: Tema personalizado
- ✅ **app.py**: Aplicación principal optimizada para producción

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
- Verifica que todas las dependencias estén en `requirements.txt`
- Asegúrate de que las versiones sean compatibles

### Error: File not found
- Confirma que `app.py` esté en la raíz del repositorio
- Verifica que el path en la configuración sea correcto

### App muy lenta
- Las apps gratuitas en Streamlit Cloud pueden tener limitaciones
- Considera optimizar las requests al scraper

## 📊 Monitoreo

- **Logs**: Disponibles en el dashboard de Streamlit Cloud
- **Métricas**: Uso y performance en tiempo real
- **Updates**: Push a GitHub despliega automáticamente

## 🔄 Actualizaciones

1. Haz cambios en tu código local
2. Commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Descripción del cambio"
   git push origin main
   ```
3. Streamlit Cloud redespliega automáticamente

## 🌟 URLs de ejemplo para testing

Puedes probar la app con estas URLs:
- `https://theobjective.com/economia/energia/2025-07-13/cnmc-directiva-apagon/`
- `https://theobjective.com/lifestyle/viajes/2025-07-17/ni-zahara-ni-bolonia-playa-bonita-cadiz-revista-viajar/`
- `https://theobjective.com/economia/`

## 📝 Notas importantes

- ⚠️ **Respeta los términos de servicio** de theobjetive.com
- 🕐 **Rate limiting**: Evita hacer muchas requests simultáneas
- 🔒 **Seguridad**: Solo funciona con URLs de theobjetive.com 