import os
import json
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# Importar el SDK de Google Gemini
import google.generativeai as genai

# Configurar la clave de API de Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI() # <-- ¡Mueve esta línea aquí!

@app.post("/api/generate-article-free")
async def generate_article_free(request: Request):
    try:
        request_data = await request.json()

        product_url = request_data.get("product_url")
        affiliate_link = request_data.get("affiliate_link")

        if not product_url or not affiliate_link:
            raise HTTPException(status_code=400, detail="product_url and affiliate_link are required")

        # ... el resto de tu código sigue igual ...

        # ... el resto de tu código sigue igual ...


        # Paso 1: Scrapear la información del producto de Amazon
        scrape_api_url = os.environ.get("SCRAPE_API_URL")
        if not scrape_api_url:
            raise HTTPException(status_code=500, detail="SCRAPE_API_URL environment variable not set.")

        try:
            scrape_response = requests.post(scrape_api_url, json={"product_url": product_url})
            scrape_response.raise_for_status()  # Lanza un error para códigos de estado HTTP erróneos
            product_info = scrape_response.json()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error al scrapear Amazon: {e}")

        # Paso 2: Generar el artículo con Gemini
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
        Basado en la siguiente información del producto de Amazon, genera un artículo de blog detallado y atractivo. 
        El artículo debe ser informativo, persuasivo y optimizado para SEO. 
        Incluye el enlace de afiliado proporcionado de forma natural en el texto.

        Información del producto:
        Título: {product_info.get("title", "N/A")}
        Precio: {product_info.get("price", "N/A")}
        Valoración: {product_info.get("rating", "N/A")}
        Descripción: {product_info.get("description", "N/A")}
        Características: {", ".join(product_info.get("features", []))}

        Enlace de afiliado: {affiliate_link}

        El artículo debe tener una introducción, varios párrafos de contenido (destacando beneficios, características clave y casos de uso), y una conclusión con una llamada a acción clara para comprar a través del enlace de afiliado.
        """
        
        gemini_response = model.generate_content(prompt)
        article_content = gemini_response.text

        # Paso 3: Publicar el artículo en WordPress
        wordpress_api_url = os.environ.get("WORDPRESS_API_URL")
        wordpress_username = os.environ.get("WORDPRESS_USERNAME")
        wordpress_password = os.environ.get("WORDPRESS_PASSWORD")

        if not all([wordpress_api_url, wordpress_username, wordpress_password]):
            raise HTTPException(status_code=500, detail="WordPress API credentials not fully set.")

        auth = requests.auth.HTTPBasicAuth(wordpress_username, wordpress_password)
        
        # Asumiendo que el título del artículo es la primera línea o se puede extraer de alguna manera
        # Por simplicidad, tomaremos las primeras 50 caracteres como título
        article_title = article_content.split("\n")[0][:50].strip()
        if not article_title:
            article_title = f"Artículo sobre {product_info.get("title", "Producto Amazon")}"

        wordpress_post_data = {
            "title": article_title,
            "content": article_content,
            "status": "publish"
        }

        try:
            wordpress_response = requests.post(f"{wordpress_api_url}/posts", auth=auth, json=wordpress_post_data)
            wordpress_response.raise_for_status()
            
            published_post_info = wordpress_response.json()
            published_url = published_post_info.get("link")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Error al publicar en WordPress: {e}")

        return JSONResponse(content={
            "status": "success",
            "article_title": article_title,
            "article_url": published_url
        })

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"status": "error", "message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Error inesperado: {e}"})


