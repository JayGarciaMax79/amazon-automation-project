"""
Webhook endpoint para integración con Make.com
Recibe datos desde Google Sheets y orquesta el procesamiento
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import asyncio
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Procesa webhooks desde Make.com"""
        try:
            # Leer datos de la petición
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validar datos requeridos
            if not self._validate_webhook_data(data):
                self._send_error(400, 'Datos de webhook inválidos')
                return
            
            # Procesar según el tipo de evento
            event_type = data.get('event_type', 'process_article')
            
            if event_type == 'process_article':
                result = self._process_article_request(data)
            elif event_type == 'health_check':
                result = self._process_health_check(data)
            elif event_type == 'deployment_notification':
                result = self._process_deployment_notification(data)
            else:
                result = {
                    'success': False,
                    'error': f'Tipo de evento no soportado: {event_type}'
                }
            
            # Enviar respuesta
            self._send_response(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, 'JSON inválido en webhook')
        except Exception as e:
            self._send_error(500, f'Error procesando webhook: {str(e)}')
    
    def do_GET(self):
        """Información sobre el webhook endpoint"""
        info = {
            "endpoint": "/api/webhook",
            "method": "POST",
            "description": "Webhook para integración con Make.com",
            "supported_events": [
                "process_article",
                "health_check", 
                "deployment_notification"
            ],
            "example_payload": {
                "event_type": "process_article",
                "product_url": "https://www.amazon.com/dp/B08N5WRWNW",
                "affiliate_link": "https://amzn.to/3xyz123",
                "row_number": 2,
                "sheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
            }
        }
        
        self._send_response(200, info)
    
    def _validate_webhook_data(self, data):
        """Valida los datos del webhook"""
        if not isinstance(data, dict):
            return False
        
        event_type = data.get('event_type', 'process_article')
        
        if event_type == 'process_article':
            required_fields = ['product_url', 'affiliate_link']
            return all(field in data and data[field] for field in required_fields)
        
        return True  # Otros tipos de eventos son menos estrictos
    
    def _process_article_request(self, data):
        """Procesa solicitud de generación de artículo"""
        try:
            product_url = data['product_url']
            affiliate_link = data['affiliate_link']
            row_number = data.get('row_number')
            sheet_id = data.get('sheet_id')
            
            # Validar URLs
            if not self._is_valid_amazon_url(product_url):
                return {
                    'success': False,
                    'error': 'URL de Amazon inválida',
                    'row_number': row_number
                }
            
            if not self._is_valid_affiliate_link(affiliate_link):
                return {
                    'success': False,
                    'error': 'Enlace de afiliado inválido',
                    'row_number': row_number
                }
            
            # Aquí se integraría con el generador de artículos
            # Por ahora, simulamos el procesamiento
            
            # En un entorno real, esto llamaría a:
            # 1. /api/scrape-amazon para extraer datos
            # 2. /api/generate-article para crear el artículo
            # 3. WordPress API para publicar
            
            # Respuesta simulada
            result = {
                'success': True,
                'message': 'Artículo procesado exitosamente',
                'data': {
                    'product_url': product_url,
                    'affiliate_link': affiliate_link,
                    'article_title': f'Análisis del producto Amazon',
                    'article_url': f'https://myamzdeals.shop/producto-{row_number}',
                    'processing_time': '45 segundos',
                    'word_count': 1850,
                    'seo_score': 8
                },
                'row_number': row_number,
                'sheet_id': sheet_id,
                'processed_at': datetime.utcnow().isoformat() + 'Z'
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error procesando artículo: {str(e)}',
                'row_number': data.get('row_number')
            }
    
    def _process_health_check(self, data):
        """Procesa health check desde Make.com"""
        return {
            'success': True,
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'service': 'Amazon Article Automation Webhook',
            'version': '1.0.0'
        }
    
    def _process_deployment_notification(self, data):
        """Procesa notificación de deployment"""
        return {
            'success': True,
            'message': 'Notificación de deployment recibida',
            'deployment_info': {
                'repository': data.get('repository'),
                'commit': data.get('commit'),
                'branch': data.get('branch'),
                'deployment_url': data.get('deployment_url')
            },
            'received_at': datetime.utcnow().isoformat() + 'Z'
        }
    
    def _is_valid_amazon_url(self, url):
        """Valida si es una URL válida de Amazon"""
        if not url or not isinstance(url, str):
            return False
        
        amazon_domains = [
            'amazon.com', 'amazon.es', 'amazon.co.uk', 'amazon.de',
            'amazon.fr', 'amazon.it', 'amazon.ca', 'amazon.com.mx'
        ]
        
        return any(domain in url for domain in amazon_domains) and '/dp/' in url
    
    def _is_valid_affiliate_link(self, link):
        """Valida si es un enlace de afiliado válido"""
        if not link or not isinstance(link, str):
            return False
        
        return 'amzn.to' in link or ('amazon.' in link and 'tag=' in link)
    
    def _send_response(self, status_code, data):
        """Envía respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """Envía respuesta de error"""
        error_data = {
            'success': False,
            'error': message,
            'status_code': status_code,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        self._send_response(status_code, error_data)
    
    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

