# 🆓 Guía Completa: Automatización Amazon 100% GRATUITA

## 🎯 Resumen Ejecutivo

Esta guía te permitirá crear una automatización completa para generar artículos de productos Amazon **sin gastar un solo centavo**. Utilizaremos únicamente servicios gratuitos y APIs sin costo.

### 💰 Costo Total: $0.00

| Servicio | Plan | Costo | Límites |
|----------|------|-------|---------|
| Google Sheets | Gratis | $0 | Ilimitado |
| Google Apps Script | Gratis | $0 | 6 min/ejecución |
| Make.com | Gratis | $0 | 1000 operaciones/mes |
| Vercel | Gratis | $0 | 100GB bandwidth |
| GitHub | Gratis | $0 | Repos públicos ilimitados |
| Google Gemini API | Gratis | $0 | 15 requests/minuto |
| Hugging Face | Gratis | $0 | Con límites de rate |
| WordPress.com | Gratis | $0 | Con subdomain |

**Resultado:** ~100 artículos/mes completamente gratis

## 🚀 Configuración Paso a Paso

### PASO 1: Configurar Google Gemini API (Gratis)

#### 1.1. Obtener API Key Gratuita

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Inicia sesión con tu cuenta Google
3. Haz clic en **"Create API Key"**
4. Copia tu API key (empieza con `AIza...`)
5. **Límites gratuitos:** 15 requests/minuto, 1500/día

#### 1.2. Probar la API

```bash
curl -X POST \
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=TU_API_KEY' \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [{
      "parts": [{"text": "Escribe un párrafo sobre un iPhone"}]
    }]
  }'
```

### PASO 2: Configurar Hugging Face (Backup Gratuito)

#### 2.1. Crear Cuenta Gratuita

1. Ve a [huggingface.co](https://huggingface.co)
2. Regístrate gratis
3. Ve a **Settings > Access Tokens**
4. Crea un nuevo token: **"Read"** permissions
5. Copia el token (empieza con `hf_...`)

#### 2.2. Probar la API

```bash
curl -X POST \
  'https://api-inference.huggingface.co/models/microsoft/DialoGPT-large' \
  -H 'Authorization: Bearer TU_HF_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{"inputs": "Escribe sobre un producto Amazon"}'
```

### PASO 3: Configurar WordPress.com Gratuito

#### 3.1. Crear Blog Gratuito

1. Ve a [wordpress.com](https://wordpress.com)
2. Haz clic en **"Start your website"**
3. Elige **"Start with a free site"**
4. Dominio: `tudominio.wordpress.com` (gratis)
5. Tema: Cualquier tema responsive

#### 3.2. Configurar API REST

1. En tu dashboard de WordPress, ve a **Users > Profile**
2. Scroll hasta **"Application Passwords"**
3. Nombre: "Amazon Automation"
4. Haz clic en **"Add New Application Password"**
5. Copia la contraseña generada

#### 3.3. Probar WordPress API

```bash
curl -X POST \
  'https://tudominio.wordpress.com/wp-json/wp/v2/posts' \
  -H 'Content-Type: application/json' \
  -u 'tu-usuario:tu-app-password' \
  -d '{
    "title": "Test Post",
    "content": "Contenido de prueba",
    "status": "publish"
  }'
```

### PASO 4: Configurar GitHub (Gratis)

#### 4.1. Crear Repositorio

1. Ve a [github.com](https://github.com)
2. Haz clic en **"New repository"**
3. Nombre: `amazon-automation-free`
4. Descripción: `Automatización gratuita de artículos Amazon`
5. **Public** (para plan gratuito)
6. Inicializar con README

#### 4.2. Clonar y Configurar

```bash
git clone https://github.com/tu-usuario/amazon-automation-free.git
cd amazon-automation-free

# Copiar archivos del proyecto
cp -r /ruta/amazon-automation-project/* .

# Configurar git
git config user.name "Tu Nombre"
git config user.email "tu-email@gmail.com"

# Primer commit
git add .
git commit -m "Initial setup - Free Amazon automation"
git push origin main
```

### PASO 5: Configurar Vercel (Gratis)

#### 5.1. Conectar con GitHub

1. Ve a [vercel.com](https://vercel.com)
2. Regístrate con tu cuenta GitHub
3. Haz clic en **"New Project"**
4. Selecciona tu repositorio `amazon-automation-free`
5. Framework: **"Other"**
6. Haz clic en **"Deploy"**

#### 5.2. Configurar Variables de Entorno

En el dashboard de Vercel:

1. Ve a **Settings > Environment Variables**
2. Agrega las siguientes variables:

```
GOOGLE_GEMINI_API_KEY=AIza...tu-api-key
HUGGINGFACE_API_KEY=hf_...tu-token
WORDPRESS_API_URL=https://tudominio.wordpress.com/wp-json/wp/v2
WORDPRESS_USERNAME=tu-usuario
WORDPRESS_PASSWORD=tu-app-password
```

#### 5.3. Probar Deployment

```bash
curl https://tu-proyecto.vercel.app/api/health
```

### PASO 6: Configurar Google Sheets

#### 6.1. Crear Hoja de Cálculo

1. Ve a [sheets.google.com](https://sheets.google.com)
2. Crear nueva hoja: **"Amazon Products Automation"**
3. Configurar headers:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Timestamp | Product URL | Affiliate Link | Status | Article Title | Article URL |

#### 6.2. Configurar Google Apps Script

1. En tu hoja, ve a **Extensions > Apps Script**
2. Borra el código por defecto
3. Copia el código de `google_apps_script.js`
4. Actualizar la URL del webhook:

```javascript
const CONFIG = {
  WEBHOOK_URL: 'https://tu-proyecto.vercel.app/api/webhook',
  // ... resto de configuración
};
```

5. Guardar y ejecutar `setupSheet()`

### PASO 7: Configurar Make.com (Gratis)

#### 7.1. Crear Cuenta Gratuita

1. Ve a [make.com](https://make.com)
2. Regístrate gratis (1000 operaciones/mes)
3. Verifica tu email

#### 7.2. Crear Escenario

1. **New Scenario**
2. Nombre: "Amazon Free Automation"

#### 7.3. Configurar Módulos

**Módulo 1: Webhook**
```json
{
  "module": "webhook:customWebhook",
  "parameters": {
    "hook": "amazon_trigger"
  }
}
```

**Módulo 2: HTTP Request (Generar Artículo)**
```json
{
  "module": "http:ActionSendData",
  "parameters": {
    "url": "https://tu-proyecto.vercel.app/api/generate-article-free",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    },
    "data": {
      "product_url": "{{1.product_url}}",
      "affiliate_link": "{{1.affiliate_link}}",
      "category": "general"
    }
  }
}
```

**Módulo 3: WordPress (Publicar)**
```json
{
  "module": "wordpress:createPost",
  "parameters": {
    "connection": "wordpress_free",
    "title": "{{2.article.title}}",
    "content": "{{2.article.content}}",
    "status": "publish"
  }
}
```

#### 7.4. Configurar Webhook URL

1. Copia la URL del webhook de Make.com
2. Actualízala en Google Apps Script:

```javascript
const WEBHOOK_URL = 'https://hook.integromat.com/tu-webhook-id';
```

### PASO 8: Configurar Ollama Local (Opcional)

#### 8.1. Instalar Ollama

```bash
# En tu PC local
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo gratuito
ollama pull llama2
ollama pull mistral
```

#### 8.2. Ejecutar Servidor

```bash
ollama serve
```

#### 8.3. Probar Localmente

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "prompt": "Escribe un artículo sobre un iPhone",
    "stream": false
  }'
```

## 🧪 Testing Completo

### Test 1: API de IA Gratuita

```bash
# Test Gemini
curl -X POST 'https://tu-proyecto.vercel.app/api/generate-article-free' \
  -H 'Content-Type: application/json' \
  -d '{
    "product_url": "https://www.amazon.com/dp/B08N5WRWNW",
    "affiliate_link": "https://amzn.to/3xyz123"
  }'
```

### Test 2: Flujo Completo

1. **Agregar producto en Google Sheets:**
   - URL: `https://www.amazon.com/dp/B08N5WRWNW`
   - Affiliate: `https://amzn.to/3xyz123`

2. **Verificar procesamiento:**
   - Estado cambia a "Procesando"
   - Make.com recibe webhook
   - Artículo se genera
   - Se publica en WordPress
   - Google Sheets se actualiza

### Test 3: Monitoreo

```bash
# Health check
curl https://tu-proyecto.vercel.app/api/health

# Logs de Make.com
# Revisar en dashboard de Make.com

# Logs de Vercel
# Revisar en dashboard de Vercel
```

## 📊 Límites y Optimizaciones

### Límites Gratuitos

| Servicio | Límite | Optimización |
|----------|--------|--------------|
| Gemini API | 15/min, 1500/día | Usar cache, batch requests |
| Hugging Face | Rate limited | Implementar retry logic |
| Make.com | 1000 ops/mes | ~100 artículos/mes |
| Vercel | 100GB/mes | Optimizar responses |
| WordPress.com | 3GB storage | Optimizar imágenes |

### Estrategias de Optimización

#### 1. Cache de Artículos
```javascript
// En Google Apps Script
function cacheArticle(asin, article) {
  const cache = CacheService.getScriptCache();
  cache.put(asin, JSON.stringify(article), 21600); // 6 horas
}
```

#### 2. Batch Processing
```javascript
// Procesar múltiples productos juntos
function processBatch(products) {
  const batchSize = 5;
  for (let i = 0; i < products.length; i += batchSize) {
    const batch = products.slice(i, i + batchSize);
    processBatchItems(batch);
    Utilities.sleep(60000); // Esperar 1 minuto entre batches
  }
}
```

#### 3. Fallback Inteligente
```javascript
// Prioridad de APIs
const apiPriority = [
  'gemini',      // Más rápido y confiable
  'huggingface', // Backup
  'ollama',      // Local si está disponible
  'template'     // Siempre funciona
];
```

## 🔧 Mantenimiento

### Tareas Diarias
- [ ] Verificar artículos generados
- [ ] Revisar logs de errores
- [ ] Monitorear uso de APIs

### Tareas Semanales
- [ ] Analizar métricas de Make.com
- [ ] Optimizar prompts si es necesario
- [ ] Backup de Google Sheets

### Tareas Mensuales
- [ ] Revisar límites de APIs
- [ ] Actualizar templates
- [ ] Optimizar flujo de trabajo

## 🆘 Solución de Problemas

### Problema: Gemini API no responde
**Solución:**
1. Verificar API key
2. Comprobar límites de rate
3. Usar Hugging Face como backup

### Problema: Make.com se queda sin operaciones
**Solución:**
1. Optimizar escenario (menos módulos)
2. Procesar en batches
3. Usar plan de pago ($9/mes para 10,000 ops)

### Problema: WordPress no publica
**Solución:**
1. Verificar credenciales
2. Comprobar permisos de usuario
3. Revisar formato del contenido

### Problema: Vercel timeout
**Solución:**
1. Optimizar código
2. Usar async/await
3. Implementar timeout handling

## 📈 Escalabilidad

### Para Crecer (Manteniendo Costos Bajos)

#### Nivel 1: Optimización Gratuita (0-100 artículos/mes)
- Usar todos los servicios gratuitos
- Optimizar prompts y templates
- Cache inteligente

#### Nivel 2: Inversión Mínima ($10-20/mes, 500+ artículos/mes)
- Make.com Pro: $9/mes (10,000 operaciones)
- WordPress.com Personal: $4/mes (dominio personalizado)
- OpenAI API: $5-10/mes (mejor calidad)

#### Nivel 3: Profesional ($50-100/mes, 2000+ artículos/mes)
- Servidor VPS: $20/mes
- OpenAI API: $30/mes
- Herramientas premium: $20/mes

## 🎉 ¡Felicidades!

Si has seguido esta guía, ahora tienes:

✅ **Automatización 100% funcional**
✅ **Costo total: $0.00**
✅ **Capacidad: ~100 artículos/mes**
✅ **Escalable según necesidades**

### Próximos Pasos

1. **Generar tu primer artículo** de prueba
2. **Optimizar prompts** para tu nicho
3. **Monitorear métricas** de rendimiento
4. **Escalar gradualmente** según resultados

¡Tu automatización gratuita está lista para generar artículos de calidad sin costo alguno!

