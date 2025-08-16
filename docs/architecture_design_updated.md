# Arquitectura de Automatización de Artículos de Amazon (Sin VPS)

## 1. Introducción

Esta arquitectura ha sido rediseñada para funcionar completamente en la nube sin necesidad de un servidor VPS propio. Utilizaremos servicios gratuitos y herramientas accesibles para crear una automatización robusta y escalable.

## 2. Componentes Principales (Actualizados)

### 2.1 Google Sheets (Trigger y Base de Datos)
- **Función:** Punto de entrada de datos y disparador principal
- **Contenido:** URL del producto Amazon, enlace de afiliado, estado del procesamiento
- **Integración:** Conectado directamente con Make.com

### 2.2 Make.com (Integromat) - Orquestador Central
- **Función:** Coordina todo el flujo de trabajo
- **Capacidades:**
  - Detecta nuevas filas en Google Sheets
  - Ejecuta scraping de Amazon mediante módulos HTTP
  - Genera artículos usando APIs de IA
  - Publica contenido en WordPress

### 2.3 GitHub Repository
- **Función:** Almacenamiento de código y control de versiones
- **Contenido:**
  - Scripts de Python para scraping
  - Templates de artículos
  - Configuraciones de Make.com
  - Documentación

### 2.4 GitHub Actions (Procesamiento)
- **Función:** Ejecutar scripts de Python en la nube
- **Capacidades:**
  - Scraping de productos Amazon
  - Generación de artículos con IA
  - Procesamiento de imágenes
  - Webhooks para Make.com

### 2.5 Vercel/Netlify (API Endpoints)
- **Función:** Hosting de funciones serverless
- **Endpoints:**
  - `/api/scrape-amazon` - Extracción de datos
  - `/api/generate-article` - Generación de artículos
  - `/api/webhook` - Recepción de webhooks

### 2.6 WordPress.com o Sitio Web Gratuito
- **Función:** Publicación de artículos
- **Alternativas:**
  - WordPress.com (plan gratuito)
  - GitHub Pages + Jekyll
  - Netlify + CMS headless

## 3. Flujo de Trabajo Actualizado

### Paso 1: Entrada de Datos
- Usuario ingresa URL de producto Amazon y enlace de afiliado en Google Sheets
- Google Sheets notifica a Make.com mediante webhook

### Paso 2: Procesamiento en Make.com
- Make.com detecta nueva fila
- Llama a función serverless para extraer datos del producto
- Procesa datos y genera artículo usando IA
- Formatea contenido para publicación

### Paso 3: Publicación
- Make.com publica artículo en WordPress usando API REST
- Actualiza Google Sheets con estado "Publicado"
- Opcionalmente envía notificación de éxito

## 4. Tecnologías y Servicios Gratuitos

### 4.1 Servicios de Hosting
- **Vercel:** Funciones serverless gratuitas (100GB bandwidth/mes)
- **Netlify:** Funciones serverless + hosting estático
- **GitHub Pages:** Hosting estático gratuito

### 4.2 Procesamiento
- **GitHub Actions:** 2000 minutos gratuitos/mes
- **Make.com:** 1000 operaciones gratuitas/mes
- **Google Sheets API:** Gratuito hasta ciertos límites

### 4.3 IA y APIs
- **OpenAI API:** Créditos gratuitos iniciales
- **Hugging Face:** Modelos gratuitos
- **Google Gemini:** API gratuita con límites

### 4.4 Base de Datos
- **Google Sheets:** Como base de datos simple
- **Airtable:** Alternativa con API robusta
- **Supabase:** PostgreSQL gratuito

## 5. Implementación Paso a Paso

### Fase 1: Configuración de Repositorio GitHub
1. Crear repositorio con estructura de proyecto
2. Configurar GitHub Actions para CI/CD
3. Crear scripts de scraping de Amazon
4. Implementar generador de artículos con IA

### Fase 2: Despliegue de Funciones Serverless
1. Configurar Vercel/Netlify
2. Desplegar endpoints API
3. Configurar variables de entorno
4. Probar funciones individualmente

### Fase 3: Configuración de Make.com
1. Crear cuenta en Make.com
2. Configurar conexión con Google Sheets
3. Crear escenario de automatización
4. Configurar webhooks y llamadas API

### Fase 4: Configuración de WordPress
1. Crear sitio en WordPress.com o alternativa
2. Configurar API REST
3. Crear templates de artículos
4. Configurar SEO básico

### Fase 5: Integración y Pruebas
1. Conectar todos los componentes
2. Realizar pruebas end-to-end
3. Optimizar rendimiento
4. Documentar proceso

## 6. Ventajas de Esta Arquitectura

### 6.1 Costo
- **100% Gratuito** dentro de los límites de uso
- Sin costos de servidor o mantenimiento
- Escalable según necesidades

### 6.2 Mantenimiento
- **Mínimo mantenimiento** requerido
- Actualizaciones automáticas de plataforma
- Monitoreo integrado

### 6.3 Escalabilidad
- **Escalado automático** según demanda
- Sin límites de infraestructura
- Fácil expansión de funcionalidades

### 6.4 Confiabilidad
- **Alta disponibilidad** de servicios cloud
- Respaldos automáticos
- Recuperación ante fallos

## 7. Limitaciones y Consideraciones

### 7.1 Límites de Servicios Gratuitos
- Make.com: 1000 operaciones/mes
- Vercel: 100GB bandwidth/mes
- GitHub Actions: 2000 minutos/mes

### 7.2 Scraping de Amazon
- Posibles bloqueos por detección anti-bot
- Necesidad de rotar User-Agents y proxies
- Cumplimiento de términos de servicio

### 7.3 Calidad de Contenido
- Dependiente de la calidad del modelo de IA
- Necesidad de revisión manual ocasional
- Optimización continua de prompts

## 8. Plan de Implementación

Esta arquitectura se implementará en las siguientes fases del proyecto, priorizando la funcionalidad core y expandiendo gradualmente las capacidades avanzadas.

