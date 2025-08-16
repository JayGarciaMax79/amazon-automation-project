"""
Integración con APIs de IA completamente gratuitas
Alternativa a OpenAI para generar artículos sin costo
"""

import requests
import json
import os
import time
import random
from typing import Dict, Any, Optional
from datetime import datetime

class FreeAIArticleGenerator:
    """
    Generador de artículos usando APIs de IA gratuitas
    """
    
    def __init__(self):
        # APIs gratuitas disponibles
        self.apis = {
            'huggingface': {
                'url': 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-large',
                'headers': {'Authorization': f'Bearer {os.getenv("HUGGINGFACE_API_KEY", "")}'},
                'free': True
            },
            'gemini': {
                'url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
                'headers': {'Content-Type': 'application/json'},
                'free': True,
                'key': os.getenv('GOOGLE_GEMINI_API_KEY', '')
            },
            'ollama': {
                'url': 'http://localhost:11434/api/generate',
                'headers': {'Content-Type': 'application/json'},
                'free': True,
                'local': True
            }
        }
        
        # Templates de artículos optimizados para IA gratuita
        self.templates = {
            'electronics': self._get_electronics_template(),
            'home': self._get_home_template(),
            'fashion': self._get_fashion_template(),
            'books': self._get_books_template(),
            'default': self._get_default_template()
        }
    
    async def generate_article(self, product_data: Dict[str, Any], affiliate_link: str) -> Dict[str, Any]:
        """
        Genera un artículo usando APIs gratuitas
        """
        try:
            # Determinar la mejor API disponible
            api_name = self._select_best_api()
            
            if not api_name:
                return self._generate_fallback_article(product_data, affiliate_link)
            
            # Generar artículo con la API seleccionada
            article_content = await self._generate_with_api(api_name, product_data, affiliate_link)
            
            # Optimizar para SEO
            seo_optimized = self._optimize_seo(article_content, product_data)
            
            return {
                'success': True,
                'article': seo_optimized,
                'ai_provider': api_name,
                'cost': 0.0,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback_used': True,
                'article': self._generate_fallback_article(product_data, affiliate_link)
            }
    
    def _select_best_api(self) -> Optional[str]:
        """Selecciona la mejor API disponible"""
        
        # Prioridad: Gemini > Hugging Face > Ollama
        priority_order = ['gemini', 'huggingface', 'ollama']
        
        for api_name in priority_order:
            if self._is_api_available(api_name):
                return api_name
        
        return None
    
    def _is_api_available(self, api_name: str) -> bool:
        """Verifica si una API está disponible"""
        api_config = self.apis.get(api_name)
        
        if not api_config:
            return False
        
        # Verificar API key para APIs que la requieren
        if api_name == 'gemini':
            return bool(api_config.get('key'))
        elif api_name == 'huggingface':
            return bool(os.getenv('HUGGINGFACE_API_KEY'))
        elif api_name == 'ollama':
            # Verificar si Ollama está corriendo localmente
            try:
                response = requests.get('http://localhost:11434/api/tags', timeout=5)
                return response.status_code == 200
            except:
                return False
        
        return True
    
    async def _generate_with_api(self, api_name: str, product_data: Dict[str, Any], affiliate_link: str) -> str:
        """Genera contenido con la API especificada"""
        
        if api_name == 'gemini':
            return await self._generate_with_gemini(product_data, affiliate_link)
        elif api_name == 'huggingface':
            return await self._generate_with_huggingface(product_data, affiliate_link)
        elif api_name == 'ollama':
            return await self._generate_with_ollama(product_data, affiliate_link)
        else:
            raise Exception(f"API no soportada: {api_name}")
    
    async def _generate_with_gemini(self, product_data: Dict[str, Any], affiliate_link: str) -> str:
        """Genera artículo con Google Gemini (Gratis)"""
        
        prompt = self._create_article_prompt(product_data, affiliate_link)
        
        api_config = self.apis['gemini']
        url = f"{api_config['url']}?key={api_config['key']}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        
        response = requests.post(url, headers=api_config['headers'], json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            return content
        else:
            raise Exception(f"Error Gemini API: {response.status_code}")
    
    async def _generate_with_huggingface(self, product_data: Dict[str, Any], affiliate_link: str) -> str:
        """Genera artículo con Hugging Face (Gratis)"""
        
        prompt = self._create_article_prompt(product_data, affiliate_link, max_length=500)
        
        api_config = self.apis['huggingface']
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        response = requests.post(api_config['url'], headers=api_config['headers'], json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', '')
            return str(result)
        else:
            raise Exception(f"Error Hugging Face API: {response.status_code}")
    
    async def _generate_with_ollama(self, product_data: Dict[str, Any], affiliate_link: str) -> str:
        """Genera artículo con Ollama local (Gratis)"""
        
        prompt = self._create_article_prompt(product_data, affiliate_link)
        
        api_config = self.apis['ollama']
        
        payload = {
            "model": "llama2",  # o "mistral", "codellama"
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(api_config['url'], headers=api_config['headers'], json=payload, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', '')
        else:
            raise Exception(f"Error Ollama API: {response.status_code}")
    
    def _create_article_prompt(self, product_data: Dict[str, Any], affiliate_link: str, max_length: int = 2000) -> str:
        """Crea el prompt optimizado para APIs gratuitas"""
        
        title = product_data.get('title', 'Producto de Amazon')
        price = product_data.get('current_price', 'No disponible')
        rating = product_data.get('rating', 'Sin calificación')
        description = product_data.get('description', '')[:300]  # Limitar descripción
        
        prompt = f"""
Escribe un artículo de blog profesional sobre este producto de Amazon:

PRODUCTO: {title}
PRECIO: {price}
CALIFICACIÓN: {rating}
DESCRIPCIÓN: {description}

INSTRUCCIONES:
1. Título atractivo y optimizado para SEO
2. Introducción enganchante (100 palabras)
3. Características principales (150 palabras)
4. Pros y contras (100 palabras)
5. Conclusión con llamada a la acción (100 palabras)
6. Incluir enlace de afiliado: {affiliate_link}
7. Tono profesional pero accesible
8. Optimizado para conversión

FORMATO: HTML con etiquetas h1, h2, h3, p, ul, li
LONGITUD: {max_length} palabras máximo
IDIOMA: Español

ARTÍCULO:
"""
        
        return prompt
    
    def _optimize_seo(self, content: str, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimiza el contenido para SEO"""
        
        title = product_data.get('title', 'Producto Amazon')
        
        # Extraer título del contenido generado
        lines = content.split('\n')
        article_title = title[:60]  # Fallback
        
        for line in lines:
            if line.strip().startswith('<h1>') or line.strip().startswith('#'):
                article_title = line.replace('<h1>', '').replace('</h1>', '').replace('#', '').strip()[:60]
                break
        
        # Generar meta descripción
        meta_description = f"Análisis completo de {title}. Características, precio y opiniones. Encuentra el mejor precio aquí."[:160]
        
        # Keywords básicas
        keywords = ['amazon', 'producto', 'análisis', 'precio', 'comprar', 'review']
        
        return {
            'title': article_title,
            'content': content,
            'meta_description': meta_description,
            'keywords': keywords,
            'word_count': len(content.split()),
            'seo_score': 7  # Puntuación base
        }
    
    def _generate_fallback_article(self, product_data: Dict[str, Any], affiliate_link: str) -> Dict[str, Any]:
        """Genera artículo básico como fallback"""
        
        title = product_data.get('title', 'Producto de Amazon')
        price = product_data.get('current_price', 'Consultar precio')
        
        content = f"""
        <h1>{title}: Análisis y Opinión Completa</h1>
        
        <p>En este artículo analizamos en detalle el <strong>{title}</strong>, 
        un producto que ha captado nuestra atención en Amazon por sus características únicas y excelente relación calidad-precio.</p>
        
        <h2>Características Principales</h2>
        <p>Este producto destaca por su calidad de construcción y funcionalidad. 
        Con un precio de <strong>{price}</strong>, ofrece una excelente propuesta de valor para los usuarios que buscan calidad y rendimiento.</p>
        
        <h2>¿Por Qué Elegir Este Producto?</h2>
        <ul>
            <li>Excelente relación calidad-precio</li>
            <li>Materiales de alta calidad</li>
            <li>Diseño funcional y atractivo</li>
            <li>Buenas valoraciones de usuarios</li>
        </ul>
        
        <h2>Nuestra Opinión</h2>
        <p>Después de analizar este producto, consideramos que es una excelente opción 
        para quienes buscan calidad y buen precio. Sus características lo convierten en una compra inteligente.</p>
        
        <h2>¿Dónde Comprarlo al Mejor Precio?</h2>
        <p>Si estás interesado en este producto, puedes encontrarlo al mejor precio 
        <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haciendo clic aquí</a>.</p>
        
        <p><strong>¡No esperes más!</strong> 
        <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">Consigue este producto ahora con el mejor precio disponible</a>.</p>
        """
        
        return {
            'title': f"{title}: Análisis Completo",
            'content': content,
            'meta_description': f"Análisis detallado de {title}. Características, precio y opiniones.",
            'keywords': ['amazon', 'producto', 'análisis', 'precio'],
            'word_count': len(content.split()),
            'seo_score': 6
        }
    
    def _get_electronics_template(self) -> str:
        return "Template optimizado para electrónicos con especificaciones técnicas"
    
    def _get_home_template(self) -> str:
        return "Template optimizado para productos del hogar con enfoque en funcionalidad"
    
    def _get_fashion_template(self) -> str:
        return "Template optimizado para moda con enfoque en estilo y tendencias"
    
    def _get_books_template(self) -> str:
        return "Template optimizado para libros con reseñas y análisis de contenido"
    
    def _get_default_template(self) -> str:
        return "Template general optimizado para cualquier tipo de producto"

# Función principal para uso en Vercel
async def generate_free_article(product_url: str, affiliate_link: str, product_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Función principal para generar artículos gratis
    """
    generator = FreeAIArticleGenerator()
    
    # Si no hay datos del producto, usar datos básicos
    if not product_data:
        product_data = {
            'title': 'Producto de Amazon',
            'current_price': 'Consultar precio',
            'description': 'Producto disponible en Amazon',
            'rating': 'Sin calificación'
        }
    
    return await generator.generate_article(product_data, affiliate_link)

# Para testing local
if __name__ == "__main__":
    import asyncio
    
    async def test():
        test_data = {
            'title': 'Apple iPhone 13 (128GB, Blue)',
            'current_price': '$699.00',
            'description': 'El iPhone 13 cuenta con el chip A15 Bionic, sistema de cámara dual avanzado...',
            'rating': '4.5 de 5'
        }
        
        result = await generate_free_article(
            'https://www.amazon.com/dp/B08N5WRWNW',
            'https://amzn.to/3xyz123',
            test_data
        )
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(test())

