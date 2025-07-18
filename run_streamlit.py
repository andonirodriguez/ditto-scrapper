#!/usr/bin/env python3
"""
Script para ejecutar la aplicación Streamlit localmente
"""

import subprocess
import sys

def main():
    """Ejecuta la aplicación Streamlit"""
    try:
        print("🚀 Iniciando Ditto Scraper en Streamlit...")
        print("📱 La aplicación se abrirá en tu navegador automáticamente")
        print("🔗 URL: http://localhost:8501")
        print("\n" + "="*50)
        
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Aplicación cerrada por el usuario!")
    except Exception as e:
        print(f"\n❌ Error ejecutando la aplicación: {e}")
        print("💡 Asegúrate de que Streamlit esté instalado: pip install streamlit")

if __name__ == "__main__":
    main() 