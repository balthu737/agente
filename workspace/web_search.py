# web_search.py

import requests
import json
from typing import Any

# Tool Definition

tool_definition = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Realiza una búsqueda en la web usando la API de DuckDuckGo y devuelve los resultados más relevantes.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Texto a buscar en la web."
                }
            },
            "required": ["query"]
        }
    }
}

# Function implementation

def run(query: str) -> str:
    """Realiza una búsqueda web y devuelve los títulos y enlaces de los primeros resultados."""
    print(" ⚙️ Herramienta llamada: web_search")
    try:
        if not query:
            return "Error en web_search: no se proporcionó ninguna consulta."

        # Usamos DuckDuckGo Instant Answer API (sin API Key)
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        results = []
        if "RelatedTopics" in data:
            for topic in data["RelatedTopics"]:
                if "Text" in topic and "FirstURL" in topic:
                    results.append({"title": topic["Text"], "url": topic["FirstURL"]})
                # En la API hay subestructuras anidadas
                if "Topics" in topic:
                    for sub in topic["Topics"]:
                        if "Text" in sub and "FirstURL" in sub:
                            results.append({"title": sub["Text"], "url": sub["FirstURL"]})
        if not results:
            return "No se encontraron resultados para la consulta."

        # Limitar a los primeros 5 resultados
        top_results = results[:5]
        return str(top_results)

    except Exception as e:
        err = f"Error en web_search: {str(e)}"
        print(err)
        return err
