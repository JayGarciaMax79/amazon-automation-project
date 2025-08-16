# Integración de OpenManus con la Automatización de Artículos Amazon

## 1. Análisis del Repositorio OpenManus

### Información del Repositorio
- **URL Principal:** https://github.com/FoundationAgents/OpenManus
- **Descripción:** Framework open-source para construir agentes de IA generales
- **Lenguaje:** Python 100%
- **Estrellas:** 49k
- **Forks:** 8.6k
- **Estado:** Activo y en desarrollo

### Características Principales de OpenManus
1. **Agente de IA General:** Capaz de realizar múltiples tareas
2. **Automatización de Navegador:** Integración con Playwright
3. **Análisis de Datos:** Agente especializado en análisis y visualización
4. **Configuración Flexible:** Soporte para múltiples modelos LLM
5. **Arquitectura Modular:** Fácil extensión y personalización

## 2. Integración Estratégica con la Automatización

### 2.1 Uso de OpenManus como Motor de IA
OpenManus puede servir como el cerebro principal de nuestra automatización, proporcionando:

- **Generación de Artículos Inteligente:** Usar el agente para crear contenido de alta calidad
- **Análisis de Productos:** Procesamiento inteligente de datos extraídos de Amazon
- **Optimización SEO:** Generación de contenido optimizado para motores de búsqueda
- **Personalización:** Adaptación del estilo de escritura según el producto

### 2.2 Arquitectura Integrada

```
Google Sheets (Trigger) 
    ↓
Make.com (Orquestador)
    ↓
OpenManus Agent (Procesamiento IA)
    ↓
GitHub (Almacenamiento)
    ↓
WordPress (Publicación)
```

## 3. Implementación Técnica

### 3.1 Configuración de OpenManus

#### Archivo de Configuración (`config/config.toml`)
```toml
# Configuración global LLM
[llm]
model = "gpt-4o"
base_url = "https://api.openai.com/v1"
api_key = "sk-..."  # Tu API key de OpenAI
max_tokens = 4096
temperature = 0.7  # Más creatividad para artículos

# Configuración para análisis de datos
[runflow]
use_data_analysis_agent = true

# Configuración específica para Amazon
[amazon]
scraping_delay = 2
max_retries = 3
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
]
```

### 3.2 Script de Integración

#### `amazon_article_agent.py`
```python
import asyncio
from app.core.agent import Agent
from app.core.llm import LLMConfig
from app.tools.browser import BrowserTool
import json

class AmazonArticleAgent:
    def __init__(self, config_path="config/config.toml"):
        self.agent = Agent(config_path=config_path)
        self.browser_tool = BrowserTool()
    
    async def process_amazon_product(self, product_url, affiliate_link):
        """
        Procesa un producto de Amazon y genera un artículo completo
        """
        try:
            # Paso 1: Extraer datos del producto
            product_data = await self.extract_product_data(product_url)
            
            # Paso 2: Generar artículo con IA
            article_content = await self.generate_article(product_data, affiliate_link)
            
            # Paso 3: Optimizar para SEO
            optimized_article = await self.optimize_seo(article_content, product_data)
            
            return {
                "success": True,
                "product_data": product_data,
                "article": optimized_article,
                "affiliate_link": affiliate_link
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def extract_product_data(self, url):
        """Extrae datos del producto usando OpenManus"""
        prompt = f"""
        Navega a la URL {url} y extrae la siguiente información del producto de Amazon:
        1. Título del producto
        2. Precio actual
        3. Descripción detallada
        4. Características principales
        5. Calificación y número de reseñas
        6. Imágenes del producto
        7. Categoría del producto
        8. Disponibilidad
        
        Devuelve la información en formato JSON estructurado.
        """
        
        result = await self.agent.run(prompt)
        return json.loads(result)
    
    async def generate_article(self, product_data, affiliate_link):
        """Genera artículo usando OpenManus"""
        prompt = f"""
        Crea un artículo de blog completo y atractivo sobre el siguiente producto:
        
        Datos del producto: {json.dumps(product_data, indent=2)}
        Enlace de afiliado: {affiliate_link}
        
        El artículo debe incluir:
        1. Título llamativo y optimizado para SEO
        2. Introducción enganchante
        3. Análisis detallado del producto
        4. Pros y contras
        5. Comparación con productos similares
        6. Conclusión con llamada a la acción
        7. Integración natural del enlace de afiliado
        
        Estilo: Profesional pero accesible, orientado a la conversión
        Longitud: 1500-2000 palabras
        Formato: HTML con estructura semántica
        """
        
        article = await self.agent.run(prompt)
        return article
    
    async def optimize_seo(self, article, product_data):
        """Optimiza el artículo para SEO"""
        prompt = f"""
        Optimiza el siguiente artículo para SEO:
        
        Artículo: {article}
        Producto: {product_data.get('title', '')}
        
        Optimizaciones requeridas:
        1. Meta título (máx 60 caracteres)
        2. Meta descripción (máx 160 caracteres)
        3. Palabras clave principales y secundarias
        4. Estructura de encabezados (H1, H2, H3)
        5. Alt text para imágenes
        6. Schema markup para productos
        7. Enlaces internos sugeridos
        
        Devuelve el artículo optimizado con metadatos SEO.
        """
        
        optimized = await self.agent.run(prompt)
        return optimized
```

### 3.3 API Endpoint para Make.com

#### `api/openmanus_endpoint.py`
```python
from flask import Flask, request, jsonify
from amazon_article_agent import AmazonArticleAgent
import asyncio

app = Flask(__name__)
agent = AmazonArticleAgent()

@app.route('/api/process-amazon-product', methods=['POST'])
def process_amazon_product():
    """
    Endpoint para procesar productos de Amazon con OpenManus
    """
    try:
        data = request.get_json()
        
        if not data or 'product_url' not in data or 'affiliate_link' not in data:
            return jsonify({
                'success': False,
                'error': 'product_url y affiliate_link son requeridos'
            }), 400
        
        # Ejecutar procesamiento asíncrono
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(
            agent.process_amazon_product(
                data['product_url'],
                data['affiliate_link']
            )
        )
        
        loop.close()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'OpenManus Amazon Article Generator',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## 4. Configuración en Make.com

### 4.1 Escenario de Make.com

1. **Trigger:** Google Sheets - Watch Rows
   - Detecta nuevas filas con product_url y affiliate_link

2. **HTTP Request:** Llamada a OpenManus API
   - URL: `https://tu-servidor.com/api/process-amazon-product`
   - Método: POST
   - Body: `{"product_url": "{{product_url}}", "affiliate_link": "{{affiliate_link}}"}`

3. **WordPress:** Create Post
   - Título: `{{article.title}}`
   - Contenido: `{{article.content}}`
   - Estado: Publicado

4. **Google Sheets:** Update Row
   - Estado: "Completado"
   - URL del artículo: `{{wordpress.post_url}}`

### 4.2 Configuración JSON para Make.com

```json
{
  "name": "Amazon Article Automation with OpenManus",
  "flow": [
    {
      "id": 1,
      "module": "google-sheets:watchRows",
      "parameters": {
        "spreadsheetId": "TU_SPREADSHEET_ID",
        "sheetName": "Amazon_Products",
        "hasHeaders": true
      }
    },
    {
      "id": 2,
      "module": "http:makeARequest",
      "parameters": {
        "url": "https://tu-endpoint.vercel.app/api/process-amazon-product",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "product_url": "{{1.product_url}}",
          "affiliate_link": "{{1.affiliate_link}}"
        }
      }
    },
    {
      "id": 3,
      "module": "wordpress:createPost",
      "parameters": {
        "title": "{{2.article.title}}",
        "content": "{{2.article.content}}",
        "status": "publish"
      }
    },
    {
      "id": 4,
      "module": "google-sheets:updateRow",
      "parameters": {
        "spreadsheetId": "TU_SPREADSHEET_ID",
        "range": "A{{1.__IMTINDEX__}}:J{{1.__IMTINDEX__}}",
        "values": [
          [
            "{{1.timestamp}}",
            "{{1.product_url}}",
            "{{1.affiliate_link}}",
            "Completado",
            "{{2.article.title}}",
            "{{3.post_url}}",
            "Artículo generado con OpenManus",
            "{{2.product_data.title}}",
            "{{2.product_data.price}}",
            "{{2.product_data.rating}}"
          ]
        ]
      }
    }
  ]
}
```

## 5. Ventajas de Usar OpenManus

### 5.1 Capacidades Avanzadas
- **Navegación Inteligente:** Puede navegar sitios web complejos
- **Análisis Contextual:** Comprende el contexto del producto
- **Generación de Contenido:** Crea artículos de alta calidad
- **Adaptabilidad:** Se ajusta a diferentes tipos de productos

### 5.2 Escalabilidad
- **Procesamiento Paralelo:** Puede manejar múltiples productos simultáneamente
- **Configuración Flexible:** Fácil ajuste de parámetros
- **Extensibilidad:** Posibilidad de agregar nuevas funcionalidades

### 5.3 Calidad del Contenido
- **SEO Optimizado:** Genera contenido optimizado para buscadores
- **Estilo Consistente:** Mantiene un estilo de escritura coherente
- **Llamadas a la Acción:** Incluye CTAs efectivos para conversión

## 6. Implementación Paso a Paso

### Paso 1: Configurar OpenManus
1. Clonar el repositorio de FoundationAgents/OpenManus
2. Configurar las API keys en config.toml
3. Instalar dependencias con uv o conda

### Paso 2: Desarrollar el Agente Personalizado
1. Crear amazon_article_agent.py
2. Implementar métodos de extracción y generación
3. Probar con productos de ejemplo

### Paso 3: Crear API Endpoint
1. Desarrollar Flask API
2. Desplegar en Vercel/Netlify
3. Configurar variables de entorno

### Paso 4: Configurar Make.com
1. Crear nuevo escenario
2. Configurar trigger de Google Sheets
3. Conectar con API de OpenManus
4. Configurar publicación en WordPress

### Paso 5: Pruebas y Optimización
1. Probar con productos reales
2. Optimizar prompts para mejor calidad
3. Ajustar configuraciones según resultados

Esta integración con OpenManus proporcionará una automatización de alta calidad que puede generar artículos profesionales y optimizados para SEO de manera completamente automática.

