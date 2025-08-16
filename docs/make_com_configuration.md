# Configuración Completa de Make.com para Automatización de Artículos Amazon

## 1. Introducción

Make.com (anteriormente Integromat) será el orquestador central de nuestra automatización. Conectará Google Sheets con nuestras funciones serverless y WordPress para crear un flujo completamente automático.

## 2. Configuración Inicial de Make.com

### Paso 1: Crear Cuenta en Make.com

1. Ve a [make.com](https://make.com)
2. Regístrate con tu email
3. Verifica tu cuenta
4. **Plan recomendado:** Free (1000 operaciones/mes = ~100 artículos)

### Paso 2: Configurar Conexiones

#### Conexión con Google Sheets:
1. Ve a **Connections** en el panel lateral
2. Busca "Google Sheets"
3. Haz clic en **Create a connection**
4. Autoriza el acceso a tu cuenta de Google
5. Nombra la conexión: "Amazon_Automation_Sheets"

#### Conexión con WordPress:
1. Busca "WordPress" en conexiones
2. Configura:
   - **Site URL:** https://myamzdeals.shop
   - **Username:** tu-usuario-wp
   - **Application Password:** (generar en WordPress)
3. Nombra la conexión: "MyAmzDeals_WordPress"

## 3. Crear el Escenario Principal

### Paso 1: Nuevo Escenario

1. Haz clic en **Create a new scenario**
2. Nombra el escenario: "Amazon Article Automation"
3. Descripción: "Automatización completa de artículos de productos Amazon"

### Paso 2: Configurar Trigger (Google Sheets)

#### Módulo 1: Google Sheets - Watch Rows

```json
{
  "module": "google-sheets:watchRows",
  "parameters": {
    "connection": "Amazon_Automation_Sheets",
    "spreadsheetId": "TU_SPREADSHEET_ID",
    "sheetName": "Amazon_Products",
    "tableContainsHeaders": true,
    "limit": 1
  },
  "filter": {
    "condition": "AND",
    "rules": [
      {
        "field": "Status",
        "operator": "equal",
        "value": "Pendiente"
      },
      {
        "field": "Product URL",
        "operator": "notEmpty"
      },
      {
        "field": "Affiliate Link", 
        "operator": "notEmpty"
      }
    ]
  }
}
```

### Paso 3: Actualizar Estado a "Procesando"

#### Módulo 2: Google Sheets - Update a Row

```json
{
  "module": "google-sheets:updateRow",
  "parameters": {
    "connection": "Amazon_Automation_Sheets",
    "spreadsheetId": "TU_SPREADSHEET_ID",
    "sheetName": "Amazon_Products",
    "row": "{{1.__IMTINDEX__}}",
    "values": {
      "Status": "Procesando",
      "Processing Notes": "Iniciando procesamiento con OpenManus..."
    }
  }
}
```

### Paso 4: Extraer Datos del Producto

#### Módulo 3: HTTP - Make a Request (Scraping)

```json
{
  "module": "http:ActionSendData",
  "parameters": {
    "url": "https://tu-proyecto.vercel.app/api/scrape-amazon",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    },
    "data": {
      "url": "{{1.Product URL}}"
    },
    "timeout": 60,
    "followRedirect": true,
    "rejectUnauthorized": true
  }
}
```

### Paso 5: Generar Artículo con OpenManus

#### Módulo 4: HTTP - Make a Request (Generación)

```json
{
  "module": "http:ActionSendData", 
  "parameters": {
    "url": "https://tu-proyecto.vercel.app/api/generate-article",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer TU_API_TOKEN"
    },
    "data": {
      "product_url": "{{1.Product URL}}",
      "affiliate_link": "{{1.Affiliate Link}}",
      "product_data": "{{3.data}}",
      "category": "{{3.data.category}}",
      "language": "es"
    },
    "timeout": 300,
    "followRedirect": true
  }
}
```

### Paso 6: Publicar en WordPress

#### Módulo 5: WordPress - Create a Post

```json
{
  "module": "wordpress:createPost",
  "parameters": {
    "connection": "MyAmzDeals_WordPress",
    "title": "{{4.article.title}}",
    "content": "{{4.article.content}}",
    "status": "publish",
    "categories": ["Reviews", "Amazon"],
    "tags": "{{join(4.article.keywords, ',')}}",
    "excerpt": "{{4.article.meta_description}}",
    "featured_media": "{{4.article.featured_image_id}}"
  }
}
```

### Paso 7: Actualizar Google Sheets con Resultado

#### Módulo 6: Google Sheets - Update a Row (Final)

```json
{
  "module": "google-sheets:updateRow",
  "parameters": {
    "connection": "Amazon_Automation_Sheets", 
    "spreadsheetId": "TU_SPREADSHEET_ID",
    "sheetName": "Amazon_Products",
    "row": "{{1.__IMTINDEX__}}",
    "values": {
      "Status": "Completado",
      "Article Title": "{{4.article.title}}",
      "Article URL": "{{5.link}}",
      "Processing Notes": "Artículo generado y publicado exitosamente",
      "Product Title": "{{3.data.title}}",
      "Product Price": "{{3.data.current_price}}",
      "Product Rating": "{{3.data.rating}}"
    }
  }
}
```

## 4. Manejo de Errores

### Módulo de Error Handler

#### Error Handler - Google Sheets Update

```json
{
  "module": "google-sheets:updateRow",
  "parameters": {
    "connection": "Amazon_Automation_Sheets",
    "spreadsheetId": "TU_SPREADSHEET_ID", 
    "sheetName": "Amazon_Products",
    "row": "{{1.__IMTINDEX__}}",
    "values": {
      "Status": "Error",
      "Processing Notes": "Error: {{error.message}}"
    }
  },
  "errorHandlers": [
    {
      "break": true,
      "scope": "scenario"
    }
  ]
}
```

## 5. Configuración de Webhooks

### Webhook Entrante (desde Google Apps Script)

1. En Make.com, agrega un módulo **Webhooks - Custom webhook**
2. Copia la URL del webhook
3. Úsala en el Google Apps Script:

```javascript
const WEBHOOK_URL = 'https://hook.integromat.com/tu-webhook-id';
```

### Webhook Saliente (hacia Google Apps Script)

#### Módulo: HTTP - Make a Request

```json
{
  "module": "http:ActionSendData",
  "parameters": {
    "url": "https://script.google.com/macros/s/TU_SCRIPT_ID/exec",
    "method": "POST",
    "headers": {
      "Content-Type": "application/json"
    },
    "data": {
      "function": "updateProcessingResult",
      "row_number": "{{1.__IMTINDEX__}}",
      "success": "{{if(5.id, true, false)}}",
      "article_title": "{{4.article.title}}",
      "article_url": "{{5.link}}",
      "error": "{{error.message}}"
    }
  }
}
```

## 6. Configuración Avanzada

### Filtros y Condiciones

#### Filtro para URLs válidas:
```javascript
// En el módulo de Google Sheets
{{contains(1.Product URL, "amazon.")}} AND {{contains(1.Affiliate Link, "amzn.to")}}
```

#### Filtro para evitar duplicados:
```javascript
// Verificar que no exista ya un artículo
{{empty(1.Article URL)}}
```

### Variables y Funciones

#### Variables globales útiles:
```javascript
// Timestamp actual
{{formatDate(now, "YYYY-MM-DD HH:mm:ss")}}

// Extraer ASIN de URL
{{regexReplace(1.Product URL, ".*\/dp\/([A-Z0-9]{10}).*", "$1")}}

// Limpiar título para URL
{{replace(replace(lower(4.article.title), " ", "-"), "[^a-z0-9-]", "")}}
```

## 7. Monitoreo y Logs

### Configurar Notificaciones

#### Email de Error:
```json
{
  "module": "email:ActionSendEmail",
  "parameters": {
    "to": "tu-email@gmail.com",
    "subject": "Error en Automatización Amazon - {{1.Product URL}}",
    "html": "
      <h2>Error en el procesamiento</h2>
      <p><strong>URL:</strong> {{1.Product URL}}</p>
      <p><strong>Error:</strong> {{error.message}}</p>
      <p><strong>Timestamp:</strong> {{formatDate(now)}}</p>
    "
  }
}
```

#### Slack/Discord Notification:
```json
{
  "module": "slack:ActionPostMessage",
  "parameters": {
    "connection": "slack_connection",
    "channel": "#automatizacion",
    "text": "✅ Nuevo artículo publicado: {{4.article.title}} - {{5.link}}"
  }
}
```

## 8. Optimizaciones de Rendimiento

### Configuración de Scheduling

1. **Intervalo de ejecución:** Cada 5 minutos
2. **Límite de ejecuciones:** 1 por vez
3. **Timeout:** 10 minutos por escenario

### Configuración de Rate Limiting

```json
{
  "rateLimit": {
    "requests": 10,
    "period": 60,
    "scope": "scenario"
  }
}
```

## 9. Testing del Escenario

### Datos de Prueba

```json
{
  "test_data": {
    "Product URL": "https://www.amazon.com/dp/B08N5WRWNW",
    "Affiliate Link": "https://amzn.to/3xyz123",
    "Status": "Pendiente"
  }
}
```

### Pasos de Testing:

1. **Ejecutar manualmente** el escenario
2. **Verificar cada módulo** paso a paso
3. **Revisar logs** de errores
4. **Confirmar resultado** en WordPress
5. **Validar actualización** en Google Sheets

## 10. Blueprint del Escenario (JSON)

```json
{
  "name": "Amazon Article Automation",
  "flow": [
    {
      "id": 1,
      "module": "google-sheets:watchRows",
      "version": 1,
      "parameters": {
        "connection": "amazon_automation_sheets",
        "mode": "select",
        "spreadsheetId": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        "sheetName": "Amazon_Products",
        "tableContainsHeaders": true,
        "includeEmptyRows": false,
        "limit": 1
      },
      "mapper": {},
      "metadata": {
        "designer": {
          "x": 0,
          "y": 0
        },
        "restore": {},
        "parameters": [
          {
            "name": "connection",
            "type": "account",
            "label": "Connection",
            "required": true
          }
        ]
      }
    },
    {
      "id": 2,
      "module": "google-sheets:updateRow",
      "version": 1,
      "parameters": {
        "connection": "amazon_automation_sheets",
        "mode": "select",
        "spreadsheetId": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        "sheetName": "Amazon_Products",
        "row": "{{1.__IMTINDEX__}}",
        "values": {
          "Status": "Procesando"
        }
      }
    }
  ],
  "metadata": {
    "instant": false,
    "version": 1,
    "scenario": {
      "roundtrips": 1,
      "maxErrors": 3,
      "autoCommit": true,
      "autoCommitTriggerLast": true,
      "sequential": false,
      "confidential": false,
      "dataloss": false,
      "dlq": false
    },
    "designer": {
      "orphans": []
    },
    "zone": "us1.make.com"
  }
}
```

## 11. Configuración de Variables de Entorno

### En Make.com:

1. Ve a **Organization settings**
2. **Environment variables**
3. Agrega:

```
OPENAI_API_KEY=sk-tu-api-key
VERCEL_API_URL=https://tu-proyecto.vercel.app
WORDPRESS_API_URL=https://myamzdeals.shop/wp-json/wp/v2
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms
```

## 12. Mantenimiento y Monitoreo

### Tareas Diarias:
- Revisar ejecuciones fallidas
- Verificar artículos publicados
- Monitorear uso de operaciones

### Tareas Semanales:
- Analizar métricas de rendimiento
- Optimizar prompts si es necesario
- Revisar y actualizar filtros

### Tareas Mensuales:
- Backup de configuración del escenario
- Revisar y optimizar flujo de trabajo
- Actualizar documentación

Esta configuración te permitirá tener una automatización completamente funcional que procese productos de Amazon y genere artículos de alta calidad de forma automática.

