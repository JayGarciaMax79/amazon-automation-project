"""
Health check endpoint para monitoreo del servicio
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Health check endpoint"""
        
        # Verificar variables de entorno críticas
        env_status = {
            'openai_api_key': bool(os.getenv('OPENAI_API_KEY')),
            'google_sheets_api': bool(os.getenv('GOOGLE_SHEETS_API_KEY')),
            'wordpress_api': bool(os.getenv('WORDPRESS_API_URL')),
            'make_webhook': bool(os.getenv('MAKE_WEBHOOK_URL'))
        }
        
        # Determinar estado general
        all_configured = all(env_status.values())
        status = "healthy" if all_configured else "degraded"
        
        health_data = {
            "status": status,
            "service": "Amazon Article Automation API",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "environment": {
                "python_version": "3.11",
                "platform": "Vercel",
                "region": os.getenv('VERCEL_REGION', 'unknown')
            },
            "configuration": env_status,
            "endpoints": {
                "generate_article": "/api/generate-article",
                "scrape_amazon": "/api/scrape-amazon", 
                "webhook": "/api/webhook",
                "docs": "/api/docs"
            },
            "dependencies": {
                "openai": "1.58.1",
                "beautifulsoup4": "4.13.4",
                "requests": "2.32.4",
                "flask": "3.1.0"
            }
        }
        
        # Código de respuesta basado en el estado
        status_code = 200 if status == "healthy" else 503
        
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        
        response = json.dumps(health_data, indent=2, ensure_ascii=False)
        self.wfile.write(response.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

