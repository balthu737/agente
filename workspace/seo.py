# seo.py

import requests
from typing import Any

# Tool Definition

tool_definition = {
    "type": "function",
    "function": {
        "name": "seo",
        "description": "Genera una lista de palabras clave SEO a partir de una palabra clave principal y el idioma solicitado.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "Palabra clave principal para la que se generarán palabras relacionadas."
                },
                "language": {
                    "type": "string",
                    "description": "Código de idioma de la palabra clave, por defecto es "es"."
                }
            },
            "required": ["keyword"]
        }
    }
}

# Function implementation

def run(keyword: str, language: str = "es") -> str:
    """Genera una lista de palabras clave SEO relacionadas con la palabra clave principal."""
    print(" ⚙️ Herramienta llamada: seo")
    try:
        if not keyword:
            return "Error en seo: no se proporcionó la palabra clave."

        url = f"https://api.keywordtool.io/v2/search/google/autocomplete?keyword={keyword}&lang={language}&country=mx&token=YOUR_API_KEY"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # La API de keywordtool devuelve los resultados bajo el campo 'suggestions'
        suggestions = data.get('suggestions', [])
        return str(suggestions)
    except Exception as e:
        err = f"Error en seo: {str(e)}"
        print(err)
        return err
