"""
Endpoint gratuito para generación de artículos usando APIs de IA gratuitas
Versión sin costo que no requiere OpenAI API
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import asyncio
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class FreeArticleGenerator(BaseHTTPRequestHandler):
    """
    Generador de artículos usando APIs completamente gratuitas
    """
    
    def do_POST(self):
        """Genera artículo usando IA gratuita"""
        try:
            # Leer datos de la petición
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validar datos requeridos
            if not self._validate_request(data):
                self._send_error(400, 'product_url y affiliate_link son requeridos')
                return
            
            # Generar artículo
            result = self._generate_article_sync(data)
            
            # Enviar respuesta
            self._send_response(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, 'JSON inválido')
        except Exception as e:
            self._send_error(500, f'Error interno: {str(e)}')
    
    def do_GET(self):
        """Información sobre el endpoint gratuito"""
        info = {
            "service": "Free AI Article Generator",
            "description": "Generación de artículos usando APIs de IA completamente gratuitas",
            "supported_apis": [
                "Google Gemini (15 requests/min gratis)",
                "Hugging Face (Gratis con límites)",
                "Ollama Local (Completamente gratis)",
                "Fallback Template (Siempre disponible)"
            ],
            "cost": "$0.00",
            "example_request": {
                "product_url": "https://www.amazon.com/dp/B08N5WRWNW",
                "affiliate_link": "https://amzn.to/3xyz123",
                "category": "electronics"
            }
        }
        self._send_response(200, info)
    
    def _validate_request(self, data):
        """Valida la petición"""
        required_fields = ['product_url', 'affiliate_link']
        return all(field in data and data[field] for field in required_fields)
    
    def _generate_article_sync(self, data):
        """Genera artículo de forma síncrona"""
        try:
            product_url = data['product_url']
            affiliate_link = data['affiliate_link']
            category = data.get('category', 'general')
            
            # Extraer datos básicos del producto
            product_data = self._extract_basic_product_data(product_url)
            
            # Intentar generar con APIs gratuitas
            article = self._try_free_apis(product_data, affiliate_link, category)
            
            if not article:
                # Usar template como fallback
                article = self._generate_template_article(product_data, affiliate_link, category)
            
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
                'article': self._generate_emergency_fallback(data['product_url'], data['affiliate_link'])
            }
    
    def _extract_basic_product_data(self, url):
        """Extrae datos básicos del producto desde la URL"""
        try:
            # Extraer ASIN
            import re
            asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
            asin = asin_match.group(1) if asin_match else 'UNKNOWN'
            
            # Datos básicos
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
    
    def _try_free_apis(self, product_data, affiliate_link, category):
        """Intenta generar con APIs gratuitas"""
        
        # 1. Intentar con Google Gemini (si hay API key)
        gemini_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if gemini_key:
            try:
                article = self._generate_with_gemini(product_data, affiliate_link, gemini_key)
                if article:
                    article['provider'] = 'google_gemini'
                    return article
            except Exception as e:
                print(f"Error con Gemini: {e}")
        
        # 2. Intentar con Hugging Face (si hay API key)
        hf_key = os.getenv('HUGGINGFACE_API_KEY')
        if hf_key:
            try:
                article = self._generate_with_huggingface(product_data, affiliate_link, hf_key)
                if article:
                    article['provider'] = 'huggingface'
                    return article
            except Exception as e:
                print(f"Error con Hugging Face: {e}")
        
        # 3. Intentar con Ollama local
        try:
            article = self._generate_with_ollama(product_data, affiliate_link)
            if article:
                article['provider'] = 'ollama_local'
                return article
        except Exception as e:
            print(f"Error con Ollama: {e}")
        
        return None
    
    def _generate_with_gemini(self, product_data, affiliate_link, api_key):
        """Genera con Google Gemini"""
        
        prompt = self._create_prompt(product_data, affiliate_link)
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048
            }
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['candidates'][0]['content']['parts'][0]['text']
            return self._format_article(content, product_data)
        
        return None
    
    def _generate_with_huggingface(self, product_data, affiliate_link, api_key):
        """Genera con Hugging Face"""
        
        prompt = self._create_prompt(product_data, affiliate_link, max_length=800)
        
        url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 1000,
                "temperature": 0.7
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                content = result[0].get('generated_text', '')
                return self._format_article(content, product_data)
        
        return None
    
    def _generate_with_ollama(self, product_data, affiliate_link):
        """Genera con Ollama local"""
        
        prompt = self._create_prompt(product_data, affiliate_link)
        
        url = "http://localhost:11434/api/generate"
        
        payload = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '')
            return self._format_article(content, product_data)
        
        return None
    
    def _create_prompt(self, product_data, affiliate_link, max_length=1500):
        """Crea prompt optimizado"""
        
        title = product_data.get('title', 'Producto Amazon')
        price = product_data.get('current_price', 'Ver precio')
        
        return f"""
Escribe un artículo de blog profesional en español sobre este producto:

PRODUCTO: {title}
PRECIO: {price}
ENLACE: {affiliate_link}

ESTRUCTURA REQUERIDA:
1. Título atractivo (H1)
2. Introducción (100 palabras)
3. Características principales (H2 + lista)
4. Pros y contras (H2 + listas)
5. Conclusión con llamada a la acción

REQUISITOS:
- Máximo {max_length} palabras
- Formato HTML
- Incluir enlace de afiliado naturalmente
- Tono profesional pero accesible
- Optimizado para SEO

ARTÍCULO:
"""
    
    def _format_article(self, content, product_data):
        """Formatea el artículo generado"""
        
        title = product_data.get('title', 'Producto Amazon')
        
        # Limpiar y formatear contenido
        if not content.strip():
            return None
        
        # Extraer título si está presente
        lines = content.split('\n')
        article_title = f"{title}: Análisis Completo"
        
        for line in lines:
            if any(marker in line.lower() for marker in ['<h1>', '#', 'título']):
                clean_title = line.replace('<h1>', '').replace('</h1>', '').replace('#', '').strip()
                if len(clean_title) > 10:
                    article_title = clean_title[:60]
                break
        
        return {
            'title': article_title,
            'content': content,
            'meta_description': f"Análisis completo de {title}. Características, precio y opiniones detalladas.",
            'keywords': ['amazon', 'producto', 'análisis', 'review', 'precio'],
            'word_count': len(content.split()),
            'seo_score': 7
        }
    
    def _generate_template_article(self, product_data, affiliate_link, category):
        """Genera artículo usando template (siempre funciona)"""
        
        title = product_data.get('title', 'Producto de Amazon')
        price = product_data.get('current_price', 'Ver precio en Amazon')
        asin = product_data.get('asin', 'UNKNOWN')
        
        # Templates por categoría
        templates = {
            'electronics': self._get_electronics_template(),
            'home': self._get_home_template(),
            'fashion': self._get_fashion_template(),
            'books': self._get_books_template()
        }
        
        template = templates.get(category, self._get_default_template())
        
        content = template.format(
            title=title,
            price=price,
            affiliate_link=affiliate_link,
            asin=asin
        )
        
        return {
            'title': f"{title}: Análisis y Opinión",
            'content': content,
            'meta_description': f"Análisis detallado de {title}. Características, precio y dónde comprarlo al mejor precio.",
            'keywords': ['amazon', 'producto', 'análisis', 'precio', 'comprar'],
            'word_count': len(content.split()),
            'seo_score': 6,
            'provider': 'template'
        }
    
    def _get_electronics_template(self):
        return """
        <h1>{title}: Análisis Técnico Completo</h1>
        
        <p>En el mundo de la tecnología, encontrar productos que combinen calidad, rendimiento y precio justo puede ser un desafío. Hoy analizamos <strong>{title}</strong>, un dispositivo que ha captado nuestra atención por sus características técnicas y excelente relación calidad-precio.</p>
        
        <h2>Especificaciones y Características Técnicas</h2>
        <p>Este producto destaca por su construcción sólida y especificaciones técnicas avanzadas. Con un precio de <strong>{price}</strong>, ofrece características que normalmente encontraríamos en dispositivos de gama superior.</p>
        
        <ul>
            <li>Diseño moderno y funcional</li>
            <li>Materiales de alta calidad</li>
            <li>Tecnología avanzada integrada</li>
            <li>Excelente rendimiento en pruebas</li>
            <li>Compatibilidad amplia con otros dispositivos</li>
        </ul>
        
        <h2>Rendimiento y Experiencia de Uso</h2>
        <p>Durante nuestras pruebas, este dispositivo demostró un rendimiento consistente y confiable. La experiencia de usuario es fluida y las funcionalidades responden según lo esperado.</p>
        
        <h2>Pros y Contras</h2>
        <h3>Ventajas:</h3>
        <ul>
            <li>Excelente relación calidad-precio</li>
            <li>Construcción sólida y duradera</li>
            <li>Fácil configuración y uso</li>
            <li>Buen soporte técnico</li>
        </ul>
        
        <h3>Desventajas:</h3>
        <ul>
            <li>Disponibilidad limitada en algunos colores</li>
            <li>Manual de usuario podría ser más detallado</li>
        </ul>
        
        <h2>Conclusión y Recomendación</h2>
        <p>Después de nuestro análisis exhaustivo, consideramos que <strong>{title}</strong> es una excelente opción para quienes buscan tecnología de calidad sin comprometer el presupuesto.</p>
        
        <p>Si estás interesado en este producto, puedes encontrarlo al mejor precio <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haciendo clic aquí</a>.</p>
        
        <p><strong>¡No esperes más!</strong> <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">Consigue este increíble dispositivo ahora con el mejor precio disponible</a>.</p>
        """
    
    def _get_home_template(self):
        return """
        <h1>{title}: La Solución Perfecta para tu Hogar</h1>
        
        <p>Crear un hogar cómodo y funcional requiere elegir los productos adecuados. <strong>{title}</strong> se presenta como una solución práctica que combina funcionalidad, diseño y precio accesible para mejorar tu espacio vital.</p>
        
        <h2>Características y Funcionalidad</h2>
        <p>Este producto para el hogar destaca por su versatilidad y facilidad de uso. Con un precio de <strong>{price}</strong>, ofrece características que lo convierten en una inversión inteligente para cualquier hogar moderno.</p>
        
        <ul>
            <li>Diseño elegante que se adapta a cualquier decoración</li>
            <li>Materiales resistentes y fáciles de limpiar</li>
            <li>Instalación sencilla sin herramientas complejas</li>
            <li>Funcionalidad práctica para el día a día</li>
            <li>Tamaño optimizado para espacios diversos</li>
        </ul>
        
        <h2>Beneficios para tu Hogar</h2>
        <p>La incorporación de este producto en tu hogar aporta beneficios inmediatos en términos de comodidad, organización y estética. Su diseño pensado para la vida moderna lo hace indispensable.</p>
        
        <h2>Análisis de Ventajas y Desventajas</h2>
        <h3>Puntos Fuertes:</h3>
        <ul>
            <li>Excelente calidad de materiales</li>
            <li>Precio competitivo en el mercado</li>
            <li>Fácil mantenimiento</li>
            <li>Diseño atemporal</li>
        </ul>
        
        <h3>Aspectos a Considerar:</h3>
        <ul>
            <li>Requiere espacio específico para instalación</li>
            <li>Disponibilidad limitada en ciertos acabados</li>
        </ul>
        
        <h2>Nuestra Recomendación Final</h2>
        <p><strong>{title}</strong> representa una excelente inversión para mejorar la funcionalidad y estética de tu hogar. Su combinación de calidad, diseño y precio lo convierte en una opción altamente recomendable.</p>
        
        <p>Para adquirir este producto al mejor precio disponible, <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haz clic aquí</a>.</p>
        
        <p><strong>¡Transforma tu hogar hoy!</strong> <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">Obtén este producto ahora y disfruta de sus beneficios inmediatamente</a>.</p>
        """
    
    def _get_fashion_template(self):
        return """
        <h1>{title}: Estilo y Tendencia en una Sola Pieza</h1>
        
        <p>La moda es una forma de expresión personal, y encontrar piezas que combinen estilo, calidad y precio accesible puede ser todo un desafío. <strong>{title}</strong> emerge como una opción que satisface estas tres necesidades fundamentales del guardarropa moderno.</p>
        
        <h2>Diseño y Estilo</h2>
        <p>Esta pieza destaca por su diseño contemporáneo y versatilidad. Con un precio de <strong>{price}</strong>, ofrece la oportunidad de incorporar tendencias actuales sin comprometer el presupuesto destinado a moda.</p>
        
        <ul>
            <li>Diseño moderno y versátil</li>
            <li>Materiales de calidad superior</li>
            <li>Corte favorecedor para diferentes tipos de cuerpo</li>
            <li>Colores y patrones actuales</li>
            <li>Fácil combinación con otras prendas</li>
        </ul>
        
        <h2>Versatilidad y Combinaciones</h2>
        <p>Una de las grandes ventajas de esta pieza es su capacidad de adaptarse a diferentes ocasiones y estilos. Desde looks casuales hasta combinaciones más elegantes, ofrece múltiples posibilidades de uso.</p>
        
        <h2>Calidad y Durabilidad</h2>
        <p>Los materiales utilizados en la confección garantizan durabilidad y comodidad. El cuidado de la prenda es sencillo, manteniendo su apariencia original tras múltiples lavados.</p>
        
        <h2>Evaluación Completa</h2>
        <h3>Aspectos Positivos:</h3>
        <ul>
            <li>Excelente relación calidad-precio</li>
            <li>Diseño atemporal y moderno</li>
            <li>Materiales cómodos y duraderos</li>
            <li>Versatilidad para diferentes ocasiones</li>
        </ul>
        
        <h3>Consideraciones:</h3>
        <ul>
            <li>Disponibilidad limitada en algunas tallas</li>
            <li>Colores pueden variar ligeramente respecto a las fotos</li>
        </ul>
        
        <h2>Conclusión de Estilo</h2>
        <p><strong>{title}</strong> representa una adición valiosa a cualquier guardarropa. Su combinación de estilo contemporáneo, calidad de materiales y precio accesible lo convierte en una compra inteligente para quienes valoran la moda consciente.</p>
        
        <p>Si quieres añadir esta pieza a tu colección, puedes encontrarla al mejor precio <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haciendo clic aquí</a>.</p>
        
        <p><strong>¡Renueva tu estilo!</strong> <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">Consigue esta increíble pieza ahora y destaca con tu look</a>.</p>
        """
    
    def _get_books_template(self):
        return """
        <h1>{title}: Una Lectura que Transforma Perspectivas</h1>
        
        <p>En un mundo donde la información abunda, encontrar libros que realmente aporten valor y conocimiento se vuelve fundamental. <strong>{title}</strong> se presenta como una obra que promete enriquecer la experiencia lectora y aportar insights valiosos a sus lectores.</p>
        
        <h2>Contenido y Estructura</h2>
        <p>Este libro, disponible por <strong>{price}</strong>, ofrece un contenido bien estructurado que facilita la comprensión y el aprendizaje progresivo. La organización de los capítulos permite tanto una lectura secuencial como la consulta de temas específicos.</p>
        
        <ul>
            <li>Contenido actualizado y relevante</li>
            <li>Estructura clara y bien organizada</li>
            <li>Ejemplos prácticos y casos de estudio</li>
            <li>Lenguaje accesible para diferentes niveles</li>
            <li>Referencias y recursos adicionales</li>
        </ul>
        
        <h2>Valor Educativo y Aplicabilidad</h2>
        <p>El valor de este libro radica en su capacidad de traducir conceptos complejos en ideas aplicables. Los lectores encontrarán herramientas prácticas que pueden implementar inmediatamente en sus áreas de interés.</p>
        
        <h2>Audiencia y Recomendaciones</h2>
        <p>Esta obra resulta especialmente valiosa para profesionales, estudiantes y cualquier persona interesada en expandir sus conocimientos en el tema tratado. Su enfoque equilibrado entre teoría y práctica lo hace accesible para diferentes perfiles de lectores.</p>
        
        <h2>Análisis Crítico</h2>
        <h3>Fortalezas del Libro:</h3>
        <ul>
            <li>Contenido bien investigado y documentado</li>
            <li>Estilo de escritura claro y engaging</li>
            <li>Ejemplos relevantes y actuales</li>
            <li>Precio accesible para el valor ofrecido</li>
        </ul>
        
        <h3>Áreas de Mejora:</h3>
        <ul>
            <li>Algunos capítulos podrían ser más concisos</li>
            <li>Falta de recursos digitales complementarios</li>
        </ul>
        
        <h2>Recomendación Final</h2>
        <p><strong>{title}</strong> constituye una inversión valiosa en conocimiento. Su contenido sólido, presentación clara y precio accesible lo convierten en una adición recomendable a cualquier biblioteca personal o profesional.</p>
        
        <p>Si estás interesado en adquirir este libro, puedes encontrarlo al mejor precio <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haciendo clic aquí</a>.</p>
        
        <p><strong>¡Invierte en tu conocimiento!</strong> <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">Consigue este libro ahora y comienza tu viaje de aprendizaje</a>.</p>
        """
    
    def _get_default_template(self):
        return """
        <h1>{title}: Análisis Completo y Detallado</h1>
        
        <p>En el mercado actual, encontrar productos que combinen calidad, funcionalidad y precio justo puede ser un verdadero desafío. <strong>{title}</strong> se presenta como una opción que merece nuestra atención y análisis detallado.</p>
        
        <h2>Características Principales</h2>
        <p>Este producto, disponible por <strong>{price}</strong>, destaca por sus características únicas que lo diferencian de la competencia. Su diseño y funcionalidad han sido pensados para satisfacer las necesidades del usuario moderno.</p>
        
        <ul>
            <li>Diseño innovador y funcional</li>
            <li>Materiales de alta calidad</li>
            <li>Excelente relación calidad-precio</li>
            <li>Fácil uso y mantenimiento</li>
            <li>Garantía y soporte del fabricante</li>
        </ul>
        
        <h2>Experiencia de Usuario</h2>
        <p>La experiencia de uso de este producto ha sido evaluada considerando diferentes escenarios y tipos de usuario. Los resultados muestran un rendimiento consistente y satisfactorio en la mayoría de las situaciones de uso.</p>
        
        <h2>Comparación con Alternativas</h2>
        <p>Al comparar este producto con alternativas similares en el mercado, destaca por ofrecer características premium a un precio más accesible, sin comprometer la calidad o funcionalidad.</p>
        
        <h2>Evaluación Objetiva</h2>
        <h3>Puntos Fuertes:</h3>
        <ul>
            <li>Excelente calidad de construcción</li>
            <li>Precio competitivo en su categoría</li>
            <li>Funcionalidad intuitiva</li>
            <li>Buenas valoraciones de usuarios</li>
        </ul>
        
        <h3>Aspectos a Considerar:</h3>
        <ul>
            <li>Disponibilidad puede ser limitada</li>
            <li>Algunas funciones avanzadas requieren aprendizaje</li>
        </ul>
        
        <h2>Conclusión y Recomendación</h2>
        <p>Después de nuestro análisis exhaustivo, <strong>{title}</strong> emerge como una opción sólida y recomendable. Su combinación de calidad, funcionalidad y precio lo convierte en una compra inteligente para quienes buscan valor real.</p>
        
        <p>Si estás considerando este producto, puedes encontrarlo al mejor precio disponible <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">haciendo clic aquí</a>.</p>
        
        <p><strong>¡No dejes pasar esta oportunidad!</strong> <a href="{affiliate_link}" target="_blank" rel="nofollow noopener">Adquiere este excelente producto ahora y disfruta de sus beneficios</a>.</p>
        """
    
    def _generate_emergency_fallback(self, product_url, affiliate_link):
        """Fallback de emergencia si todo falla"""
        return {
            'title': 'Producto Amazon - Análisis',
            'content': f'''
            <h1>Producto Amazon - Análisis y Opinión</h1>
            <p>Hemos analizado este interesante producto disponible en Amazon.</p>
            <h2>¿Por qué considerarlo?</h2>
            <ul>
                <li>Disponible en Amazon con envío rápido</li>
                <li>Buenas valoraciones de usuarios</li>
                <li>Precio competitivo</li>
            </ul>
            <p>Puedes ver más detalles y comprarlo <a href="{affiliate_link}" target="_blank" rel="nofollow">aquí</a>.</p>
            ''',
            'meta_description': 'Análisis de producto Amazon. Características y mejor precio.',
            'keywords': ['amazon', 'producto'],
            'word_count': 50,
            'seo_score': 4
        }
    
    def _send_response(self, status_code, data):
        """Envía respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """Envía respuesta de error"""
        error_data = {
            'success': False,
            'error': message,
            'status_code': status_code,
            'cost': 0.0
        }
        self._send_response(status_code, error_data)
    
    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Handler para Vercel
def handler(request, response):
    """Handler principal para Vercel"""
    api_handler = FreeArticleGenerator()
    
    # Simular request para BaseHTTPRequestHandler
    api_handler.command = request.method
    api_handler.path = request.url
    api_handler.headers = request.headers
    
    if request.method == 'POST':
        api_handler.do_POST()
    elif request.method == 'GET':
        api_handler.do_GET()
    elif request.method == 'OPTIONS':
        api_handler.do_OPTIONS()
    else:
        api_handler._send_error(405, 'Método no permitido')

# Para testing local
if __name__ == '__main__':
    from http.server import HTTPServer
    
    server = HTTPServer(('localhost', 8001), FreeArticleGenerator)
    print("🚀 Servidor de artículos GRATUITOS iniciado en http://localhost:8001")
    print("💰 Costo: $0.00 - Completamente gratis")
    print("🤖 APIs soportadas: Gemini, Hugging Face, Ollama, Templates")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Servidor detenido")
        server.shutdown()

