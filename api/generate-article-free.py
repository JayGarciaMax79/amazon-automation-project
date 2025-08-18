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
                'body': json.dumps(info, ensure
