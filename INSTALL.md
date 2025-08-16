# 🚀 Instalación Rápida - Amazon Automation

## ⚡ Inicio en 15 Minutos

### 📋 Requisitos Previos
- [ ] Cuenta Google (Gmail)
- [ ] Cuenta GitHub (gratis)
- [ ] Cuenta Make.com (gratis)
- [ ] Cuenta Vercel (gratis)
- [ ] Cuenta WordPress.com (gratis)

### 🎯 Opción 1: Configuración 100% GRATUITA

#### PASO 1: APIs Gratuitas (5 min)

**Google Gemini API:**
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea API Key → Copia (empieza con `AIza...`)

**Hugging Face (Backup):**
1. Ve a [huggingface.co](https://huggingface.co) → Regístrate
2. Settings → Access Tokens → Crear token

#### PASO 2: WordPress Gratis (3 min)

1. Ve a [wordpress.com](https://wordpress.com)
2. "Start with a free site" → Elige dominio: `tudominio.wordpress.com`
3. Users → Profile → Application Passwords → Crear "Amazon Automation"

#### PASO 3: GitHub + Vercel (5 min)

1. **GitHub:** Sube este proyecto a tu repositorio
2. **Vercel:** Conecta con GitHub → Deploy
3. **Variables de entorno en Vercel:**
```
GOOGLE_GEMINI_API_KEY=AIza...
HUGGINGFACE_API_KEY=hf_...
WORDPRESS_API_URL=https://tudominio.wordpress.com/wp-json/wp/v2
WORDPRESS_USERNAME=tu-usuario
WORDPRESS_PASSWORD=tu-app-password
```

#### PASO 4: Google Sheets (2 min)

1. Crea nueva hoja: "Amazon Products Automation"
2. Extensions → Apps Script → Pega código de `scripts/google_apps_script.js`
3. Actualiza `WEBHOOK_URL` con tu URL de Vercel

#### PASO 5: Make.com (5 min)

1. Crea cuenta gratis en [make.com](https://make.com)
2. Importa blueprint de `config/make_scenario.json`
3. Conecta servicios y activa escenario

### ✅ ¡LISTO! Prueba tu primer artículo

1. En Google Sheets, agrega:
   - **Product URL:** `https://www.amazon.com/dp/B08N5WRWNW`
   - **Affiliate Link:** `https://amzn.to/3xyz123`

2. En 2-3 minutos verás el artículo publicado en tu WordPress

---

## 🎯 Opción 2: Con OpenAI (Mejor Calidad)

Si tienes API key de OpenAI, sigue los mismos pasos pero:

1. **En Vercel, agrega:**
```
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.openai.com/v1
```

2. **Usa el endpoint:** `/api/generate-article` (en lugar de `/api/generate-article-free`)

---

## 📁 Estructura de Archivos

```
amazon-automation-package/
├── 📖 INSTALL.md (esta guía)
├── 📖 README.md (descripción completa)
├── 📁 api/ (funciones serverless)
├── 📁 docs/ (documentación detallada)
├── 📁 scripts/ (Google Apps Script y utilidades)
├── 📁 config/ (configuraciones Make.com)
├── 📁 templates/ (plantillas HTML)
└── 📁 examples/ (ejemplos de uso)
```

---

## 🆘 ¿Problemas?

### Error común: "API Key inválida"
**Solución:** Verifica que copiaste la API key completa sin espacios

### Error: "Webhook no funciona"
**Solución:** Verifica que la URL en Google Apps Script sea correcta

### Error: "WordPress no publica"
**Solución:** Verifica username y application password

---

## 📊 Límites Gratuitos

| Servicio | Límite Gratis | Artículos/mes |
|----------|---------------|---------------|
| Google Gemini | 1500/día | ~100 |
| Make.com | 1000 ops | ~100 |
| Vercel | 100GB | Ilimitado |
| WordPress.com | 3GB storage | ~500 |

**Total: ~100 artículos/mes GRATIS**

---

## 🚀 Próximos Pasos

1. **Personaliza templates** en `templates/`
2. **Optimiza prompts** para tu nicho
3. **Monitorea métricas** en dashboards
4. **Escala gradualmente** según necesidades

¡Tu automatización está lista! 🎉

