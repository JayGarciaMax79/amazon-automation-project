import json
import os
import requests
from datetime import datetime

def handler(request):
    try:
        if request.method == 'POST':
            data = request.json if request.json and isinstance(request.json, dict) else {}
            if not all(field in data and data[field] for field in ['product_url', 'affiliate_link']):
                return {
                    'statusCode': 400,
                    'body': json.dumps({'success': False, 'error': 'product_url y affiliate_link son requeridos'}),
                    'headers': {'Content-Type': 'application/json'}
                }
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
                "supported_apis": ["Google Gemini (15 requests/min gratis)", "Hugging Face (Gratis con límites)", "Fallback Template (Siempre disponible)"],
                "cost": "$0.00",
                "example_request": {"product_url": "https://www.amazon.com/dp/B08N5WRWNW", "affiliate_link": "https://amzn.to/3xyz123", "category": "electronics"}
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

# Aquí deberías añadir las funciones _try_free_apis, _generate_with_gemini, _generate_with_huggingface, _create_prompt, etc.
# desde tu código original. Por ahora, usaré un placeholder para que el código sea funcional como mínimo.
def _try_free_apis(product_data, affiliate_link, category):
    return {"content": f"Artículo generado para {product_data['title']} con enlace {affiliate_link}", "provider": "fallback"}

def _generate_template_article(product_data, affiliate_link, category):
    return {"content": f"Plantilla para {product_data['title']}. Compra aquí: {affiliate_link}", "provider": "template"}

def _generate_emergency_fallback(product_url, affiliate_link):
    return {"content": f"Error al generar artículo. Visita {product_url} y usa {affiliate_link}", "provider": "emergency"}
