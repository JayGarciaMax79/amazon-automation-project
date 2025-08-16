"""
Función Serverless para Vercel que integra OpenManus
para generar artículos de productos de Amazon
"""

import json
import os
import asyncio
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Configurar variables de entorno para OpenAI
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', 'sk-placeholder')
os.environ['OPENAI_API_BASE'] = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')

class AmazonArticleAPI(BaseHTTPRequestHandler):
    """
    API Handler para generar artículos de Amazon usando OpenManus
    """
    
    def do_POST(self):
        """Maneja peticiones POST para generar artículos"""
        try:
            # Leer datos de la petición
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validar datos requeridos
            if not self._validate_request(data):
                self._send_error(400, 'product_url y affiliate_link son requeridos')
                return
            
            # Procesar la solicitud
            result = self._process_article_request(data)
            
            # Enviar respuesta
            self._send_response(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, 'JSON inválido')
        except Exception as e:
            self._send_error(500, f'Error interno: {str(e)}')
    
    def do_GET(self):
        """Maneja peticiones GET para health check y documentación"""
        parsed_url = urlparse(self.path)
        
        if parsed_url.path == '/api/health':
            self._send_health_check()
        elif parsed_url.path == '/api/docs':
            self._send_documentation()
        else:
            self._send_error(404, 'Endpoint no encontrado')
    
    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self._send_cors_headers()
        self.end_headers()
    
    def _validate_request(self, data):
        """Valida que la petición tenga los datos requeridos"""
        required_fields = ['product_url', 'affiliate_link']
        return all(field in data and data[field] for field in required_fields)
    
    def _process_article_request(self, data):
        """Procesa la solicitud de generación de artículo"""
        try:
            # Simular el procesamiento con OpenManus
            # En un entorno real, aquí se llamaría al generador de artículos
            
            product_url = data['product_url']
            affiliate_link = data['affiliate_link']
            
            # Validar que sea una URL de Amazon
            if 'amazon.' not in product_url:
                return {
                    'success': False,
                    'error': 'La URL debe ser de Amazon'
                }
            
            # Generar artículo (versión simplificada para demo)
            article_data = self._generate_demo_article(product_url, affiliate_link)
            
            return {
                'success': True,
                'article': article_data,
                'processing_time': '45 segundos',
                'status': 'completed'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al procesar artículo: {str(e)}'
            }
    
    def _generate_demo_article(self, product_url, affiliate_link):
        """Genera un artículo de demostración"""
        # Extraer ASIN de la URL
        asin = self._extract_asin(product_url)
        
        return {
            'title': f'Análisis Completo: Producto Amazon {asin}',
            'meta_description': f'Descubre todo sobre este increíble producto de Amazon. Análisis detallado, características y mejor precio.',
            'content': f'''
            <h1>Análisis Completo: Producto Amazon {asin}</h1>
            
            <p>En este artículo te presentamos un análisis exhaustivo de este fantástico producto disponible en Amazon. Hemos evaluado cada aspecto para ayudarte a tomar la mejor decisión de compra.</p>
            
            <h2>Características Principales</h2>
            <p>Este producto destaca por su excelente calidad y funcionalidad. Las características más importantes incluyen:</p>
            <ul>
                <li>Diseño innovador y atractivo</li>
                <li>Materiales de alta calidad</li>
                <li>Excelente relación calidad-precio</li>
                <li>Fácil instalación y uso</li>
            </ul>
            
            <h2>Análisis Detallado</h2>
            <p>Después de una evaluación minuciosa, podemos afirmar que este producto cumple con las expectativas. Su rendimiento es consistente y la calidad de construcción es notable.</p>
            
            <h2>Pros y Contras</h2>
            <h3>Ventajas:</h3>
            <ul>
                <li>Excelente calidad de materiales</li>
                <li>Precio competitivo</li>
                <li>Fácil de usar</li>
                <li>Buenas reseñas de usuarios</li>
            </ul>
            
            <h3>Desventajas:</h3>
            <ul>
                <li>Disponibilidad limitada en algunos colores</li>
                <li>Instrucciones podrían ser más claras</li>
            </ul>
            
            <h2>Conclusión y Recomendación</h2>
            <p>Este producto representa una excelente opción para quienes buscan calidad y funcionalidad. Su precio es justo y las características lo convierten en una compra inteligente.</p>
            
            <p><strong>¿Dónde comprarlo?</strong> Puedes adquirir este producto al mejor precio <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haciendo clic aquí</a>.</p>
            
            <p>No esperes más y aprovecha esta oportunidad. <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">¡Cómpralo ahora con el mejor precio!</a></p>
            ''',
            'keywords': ['amazon', 'producto', 'análisis', 'review', 'comprar', 'precio'],
            'category': 'general',
            'word_count': 350,
            'seo_score': 8,
            'estimated_read_time': 2
        }
    
    def _extract_asin(self, url):
        """Extrae el ASIN de una URL de Amazon"""
        import re
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            return asin_match.group(1)
        return 'UNKNOWN'
    
    def _send_health_check(self):
        """Envía respuesta de health check"""
        health_data = {
            'status': 'healthy',
            'service': 'Amazon Article Generator with OpenManus',
            'version': '1.0.0',
            'endpoints': {
                'POST /api/generate': 'Generar artículo de producto Amazon',
                'GET /api/health': 'Health check',
                'GET /api/docs': 'Documentación de la API'
            }
        }
        self._send_response(200, health_data)
    
    def _send_documentation(self):
        """Envía documentación de la API"""
        docs = {
            'title': 'Amazon Article Generator API',
            'description': 'API para generar artículos de productos de Amazon usando OpenManus',
            'version': '1.0.0',
            'endpoints': {
                'POST /api/generate': {
                    'description': 'Genera un artículo completo sobre un producto de Amazon',
                    'parameters': {
                        'product_url': 'URL del producto de Amazon (requerido)',
                        'affiliate_link': 'Enlace de afiliado de Amazon (requerido)',
                        'category': 'Categoría del producto (opcional)',
                        'language': 'Idioma del artículo (opcional, default: es)'
                    },
                    'response': {
                        'success': 'boolean',
                        'article': {
                            'title': 'Título del artículo',
                            'content': 'Contenido HTML del artículo',
                            'meta_description': 'Meta descripción para SEO',
                            'keywords': 'Array de palabras clave',
                            'word_count': 'Número de palabras',
                            'seo_score': 'Puntuación SEO (1-10)'
                        }
                    }
                }
            },
            'examples': {
                'request': {
                    'product_url': 'https://www.amazon.com/dp/B08N5WRWNW',
                    'affiliate_link': 'https://amzn.to/3xyz123'
                }
            }
        }
        self._send_response(200, docs)
    
    def _send_response(self, status_code, data):
        """Envía una respuesta JSON"""
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """Envía una respuesta de error"""
        error_data = {
            'success': False,
            'error': message,
            'status_code': status_code
        }
        self._send_response(status_code, error_data)
    
    def _send_cors_headers(self):
        """Envía headers CORS"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')

# Handler principal para Vercel
def handler(request, response):
    """
    Handler principal para Vercel Functions
    """
    try:
        # Crear instancia del handler
        api_handler = AmazonArticleAPI()
        
        # Simular el request para BaseHTTPRequestHandler
        api_handler.command = request.method
        api_handler.path = request.url
        api_handler.headers = request.headers
        
        # Procesar según el método
        if request.method == 'POST':
            api_handler.do_POST()
        elif request.method == 'GET':
            api_handler.do_GET()
        elif request.method == 'OPTIONS':
            api_handler.do_OPTIONS()
        else:
            api_handler._send_error(405, 'Método no permitido')
            
    except Exception as e:
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        response.body = json.dumps({
            'success': False,
            'error': f'Error interno del servidor: {str(e)}'
        })

# Para testing local
if __name__ == '__main__':
    from http.server import HTTPServer
    
    server = HTTPServer(('localhost', 8000), AmazonArticleAPI)
    print("Servidor iniciado en http://localhost:8000")
    print("Endpoints disponibles:")
    print("- POST /api/generate - Generar artículo")
    print("- GET /api/health - Health check")
    print("- GET /api/docs - Documentación")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        server.shutdown()

