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
            info = {...}  # Info del servicio
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

# Copia aquí _extract_basic_product_data, _try_free_apis, etc., desde tu código original.
