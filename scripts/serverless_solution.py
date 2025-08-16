"""
Función serverless para Vercel que extrae datos de productos de Amazon
Compatible con Vercel Functions (Python)
"""

import json
import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin
from http.server import BaseHTTPRequestHandler

class AmazonScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def scrape_product(self, url):
        """Extrae datos de un producto de Amazon"""
        try:
            # Delay para evitar detección
            time.sleep(random.uniform(0.5, 2))
            
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'success': True,
                'data': {
                    'url': url,
                    'title': self._get_title(soup),
                    'price': self._get_price(soup),
                    'description': self._get_description(soup),
                    'images': self._get_images(soup, url),
                    'rating': self._get_rating(soup),
                    'reviews_count': self._get_reviews_count(soup),
                    'availability': self._get_availability(soup),
                    'features': self._get_features(soup),
                    'asin': self._get_asin(url, soup),
                    'category': self._get_category(soup)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al extraer datos: {str(e)}'
            }
    
    def _get_title(self, soup):
        selectors = ['#productTitle', '.product-title', 'h1.a-size-large', 'h1 span']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text().strip()
        return "Título no encontrado"
    
    def _get_price(self, soup):
        selectors = [
            '.a-price-whole',
            '.a-price .a-offscreen',
            '#priceblock_dealprice',
            '#priceblock_ourprice',
            '.a-price-range'
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                price_text = element.get_text().strip()
                price_clean = re.sub(r'[^\d.,]', '', price_text)
                if price_clean:
                    return price_clean
        return "Precio no disponible"
    
    def _get_description(self, soup):
        selectors = [
            '#feature-bullets ul',
            '#productDescription',
            '.a-unordered-list.a-vertical.a-spacing-mini'
        ]
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'ul':
                    items = element.find_all('li')
                    description = ' '.join([item.get_text().strip() for item in items if item.get_text().strip()])
                else:
                    description = element.get_text().strip()
                
                if description and len(description) > 20:
                    return description[:1500]
        return "Descripción no disponible"
    
    def _get_images(self, soup, base_url):
        images = []
        selectors = ['#landingImage', '.a-dynamic-image', '#imgTagWrapperId img']
        
        for selector in selectors:
            elements = soup.select(selector)
            for img in elements:
                src = img.get('src') or img.get('data-src')
                if src:
                    full_url = urljoin(base_url, src)
                    if full_url not in images:
                        images.append(full_url)
        
        return images[:3]  # Limitar a 3 imágenes
    
    def _get_rating(self, soup):
        selectors = ['.a-icon-alt', '.a-star-5 .a-icon-alt']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                rating_text = element.get_text()
                rating_match = re.search(r'(\d+\.?\d*)\s*de\s*5|(\d+\.?\d*)\s*out\s*of\s*5', rating_text)
                if rating_match:
                    return rating_match.group(1) or rating_match.group(2)
        return "Sin calificación"
    
    def _get_reviews_count(self, soup):
        selectors = ['#acrCustomerReviewText', '.a-link-normal .a-size-base']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                reviews_text = element.get_text()
                reviews_match = re.search(r'([\d,]+)\s*(reviews?|reseñas?)', reviews_text, re.IGNORECASE)
                if reviews_match:
                    return reviews_match.group(1).replace(',', '')
        return "0"
    
    def _get_availability(self, soup):
        selectors = ['#availability span', '.a-color-success', '.a-color-state']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                availability = element.get_text().strip()
                if availability and len(availability) < 100:
                    return availability
        return "Disponibilidad no especificada"
    
    def _get_features(self, soup):
        features = []
        selectors = ['#feature-bullets li span', '.a-unordered-list.a-vertical li span']
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                feature = element.get_text().strip()
                if feature and len(feature) > 10 and feature not in features:
                    features.append(feature)
                    if len(features) >= 5:
                        break
            if features:
                break
        
        return features
    
    def _get_asin(self, url, soup):
        asin_match = re.search(r'/dp/([A-Z0-9]{10})', url)
        if asin_match:
            return asin_match.group(1)
        
        selectors = ['[data-asin]', '#ASIN']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                asin = element.get('data-asin') or element.get('value')
                if asin:
                    return asin
        
        return "ASIN no encontrado"
    
    def _get_category(self, soup):
        selectors = ['#wayfinding-breadcrumbs_feature_div', '.a-breadcrumb']
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                category = element.get_text().strip()
                if category:
                    return category[:200]
        return "Categoría no especificada"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Maneja las peticiones POST para scraping de Amazon"""
        try:
            # Leer el cuerpo de la petición
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Validar que se proporcione la URL
            if 'url' not in data:
                self._send_error(400, 'URL del producto es requerida')
                return
            
            url = data['url']
            
            # Validar que sea una URL de Amazon
            if 'amazon.' not in url:
                self._send_error(400, 'La URL debe ser de Amazon')
                return
            
            # Realizar el scraping
            scraper = AmazonScraper()
            result = scraper.scrape_product(url)
            
            # Enviar respuesta
            self._send_response(200, result)
            
        except json.JSONDecodeError:
            self._send_error(400, 'JSON inválido')
        except Exception as e:
            self._send_error(500, f'Error interno: {str(e)}')
    
    def do_GET(self):
        """Maneja las peticiones GET para health check"""
        health_data = {
            'status': 'healthy',
            'service': 'Amazon Product Scraper',
            'version': '1.0.0'
        }
        self._send_response(200, health_data)
    
    def _send_response(self, status_code, data):
        """Envía una respuesta JSON"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))
    
    def _send_error(self, status_code, message):
        """Envía una respuesta de error"""
        error_data = {
            'success': False,
            'error': message
        }
        self._send_response(status_code, error_data)
    
    def do_OPTIONS(self):
        """Maneja las peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Para uso local/testing
if __name__ == '__main__':
    scraper = AmazonScraper()
    test_url = "https://www.amazon.com/dp/B08N5WRWNW"  # URL de ejemplo
    result = scraper.scrape_product(test_url)
    print(json.dumps(result, indent=2, ensure_ascii=False))

