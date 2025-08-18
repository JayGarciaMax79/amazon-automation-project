import json
import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional

# Simulación de handler para Vercel
def handler(request):
    """Handler principal para Vercel"""
    try:
        # Obtener datos de la petición
        if request.method == 'POST':
            data = request.json  # Vercel pasa el body como JSON
            if not data or not _validate_request(data):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'success': False, 'error': 'product_url y affiliate_link son requeridos'}),
                    'headers': {'Content-Type': 'application/json'}
                }

            # Generar artículo
            result = _generate_article_sync(data)
            return {
                'statusCode': 200,
                'body': json.dumps(result, ensure_ascii=False, indent=2),
                'headers': {'Content-Type': 'application/json'}
            }
        elif request.method == 'GET':
            info = {
                "service": "Free AI Article Generator",
                "description": "Generación de artículos usando APIs de IA completamente gratuitas",
                "supported_apis": ["Google Gemini (15 requests/min gratis)", "Hugging Face (Gratis con límites)", "Ollama Local (Completamente gratis)", "Fallback Template (Siempre disponible)"],
                "cost": "$0.00",
                "example_request": {
                    "product_url": "https://www.amazon.com/dp/B08N5WRWNW",
                    "affiliate_link": "https://amzn.to/3xyz123",
                    "category": "electronics"
                }
            }
            return {
                'statusCode': 200,
                'body': json.dumps(info, ensure_ascii=False, indent=2),
                'headers': {'Content-Type': 'application/json'}
            }
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'success': False, 'error': 'Método no permitido'}),
                'headers': {'Content-Type': 'application/json'}
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'success': False, 'error': f'Error interno: {str(e)}'}),
            'headers': {'Content-Type': 'application/json'}
        }

# Resto de las funciones (copiadas y adaptadas del código original)
def _validate_request(data):
    required_fields = ['product_url', 'affiliate_link']
    return all(field in data and data[field] for field in required_fields)

def _generate_article_sync(data):
    try:
        product_url = data['product_url']
        affiliate_link = data['affiliate_link']
        category = data.get('category', 'general')
        
        product_data = _extract_basic_product_data(product_url)
        article = _try_free_apis(product_data, affiliate_link, category)
        
        if not article:
            article = _generate_template_article(product_data, affiliate_link, category)
        
        return {
            'success': True,
            'article': article,
            'cost': 0.0,
            'provider': article.get('provider', 'template'),
            'generated_at': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'article': _generate_emergency_fallback(data['product_url'], data['affiliate_link'])
        }

# Copia las funciones restantes (_extract_basic_product_data, _try_free_apis, _generate_with_gemini, etc.)
# desde tu código original aquí, asegurándote de que usen requests y manejen errores adecuadamente.

def _extract_basic_product_data(url):
    try:
        import re
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        asin = asin_match.group(1) if asin_match else 'UNKNOWN'
        return {
            'asin': asin,
            'title': f'Producto Amazon {asin}',
            'url': url,
            'current_price': 'Consultar precio en Amazon',
            'rating': 'Ver calificaciones',
            'description': 'Producto disponible en Amazon con excelentes características.'
        }
    except Exception:
        return {
            'title': 'Producto de Amazon',
            'current_price': 'Precio disponible en Amazon',
            'rating': 'Ver reseñas',
            'description': 'Excelente producto disponible en Amazon.'
        }

def _try_free_apis(product_data, affiliate_link, category):
    gemini_key = os.getenv('GOOGLE_GEMINI_API_KEY')
    hf_key = os.getenv('HUGGINGFACE_API_KEY')
    
    if gemini_key:
        try:
            article = _generate_with_gemini(product_data, affiliate_link, gemini_key)
            if article:
                article['provider'] = 'google_gemini'
                return article
        except Exception as e:
            print(f"Error con Gemini: {e}")
    
    if hf_key:
        try:
            article = _generate_with_huggingface(product_data, affiliate_link, hf_key)
            if article:
                article['provider'] = 'huggingface'
                return article
        except Exception as e:
            print(f"Error con Hugging Face: {e}")
    
    # Nota: Ollama local no funcionará en Vercel (requiere localhost). Omite esta parte o usa un fallback.
    return None

# Copia _generate_with_gemini, _generate_with_huggingface, _create_prompt, _format_article, etc.
# Asegúrate de que las URLs y claves estén correctas y que las respuestas se manejen bien.

# Copia los templates (_get_electronics_template, etc.) y _generate_emergency_fallback como están.

