"""
Página principal de la API de Amazon Article Automation
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Página principal de la API"""
        
        html_content = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Amazon Article Automation API</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                    color: #333;
                }
                .header {
                    text-align: center;
                    margin-bottom: 40px;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 10px;
                }
                .endpoint {
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 8px;
                    padding: 20px;
                    margin: 20px 0;
                }
                .method {
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 12px;
                }
                .get { background: #28a745; color: white; }
                .post { background: #007bff; color: white; }
                .code {
                    background: #f1f3f4;
                    padding: 10px;
                    border-radius: 4px;
                    font-family: 'Courier New', monospace;
                    overflow-x: auto;
                }
                .status {
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 4px;
                    background: #28a745;
                    color: white;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 Amazon Article Automation API</h1>
                <p>Generación automática de artículos de productos Amazon con IA</p>
                <div class="status">✅ ONLINE</div>
            </div>

            <h2>📋 Endpoints Disponibles</h2>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/generate-article</h3>
                <p><strong>Descripción:</strong> Genera un artículo completo sobre un producto de Amazon usando OpenManus AI</p>
                <p><strong>Parámetros:</strong></p>
                <div class="code">
{
  "product_url": "https://www.amazon.com/dp/B08N5WRWNW",
  "affiliate_link": "https://amzn.to/3xyz123"
}
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/scrape-amazon</h3>
                <p><strong>Descripción:</strong> Extrae datos de un producto de Amazon</p>
                <p><strong>Parámetros:</strong></p>
                <div class="code">
{
  "url": "https://www.amazon.com/dp/B08N5WRWNW"
}
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method post">POST</span> /api/webhook</h3>
                <p><strong>Descripción:</strong> Webhook para recibir datos desde Make.com</p>
                <p><strong>Uso:</strong> Configurar en Make.com para orquestación automática</p>
            </div>

            <div class="endpoint">
                <h3><span class="method get">GET</span> /api/health</h3>
                <p><strong>Descripción:</strong> Health check del servicio</p>
                <p><strong>Respuesta:</strong></p>
                <div class="code">
{
  "status": "healthy",
  "service": "Amazon Article Automation",
  "version": "1.0.0"
}
                </div>
            </div>

            <div class="endpoint">
                <h3><span class="method get">GET</span> /api/docs</h3>
                <p><strong>Descripción:</strong> Documentación completa de la API</p>
                <p><strong>Formato:</strong> JSON con especificaciones OpenAPI</p>
            </div>

            <h2>🔧 Configuración</h2>
            <p>Para usar esta API necesitas configurar las siguientes variables de entorno:</p>
            <div class="code">
OPENAI_API_KEY=sk-...
GOOGLE_SHEETS_API_KEY=...
WORDPRESS_API_URL=https://tu-sitio.com/wp-json/wp/v2
MAKE_WEBHOOK_URL=https://hook.integromat.com/...
            </div>

            <h2>📖 Documentación</h2>
            <ul>
                <li><a href="https://github.com/tu-usuario/amazon-automation-project">📚 GitHub Repository</a></li>
                <li><a href="/api/docs">📋 API Documentation</a></li>
                <li><a href="https://docs.tu-dominio.com">🔧 Setup Guide</a></li>
            </ul>

            <h2>🆘 Soporte</h2>
            <p>Si necesitas ayuda:</p>
            <ul>
                <li>📧 Email: soporte@tu-dominio.com</li>
                <li>🐛 Issues: <a href="https://github.com/tu-usuario/amazon-automation-project/issues">GitHub Issues</a></li>
                <li>💬 Discord: <a href="https://discord.gg/...">Únete a nuestro servidor</a></li>
            </ul>

            <footer style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee;">
                <p>🤖 Powered by OpenManus AI | ⚡ Hosted on Vercel | 🔄 Orchestrated by Make.com</p>
            </footer>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Maneja peticiones OPTIONS para CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

