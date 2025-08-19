import os
import json
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Importar el SDK de Google Gemini
import google.generativeai as genai

# Configurar la clave de API de Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

print("FastAPI app instance created!")

# Función simulada de scraping (integrada)
def scrape_amazon_product(product_url):
    """
    Función simulada de scraping de Amazon.
    En un entorno real, esto haría scraping real del producto.
    """
    return {
        "title": "Producto de Amazon Ejemplo",
        "price": "$29.99",
        "rating": "4.5/5 estrellas",
        "description": "Este es un excelente producto con características innovadoras que mejorará tu experiencia diaria.",
        "features": [
            "Característica 1: Alta calidad",
            "Característica 2: Fácil de usar",
            "Característica 3: Diseño elegante",
            "Característica 4: Precio competitivo"
        ]
    }

@app.post("/api/generate-article-free")
async def generate_article_free(request: Request):
    try:
        # Obtener los datos del request
        data = await request.json()
        product_url = data.get("product_url")
        affiliate_link = data.get("affiliate_link")
        
        if not product_url or not affiliate_link:
            raise HTTPException(status_code=400, detail="product_url y affiliate_link son requeridos")

        # Paso 1: Scrapear la información del producto de Amazon (simulado)
        product_info = scrape_amazon_product(product_url)

        # Paso 2: Generar el artículo con Gemini
        model = genai.GenerativeModel("gemini-1.5-flash")
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

        # Paso 3: Publicar el artículo en WordPress (opcional)
        wordpress_api_url = os.environ.get("WORDPRESS_API_URL")
        wordpress_username = os.environ.get("WORDPRESS_USERNAME")
        wordpress_password = os.environ.get("WORDPRESS_PASSWORD")

        published_url = None
        if all([wordpress_api_url, wordpress_username, wordpress_password]):
            try:
                auth = requests.auth.HTTPBasicAuth(wordpress_username, wordpress_password)
                
                # Extraer título del artículo
                article_title = article_content.split("\n")[0][:50].strip()
                if not article_title:
                    article_title = f'Artículo sobre {product_info.get("title", "Producto Amazon")}'

                wordpress_post_data = {
                    "title": article_title,
                    "content": article_content,
                    "status": "publish"
                }

                wordpress_response = requests.post(f"{wordpress_api_url}/posts", auth=auth, json=wordpress_post_data)
                wordpress_response.raise_for_status()
                
                published_post_info = wordpress_response.json()
                published_url = published_post_info.get("link")
            except requests.exceptions.RequestException as e:
                print(f"Error al publicar en WordPress: {e}")
                # No lanzamos error, solo continuamos sin publicar

        return JSONResponse(content={
            "status": "success",
            "article_title": article_content.split("\n")[0][:50].strip() or "Artículo generado",
            "article_content": article_content,
            "article_url": published_url,
            "product_info": product_info
        })

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"status": "error", "message": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": f"Error inesperado: {str(e)}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


