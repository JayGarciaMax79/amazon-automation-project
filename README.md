# Amazon Products Article Automation

🚀 **Automatización completa para generar artículos de calidad sobre productos de Amazon usando IA**

## 📋 Descripción

Este proyecto automatiza completamente el proceso de creación de artículos de blog sobre productos de Amazon, desde la entrada de datos en Google Sheets hasta la publicación final en WordPress, utilizando OpenManus AI como motor de generación de contenido.

## 🏗️ Arquitectura

```
Google Sheets (Trigger) 
    ↓
Make.com (Orquestador)
    ↓
Vercel Functions (OpenManus AI)
    ↓
GitHub (Versionado)
    ↓
WordPress (Publicación)
```

## ✨ Características

- 🤖 **Generación automática de artículos** usando OpenManus AI
- 📊 **Google Sheets como trigger** - Solo ingresa URL + enlace de afiliado
- 🔄 **Make.com para orquestación** - Workflow visual sin código
- ⚡ **Funciones serverless** - Escalable y sin costos de servidor
- 📝 **Optimización SEO automática** - Títulos, meta descripciones y keywords
- 🎨 **Templates por categoría** - Electrónicos, hogar, moda, libros
- 🔗 **Integración natural de enlaces de afiliado** - Maximiza conversiones
- 📱 **Responsive y moderno** - Compatible con todos los dispositivos

## 🚀 Inicio Rápido

### 1. Configurar Google Sheets
```bash
# Copia la plantilla de Google Sheets
# Configura las fórmulas automáticas
# Instala el script de Google Apps Script
```

### 2. Desplegar en Vercel
```bash
# Clona este repositorio
git clone https://github.com/tu-usuario/amazon-automation-project.git

# Despliega en Vercel
vercel --prod
```

### 3. Configurar Make.com
```bash
# Importa el blueprint de Make.com
# Conecta con Google Sheets y Vercel
# Configura WordPress API
```

## 📁 Estructura del Proyecto

```
amazon-automation-project/
├── .github/workflows/          # GitHub Actions
├── api/                        # Funciones serverless
│   ├── generate-article.py     # Generador principal
│   ├── scrape-amazon.py        # Extractor de datos
│   └── webhook.py              # Webhooks para Make.com
├── src/                        # Código fuente
│   ├── openmanus_integration/  # Integración OpenManus
│   ├── templates/              # Templates de artículos
│   └── utils/                  # Utilidades
├── docs/                       # Documentación
├── config/                     # Configuraciones
├── templates/                  # Plantillas
└── README.md
```

## 🛠️ Tecnologías

- **IA:** OpenManus (GPT-4o)
- **Trigger:** Google Sheets + Apps Script
- **Orquestación:** Make.com (Integromat)
- **Backend:** Python + Flask
- **Hosting:** Vercel Functions (Serverless)
- **Versionado:** GitHub + GitHub Actions
- **Publicación:** WordPress REST API

## 📖 Documentación

- [🔧 Guía de Configuración](docs/setup-guide.md)
- [📊 Configurar Google Sheets](docs/google-sheets-setup.md)
- [🤖 Integración OpenManus](docs/openmanus-integration.md)
- [⚙️ Configurar Make.com](docs/make-com-setup.md)
- [🚀 Despliegue en Vercel](docs/vercel-deployment.md)
- [🔗 API Reference](docs/api-reference.md)

## 🎯 Flujo de Trabajo

1. **Usuario ingresa datos** en Google Sheets:
   - URL del producto Amazon
   - Enlace de afiliado

2. **Google Apps Script detecta** nueva entrada y envía webhook a Make.com

3. **Make.com orquesta** el proceso:
   - Llama a función de extracción de datos
   - Envía datos a generador de artículos OpenManus
   - Publica artículo en WordPress

4. **Resultado final**:
   - Artículo SEO optimizado publicado
   - Google Sheets actualizado con enlaces
   - Versionado automático en GitHub

## 💰 Costos

| Servicio | Plan Gratuito | Límites |
|----------|---------------|---------|
| Google Sheets | ✅ Gratis | Ilimitado |
| Make.com | ✅ 1000 ops/mes | Suficiente para ~100 artículos |
| Vercel | ✅ 100GB/mes | Suficiente para miles de requests |
| GitHub | ✅ Repositorios públicos | Ilimitado |
| OpenAI API | 💳 Pago por uso | ~$0.01-0.03 por artículo |

**Costo estimado:** $1-3 USD por 100 artículos

## 🔧 Configuración

### Variables de Entorno

```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.openai.com/v1

# Google Sheets
GOOGLE_SHEETS_API_KEY=...
GOOGLE_SERVICE_ACCOUNT_EMAIL=...

# WordPress
WORDPRESS_API_URL=https://tu-sitio.com/wp-json/wp/v2
WORDPRESS_USERNAME=...
WORDPRESS_PASSWORD=...

# Make.com
MAKE_WEBHOOK_URL=https://hook.integromat.com/...
```

### Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/amazon-automation-project.git
cd amazon-automation-project

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar localmente
python api/generate-article.py
```

## 📊 Métricas y Monitoreo

- **Artículos generados:** Tracking automático en Google Sheets
- **Calidad SEO:** Puntuación automática 1-10
- **Tiempo de procesamiento:** Promedio 30-60 segundos
- **Tasa de éxito:** >95% con URLs válidas

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

- 📧 **Email:** soporte@tu-dominio.com
- 💬 **Discord:** [Únete a nuestro servidor](https://discord.gg/...)
- 📖 **Documentación:** [docs.tu-dominio.com](https://docs.tu-dominio.com)
- 🐛 **Issues:** [GitHub Issues](https://github.com/tu-usuario/amazon-automation-project/issues)

## 🙏 Agradecimientos

- [OpenManus](https://github.com/FoundationAgents/OpenManus) - Motor de IA
- [Make.com](https://make.com) - Plataforma de automatización
- [Vercel](https://vercel.com) - Hosting serverless
- [Google Sheets](https://sheets.google.com) - Base de datos y trigger

---

⭐ **¡Si este proyecto te ayuda, dale una estrella!** ⭐

