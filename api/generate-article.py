"""
Generador de Artículos de Amazon usando OpenManus
Integra OpenManus para crear artículos de alta calidad sobre productos de Amazon
"""

import asyncio
import json
import os
import sys
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Agregar el path de OpenManus
sys.path.append('/home/ubuntu/OpenManus')

from app.core.agent import Agent
from app.core.llm import LLMConfig
from app.tools.browser import BrowserTool

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmazonArticleGenerator:
    """
    Generador de artículos de Amazon usando OpenManus como motor de IA
    """
    
    def __init__(self, config_path: str = "/home/ubuntu/OpenManus/config/config.toml"):
        """
        Inicializa el generador de artículos
        
        Args:
            config_path: Ruta al archivo de configuración de OpenManus
        """
        self.config_path = config_path
        self.agent = None
        self.browser_tool = None
        
        # Templates de artículos por categoría
        self.article_templates = {
            "electronics": self._get_electronics_template(),
            "home": self._get_home_template(),
            "fashion": self._get_fashion_template(),
            "books": self._get_books_template(),
            "default": self._get_default_template()
        }
        
        # Palabras clave SEO por categoría
        self.seo_keywords = {
            "electronics": ["mejor", "análisis", "review", "comparación", "precio", "características"],
            "home": ["hogar", "casa", "decoración", "funcional", "calidad", "diseño"],
            "fashion": ["moda", "estilo", "tendencia", "outfit", "look", "temporada"],
            "books": ["libro", "lectura", "autor", "reseña", "recomendación", "género"],
            "default": ["producto", "calidad", "precio", "comprar", "mejor", "análisis"]
        }
    
    async def initialize(self):
        """Inicializa el agente de OpenManus"""
        try:
            self.agent = Agent(config_path=self.config_path)
            self.browser_tool = BrowserTool()
            logger.info("OpenManus Agent inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar OpenManus Agent: {e}")
            raise
    
    async def generate_article(self, product_url: str, affiliate_link: str) -> Dict[str, Any]:
        """
        Genera un artículo completo sobre un producto de Amazon
        
        Args:
            product_url: URL del producto de Amazon
            affiliate_link: Enlace de afiliado
            
        Returns:
            Dict con el artículo generado y metadatos
        """
        try:
            logger.info(f"Iniciando generación de artículo para: {product_url}")
            
            # Paso 1: Extraer datos del producto
            product_data = await self._extract_product_data(product_url)
            
            # Paso 2: Determinar categoría del producto
            category = await self._determine_category(product_data)
            
            # Paso 3: Generar contenido del artículo
            article_content = await self._generate_article_content(
                product_data, affiliate_link, category
            )
            
            # Paso 4: Optimizar para SEO
            seo_optimized = await self._optimize_for_seo(article_content, product_data, category)
            
            # Paso 5: Generar metadatos
            metadata = await self._generate_metadata(product_data, category)
            
            result = {
                "success": True,
                "article": {
                    "title": seo_optimized.get("title", ""),
                    "content": seo_optimized.get("content", ""),
                    "meta_description": seo_optimized.get("meta_description", ""),
                    "keywords": seo_optimized.get("keywords", []),
                    "category": category,
                    "word_count": len(seo_optimized.get("content", "").split())
                },
                "product_data": product_data,
                "metadata": metadata,
                "affiliate_link": affiliate_link,
                "generated_at": datetime.now().isoformat()
            }
            
            logger.info("Artículo generado exitosamente")
            return result
            
        except Exception as e:
            logger.error(f"Error al generar artículo: {e}")
            return {
                "success": False,
                "error": str(e),
                "product_url": product_url,
                "affiliate_link": affiliate_link
            }
    
    async def _extract_product_data(self, product_url: str) -> Dict[str, Any]:
        """Extrae datos del producto usando OpenManus"""
        
        extraction_prompt = f"""
        Necesito que extraigas información detallada de un producto de Amazon.
        
        URL del producto: {product_url}
        
        Por favor, navega a esta URL y extrae la siguiente información:
        
        1. Título completo del producto
        2. Precio actual (si está disponible)
        3. Precio original (si hay descuento)
        4. Descripción del producto
        5. Características principales (bullet points)
        6. Calificación promedio (estrellas)
        7. Número total de reseñas
        8. Disponibilidad del producto
        9. Marca del producto
        10. Categoría principal
        11. URLs de las imágenes principales (máximo 3)
        12. ASIN del producto
        13. Dimensiones (si están disponibles)
        14. Peso (si está disponible)
        15. Información del vendedor
        
        IMPORTANTE: Devuelve la información en formato JSON válido con la siguiente estructura:
        {{
            "title": "título del producto",
            "current_price": "precio actual",
            "original_price": "precio original",
            "description": "descripción detallada",
            "features": ["característica 1", "característica 2", ...],
            "rating": "calificación",
            "review_count": "número de reseñas",
            "availability": "disponibilidad",
            "brand": "marca",
            "category": "categoría",
            "images": ["url1", "url2", "url3"],
            "asin": "ASIN",
            "dimensions": "dimensiones",
            "weight": "peso",
            "seller": "información del vendedor"
        }}
        
        Si algún dato no está disponible, usa "No disponible" como valor.
        """
        
        try:
            result = await self.agent.run(extraction_prompt)
            
            # Intentar parsear como JSON
            try:
                product_data = json.loads(result)
            except json.JSONDecodeError:
                # Si no es JSON válido, extraer información manualmente
                product_data = self._parse_extraction_result(result)
            
            return product_data
            
        except Exception as e:
            logger.error(f"Error al extraer datos del producto: {e}")
            return {
                "title": "Producto de Amazon",
                "current_price": "No disponible",
                "description": "Descripción no disponible",
                "features": [],
                "rating": "No disponible",
                "review_count": "0",
                "availability": "No disponible",
                "brand": "No disponible",
                "category": "General",
                "images": [],
                "asin": "No disponible"
            }
    
    async def _determine_category(self, product_data: Dict[str, Any]) -> str:
        """Determina la categoría del producto para usar el template apropiado"""
        
        category_prompt = f"""
        Basándote en la siguiente información del producto, determina su categoría principal:
        
        Título: {product_data.get('title', '')}
        Descripción: {product_data.get('description', '')}
        Categoría Amazon: {product_data.get('category', '')}
        Marca: {product_data.get('brand', '')}
        
        Categorías disponibles:
        - electronics (electrónicos, gadgets, tecnología)
        - home (hogar, casa, decoración, cocina)
        - fashion (ropa, accesorios, moda)
        - books (libros, ebooks)
        - default (otros productos)
        
        Responde ÚNICAMENTE con el nombre de la categoría (electronics, home, fashion, books, o default).
        """
        
        try:
            result = await self.agent.run(category_prompt)
            category = result.strip().lower()
            
            if category in self.article_templates:
                return category
            else:
                return "default"
                
        except Exception as e:
            logger.error(f"Error al determinar categoría: {e}")
            return "default"
    
    async def _generate_article_content(self, product_data: Dict[str, Any], 
                                      affiliate_link: str, category: str) -> str:
        """Genera el contenido del artículo usando el template apropiado"""
        
        template = self.article_templates.get(category, self.article_templates["default"])
        
        content_prompt = f"""
        Crea un artículo de blog completo y atractivo sobre el siguiente producto de Amazon.
        
        INFORMACIÓN DEL PRODUCTO:
        {json.dumps(product_data, indent=2, ensure_ascii=False)}
        
        ENLACE DE AFILIADO: {affiliate_link}
        
        TEMPLATE A SEGUIR:
        {template}
        
        INSTRUCCIONES ESPECÍFICAS:
        1. El artículo debe tener entre 1500-2000 palabras
        2. Usa un tono profesional pero accesible
        3. Incluye el enlace de afiliado de forma natural (mínimo 3 veces)
        4. Crea títulos y subtítulos atractivos
        5. Incluye pros y contras del producto
        6. Añade una llamada a la acción convincente
        7. Usa formato HTML semántico
        8. Incluye comparaciones con productos similares si es relevante
        9. Optimiza para SEO con palabras clave naturales
        10. Mantén un enfoque honesto y útil para el lector
        
        ESTRUCTURA REQUERIDA:
        - Título principal (H1)
        - Introducción enganchante
        - Sección de características principales
        - Análisis detallado
        - Pros y contras
        - Comparación (si aplica)
        - Conclusión con CTA
        
        Genera el artículo completo en HTML.
        """
        
        try:
            article_content = await self.agent.run(content_prompt)
            return article_content
            
        except Exception as e:
            logger.error(f"Error al generar contenido del artículo: {e}")
            return self._generate_fallback_article(product_data, affiliate_link)
    
    async def _optimize_for_seo(self, content: str, product_data: Dict[str, Any], 
                              category: str) -> Dict[str, Any]:
        """Optimiza el artículo para SEO"""
        
        keywords = self.seo_keywords.get(category, self.seo_keywords["default"])
        
        seo_prompt = f"""
        Optimiza el siguiente artículo para SEO:
        
        CONTENIDO ACTUAL:
        {content}
        
        INFORMACIÓN DEL PRODUCTO:
        Título: {product_data.get('title', '')}
        Categoría: {category}
        
        PALABRAS CLAVE OBJETIVO: {', '.join(keywords)}
        
        TAREAS DE OPTIMIZACIÓN:
        1. Crear un meta título optimizado (máximo 60 caracteres)
        2. Crear una meta descripción atractiva (máximo 160 caracteres)
        3. Identificar palabras clave principales y secundarias
        4. Optimizar los encabezados (H1, H2, H3)
        5. Añadir alt text para imágenes
        6. Mejorar la densidad de palabras clave (2-3%)
        7. Crear enlaces internos sugeridos
        8. Optimizar la estructura del contenido
        
        FORMATO DE RESPUESTA (JSON):
        {{
            "title": "título optimizado para SEO",
            "meta_description": "descripción meta optimizada",
            "keywords": ["palabra1", "palabra2", "palabra3"],
            "content": "contenido HTML optimizado",
            "alt_texts": ["alt text 1", "alt text 2"],
            "internal_links": ["enlace sugerido 1", "enlace sugerido 2"],
            "seo_score": "puntuación estimada del 1-10"
        }}
        """
        
        try:
            result = await self.agent.run(seo_prompt)
            
            try:
                seo_data = json.loads(result)
            except json.JSONDecodeError:
                # Fallback si no es JSON válido
                seo_data = {
                    "title": product_data.get('title', 'Producto Amazon')[:60],
                    "meta_description": f"Análisis completo de {product_data.get('title', 'este producto')}. Características, precio y opiniones."[:160],
                    "keywords": keywords[:5],
                    "content": content,
                    "seo_score": "7"
                }
            
            return seo_data
            
        except Exception as e:
            logger.error(f"Error al optimizar SEO: {e}")
            return {
                "title": product_data.get('title', 'Producto Amazon')[:60],
                "meta_description": f"Análisis de {product_data.get('title', 'producto')}",
                "keywords": keywords[:5],
                "content": content,
                "seo_score": "6"
            }
    
    async def _generate_metadata(self, product_data: Dict[str, Any], category: str) -> Dict[str, Any]:
        """Genera metadatos adicionales para el artículo"""
        
        return {
            "estimated_read_time": self._calculate_read_time(product_data.get('title', '')),
            "target_audience": self._get_target_audience(category),
            "content_type": "product_review",
            "language": "es",
            "region": "global",
            "update_frequency": "monthly",
            "monetization": "affiliate",
            "quality_score": self._calculate_quality_score(product_data)
        }
    
    def _get_electronics_template(self) -> str:
        """Template para productos electrónicos"""
        return """
        # [TÍTULO DEL PRODUCTO]: Análisis Completo y Mejor Precio 2025
        
        ## Introducción
        - Presentación del producto
        - Por qué es relevante
        - Qué encontrarás en este análisis
        
        ## Características Principales
        - Especificaciones técnicas
        - Funcionalidades destacadas
        - Innovaciones tecnológicas
        
        ## Análisis Detallado
        - Rendimiento
        - Calidad de construcción
        - Facilidad de uso
        - Compatibilidad
        
        ## Pros y Contras
        ### Ventajas
        ### Desventajas
        
        ## Comparación con Competidores
        - Productos similares
        - Diferencias clave
        - Relación calidad-precio
        
        ## Conclusión y Recomendación
        - Veredicto final
        - Para quién es ideal
        - Llamada a la acción
        """
    
    def _get_home_template(self) -> str:
        """Template para productos del hogar"""
        return """
        # [TÍTULO DEL PRODUCTO]: La Mejor Opción para tu Hogar
        
        ## Introducción
        - Presentación del producto
        - Beneficios para el hogar
        - Por qué considerarlo
        
        ## Diseño y Calidad
        - Materiales utilizados
        - Acabados y estética
        - Durabilidad
        
        ## Funcionalidad
        - Uso práctico
        - Facilidad de instalación/uso
        - Mantenimiento
        
        ## Pros y Contras
        ### Lo que nos gusta
        ### Aspectos a mejorar
        
        ## Opiniones de Usuarios
        - Experiencias reales
        - Puntos comunes
        - Satisfacción general
        
        ## Conclusión
        - Recomendación final
        - Mejor uso
        - Dónde comprarlo
        """
    
    def _get_fashion_template(self) -> str:
        """Template para productos de moda"""
        return """
        # [TÍTULO DEL PRODUCTO]: Estilo y Calidad en un Solo Producto
        
        ## Introducción
        - Presentación del producto
        - Tendencia actual
        - Por qué destacar
        
        ## Diseño y Estilo
        - Características visuales
        - Versatilidad
        - Ocasiones de uso
        
        ## Calidad y Materiales
        - Tejidos/materiales
        - Confección
        - Durabilidad
        
        ## Tallas y Ajuste
        - Guía de tallas
        - Consejos de ajuste
        - Comentarios de usuarios
        
        ## Pros y Contras
        ### Puntos fuertes
        ### Aspectos a considerar
        
        ## Cómo Combinar
        - Sugerencias de outfits
        - Accesorios complementarios
        - Versatilidad
        
        ## Conclusión
        - Recomendación final
        - Mejor ocasión de uso
        - Dónde adquirirlo
        """
    
    def _get_books_template(self) -> str:
        """Template para libros"""
        return """
        # [TÍTULO DEL LIBRO]: Reseña Completa y Opinión Personal
        
        ## Introducción
        - Presentación del libro
        - Autor y contexto
        - Por qué leerlo
        
        ## Sinopsis (Sin Spoilers)
        - Tema principal
        - Género y estilo
        - Público objetivo
        
        ## Análisis del Contenido
        - Calidad de la escritura
        - Desarrollo de personajes/temas
        - Estructura narrativa
        
        ## Pros y Contras
        ### Lo que más me gustó
        ### Aspectos mejorables
        
        ## Comparación con Otros Libros
        - Libros similares
        - Diferencias clave
        - Lugar en el género
        
        ## Conclusión y Recomendación
        - Veredicto final
        - Para qué tipo de lector
        - Dónde conseguirlo
        """
    
    def _get_default_template(self) -> str:
        """Template por defecto para cualquier producto"""
        return """
        # [TÍTULO DEL PRODUCTO]: Análisis Completo y Honest Review
        
        ## Introducción
        - Presentación del producto
        - Contexto y relevancia
        - Qué esperar de esta reseña
        
        ## Características Principales
        - Especificaciones clave
        - Funcionalidades destacadas
        - Valor agregado
        
        ## Experiencia de Uso
        - Facilidad de uso
        - Rendimiento
        - Calidad general
        
        ## Pros y Contras
        ### Ventajas principales
        ### Desventajas a considerar
        
        ## Relación Calidad-Precio
        - Análisis del precio
        - Comparación con alternativas
        - Valor por dinero
        
        ## Conclusión
        - Recomendación final
        - Para quién es ideal
        - Dónde comprarlo al mejor precio
        """
    
    def _parse_extraction_result(self, result: str) -> Dict[str, Any]:
        """Parsea el resultado de extracción si no es JSON válido"""
        # Implementación básica de parsing
        return {
            "title": "Producto extraído",
            "current_price": "No disponible",
            "description": result[:500] if result else "No disponible",
            "features": [],
            "rating": "No disponible",
            "review_count": "0",
            "availability": "No disponible",
            "brand": "No disponible",
            "category": "General",
            "images": [],
            "asin": "No disponible"
        }
    
    def _generate_fallback_article(self, product_data: Dict[str, Any], affiliate_link: str) -> str:
        """Genera un artículo básico como fallback"""
        title = product_data.get('title', 'Producto de Amazon')
        
        return f"""
        <h1>{title}: Análisis y Opinión</h1>
        
        <p>En este artículo analizamos en detalle el <strong>{title}</strong>, 
        un producto que ha captado nuestra atención por sus características únicas.</p>
        
        <h2>Características Principales</h2>
        <p>Este producto destaca por su calidad y funcionalidad. 
        A continuación, te contamos todo lo que necesitas saber.</p>
        
        <h2>Nuestra Opinión</h2>
        <p>Después de analizar este producto, consideramos que es una excelente opción 
        para quienes buscan calidad y buen precio.</p>
        
        <h2>Conclusión</h2>
        <p>Si estás interesado en este producto, puedes encontrarlo al mejor precio 
        <a href="{affiliate_link}" target="_blank" rel="nofollow">aquí</a>.</p>
        """
    
    def _calculate_read_time(self, content: str) -> int:
        """Calcula el tiempo estimado de lectura en minutos"""
        words = len(content.split())
        return max(1, words // 200)  # 200 palabras por minuto
    
    def _get_target_audience(self, category: str) -> str:
        """Determina la audiencia objetivo según la categoría"""
        audiences = {
            "electronics": "Entusiastas de la tecnología, profesionales",
            "home": "Propietarios de viviendas, decoradores",
            "fashion": "Amantes de la moda, compradores conscientes del estilo",
            "books": "Lectores, estudiantes, profesionales",
            "default": "Consumidores generales"
        }
        return audiences.get(category, audiences["default"])
    
    def _calculate_quality_score(self, product_data: Dict[str, Any]) -> int:
        """Calcula una puntuación de calidad del producto"""
        score = 5  # Base score
        
        if product_data.get('rating') and product_data['rating'] != "No disponible":
            try:
                rating = float(product_data['rating'].split()[0])
                score += int(rating)
            except:
                pass
        
        if product_data.get('review_count') and product_data['review_count'] != "0":
            try:
                reviews = int(product_data['review_count'].replace(',', ''))
                if reviews > 100:
                    score += 1
                if reviews > 1000:
                    score += 1
            except:
                pass
        
        return min(10, score)

# Función principal para uso como API
async def generate_amazon_article(product_url: str, affiliate_link: str) -> Dict[str, Any]:
    """
    Función principal para generar artículos de Amazon
    
    Args:
        product_url: URL del producto de Amazon
        affiliate_link: Enlace de afiliado
        
    Returns:
        Dict con el artículo generado
    """
    generator = AmazonArticleGenerator()
    await generator.initialize()
    return await generator.generate_article(product_url, affiliate_link)

# Para testing
if __name__ == "__main__":
    async def test():
        # URL de ejemplo para testing
        test_url = "https://www.amazon.com/dp/B08N5WRWNW"
        test_affiliate = "https://amzn.to/3xyz123"
        
        result = await generate_amazon_article(test_url, test_affiliate)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    asyncio.run(test())

