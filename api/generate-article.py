import asyncio
import json
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Import Google Generative AI SDK
try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("Please install google-generativeai: pip install google-generativeai")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmazonArticleGenerator:
    """
    Generador de artículos de Amazon usando Google Gemini
    """
    
    def __init__(self):
        """
        Inicializa el generador con la clave API de Gemini
        """
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')  # Use appropriate Gemini model
        
        # Templates de artículos por categoría
        self.article_templates = {
            "electronics": self._get_electronics_template(),
            "home": self._get_home_template(),
            "fashion": self._get_fashion_template(),
            "books": self._get_books_template(),
            "default": self._get_default_template()
        }
        
        # Palabras clave SEO por categoría
        self.seo_keywords = {
            "electronics": ["mejor", "análisis", "review", "comparación", "precio", "características"],
            "home": ["hogar", "casa", "decoración", "funcional", "calidad", "diseño"],
            "fashion": ["moda", "estilo", "tendencia", "outfit", "look", "temporada"],
            "books": ["libro", "lectura", "autor", "reseña", "recomendación", "género"],
            "default": ["producto", "calidad", "precio", "comprar", "mejor", "análisis"]
        }
    
    async def initialize(self):
        """Inicializa el modelo de Gemini"""
        logger.info("Gemini model initialized")
        return True
    
    async def generate_article(self, product_url: str, affiliate_link: str) -> Dict[str, Any]:
        """
        Genera un artículo completo sobre un producto de Amazon usando Gemini
        """
        try:
            logger.info(f"Iniciando generación de artículo para: {product_url}")
            
            # Simular extracción de datos (reemplazar con scraping si necesario)
            product_data = await self._extract_product_data(product_url)
            category = await self._determine_category(product_data)
            article_content = await self._generate_article_content(product_data, affiliate_link, category)
            seo_optimized = await self._optimize_for_seo(article_content, product_data, category)
            metadata = await self._generate_metadata(product_data, category)
            
            result = {
                "success": True,
                "article": {
                    "title": seo_optimized.get("title", ""),
                    "content": seo_optimized.get("content", ""),
                    "meta_description": seo_optimized.get("meta_description", ""),
                    "keywords": seo_optimized.get("keywords", []),
                    "category": category,
                    "word_count": len(seo_optimized.get("content", "").split())
                },
                "product_data": product_data,
                "metadata": metadata,
                "affiliate_link": affiliate_link,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info("Artículo generado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error al generar artículo: {e}")
            return {
                "success": False,
                "error": str(e),
                "product_url": product_url,
                "affiliate_link": affiliate_link
            }
    
    async def _extract_product_data(self, product_url: str) -> Dict[str, Any]:
        """Extrae datos del producto usando Gemini (simulación; añadir scraping si necesario)"""
        extraction_prompt = f"""
        Simula la extracción de datos de un producto de Amazon. 
        URL: {product_url}
        Devuelve un JSON con: title, current_price, description, features (array), rating, review_count, availability, brand, category, images (array), asin.
        Usa valores ficticios si no hay datos reales.
        """
        try:
            response = self.model.generate_content(extraction_prompt)
            product_data = json.loads(response.text)  # Assume Gemini returns JSON
            return product_data
        except Exception as e:
            logger.error(f"Error al extraer datos: {e}")
            return {
                "title": "Producto de Amazon",
                "current_price": "No disponible",
                "description": "Descripción no disponible",
                "features": [],
                "rating": "No disponible",
                "review_count": "0",
                "availability": "No disponible",
                "brand": "No disponible",
                "category": "General",
                "images": [],
                "asin": "No disponible"
            }
    
    async def _determine_category(self, product_data: Dict[str, Any]) -> str:
        """Determina la categoría del producto usando Gemini"""
        category_prompt = f"""
        Determina la categoría principal basada en:
        Título: {product_data.get('title', '')}
        Descripción: {product_data.get('description', '')}
        Categorías: electronics, home, fashion, books, default
        Responde solo con la categoría.
        """
        try:
            response = self.model.generate_content(category_prompt)
            category = response.text.strip().lower()
            return category if category in self.article_templates else "default"
        except Exception as e:
            logger.error(f"Error al determinar categoría: {e}")
            return "default"
    
    async def _generate_article_content(self, product_data: Dict[str, Any], affiliate_link: str, category: str) -> str:
        """Genera contenido del artículo usando Gemini"""
        template = self.article_templates.get(category, self.article_templates["default"])
        content_prompt = f"""
        Crea un artículo HTML de 1500-2000 palabras sobre:
        {json.dumps(product_data, indent=2)}
        Affiliate link: {affiliate_link}
        Template: {template}
        Instrucciones: Tono profesional, 3+ affiliate links, pros/cons, CTA.
        """
        try:
            response = self.model.generate_content(content_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error al generar contenido: {e}")
            return self._generate_fallback_article(product_data, affiliate_link)
    
    async def _optimize_for_seo(self, content: str, product_data: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Optimiza para SEO usando Gemini"""
        keywords = self.seo_keywords.get(category, self.seo_keywords["default"])
        seo_prompt = f"""
        Optimiza este contenido para SEO:
        {content}
        Product: {product_data.get('title', '')}
        Keywords: {', '.join(keywords)}
        Return JSON with title, meta_description, keywords, content, seo_score.
        """
        try:
            response = self.model.generate_content(seo_prompt)
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Error al optimizar SEO: {e}")
            return {
                "title": product_data.get('title', 'Producto Amazon')[:60],
                "meta_description": f"Análisis de {product_data.get('title', 'producto')}"[:160],
                "keywords": keywords[:5],
                "content": content,
                "seo_score": "6"
            }
    
    async def _generate_metadata(self, product_data: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Genera metadatos"""
        return {
            "estimated_read_time": self._calculate_read_time(product_data.get('title', '')),
            "target_audience": self._get_target_audience(category),
            "content_type": "product_review",
            "language": "es",
            "region": "global",
            "update_frequency": "monthly",
            "monetization": "affiliate",
            "quality_score": self._calculate_quality_score(product_data)
        }
    
    # [Keep _get_*_template, _parse_extraction_result, _generate_fallback_article, etc., as they are]

# Vercel handler function
def handler(request):
    """Handle HTTP requests for Vercel serverless function"""
    try:
        data = request.get_json()
        if not data or 'product_url' not in data or 'affiliate_link' not in data:
            return json.dumps({"error": "Missing product_url or affiliate_link"}), 400, {'Content-Type': 'application/json'}

        product_url = data['product_url']
        affiliate_link = data['affiliate_link']

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(generate_amazon_article(product_url, affiliate_link))
        loop.close()

        return json.dumps(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        logger.error(f"Handler error: {e}")
        return json.dumps({"error": str(e), "success": False}), 500, {'Content-Type': 'application/json'}

# For local testing
if __name__ == "__main__":
    async def test():
        test_url = "https://www.amazon.com/dp/B08N5WRWNW"
        test_affiliate = "https://amzn.to/3xyz123"
        result = await generate_amazon_article(test_url, test_affiliate)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(test())
