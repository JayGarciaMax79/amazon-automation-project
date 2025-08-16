# Estructura de Google Sheets para Automatización de Artículos Amazon

## 1. Configuración de la Hoja de Cálculo

### Nombre de la Hoja
`Amazon_Products_Automation`

### Columnas Requeridas

| Columna | Nombre | Tipo | Descripción | Ejemplo |
|---------|--------|------|-------------|---------|
| A | `timestamp` | Fecha/Hora | Fecha y hora de entrada automática | 2025-01-15 14:30:00 |
| B | `product_url` | URL | URL del producto de Amazon | https://www.amazon.com/dp/B08N5WRWNW |
| C | `affiliate_link` | URL | Enlace de afiliado de Amazon | https://amzn.to/3xyz123 |
| D | `status` | Texto | Estado del procesamiento | Pendiente/Procesando/Completado/Error |
| E | `article_title` | Texto | Título generado del artículo | "Análisis completo del iPhone 13..." |
| F | `article_url` | URL | URL del artículo publicado | https://myamzdeals.shop/iphone-13-review |
| G | `processing_notes` | Texto | Notas del procesamiento | "Artículo generado exitosamente" |
| H | `product_title` | Texto | Título extraído del producto | "Apple iPhone 13 (128GB, Blue)" |
| I | `product_price` | Texto | Precio extraído | "$699.00" |
| J | `product_rating` | Texto | Calificación del producto | "4.5 de 5" |

## 2. Fórmulas Automáticas

### Columna A (Timestamp)
```
=IF(B2<>"", NOW(), "")
```
Esta fórmula se activa automáticamente cuando se ingresa una URL en la columna B.

### Columna D (Status) - Valor por defecto
```
=IF(B2<>"", "Pendiente", "")
```
Establece automáticamente el estado como "Pendiente" cuando se ingresa una URL.

## 3. Validación de Datos

### Columna B (Product URL)
- **Tipo:** URL
- **Validación:** Debe contener "amazon.com" o "amazon.es" o dominios Amazon válidos
- **Mensaje de error:** "Debe ser una URL válida de Amazon"

### Columna C (Affiliate Link)
- **Tipo:** URL
- **Validación:** Debe contener "amzn.to" o "amazon.com" con tag de afiliado
- **Mensaje de error:** "Debe ser un enlace de afiliado válido de Amazon"

## 4. Formato Condicional

### Estados de Procesamiento
- **Pendiente:** Fondo amarillo claro
- **Procesando:** Fondo azul claro
- **Completado:** Fondo verde claro
- **Error:** Fondo rojo claro

### Reglas de Formato
```
Pendiente: =$D2="Pendiente"
Procesando: =$D2="Procesando"
Completado: =$D2="Completado"
Error: =$D2="Error"
```

## 5. Configuración del Trigger en Make.com

### Módulo: Google Sheets - Watch Rows
- **Spreadsheet:** Amazon_Products_Automation
- **Sheet:** Hoja1
- **Table contains headers:** Sí
- **Row with headers:** 1
- **Limit:** 1 (procesar de uno en uno)

### Filtro de Trigger
```
Status = "Pendiente"
Product URL is not empty
Affiliate Link is not empty
```

## 6. Ejemplo de Entrada de Usuario

### Paso 1: Usuario ingresa datos
| product_url | affiliate_link |
|-------------|----------------|
| https://www.amazon.com/dp/B08N5WRWNW | https://amzn.to/3xyz123 |

### Paso 2: Fórmulas automáticas se ejecutan
| timestamp | product_url | affiliate_link | status |
|-----------|-------------|----------------|--------|
| 2025-01-15 14:30:00 | https://www.amazon.com/dp/B08N5WRWNW | https://amzn.to/3xyz123 | Pendiente |

### Paso 3: Make.com detecta nueva fila y procesa

### Paso 4: Resultado final
| timestamp | product_url | affiliate_link | status | article_title | article_url | product_title | product_price |
|-----------|-------------|----------------|--------|---------------|-------------|---------------|---------------|
| 2025-01-15 14:30:00 | https://www.amazon.com/dp/B08N5WRWNW | https://amzn.to/3xyz123 | Completado | "iPhone 13: Análisis Completo y Mejor Precio" | https://myamzdeals.shop/iphone-13-analisis | "Apple iPhone 13 (128GB, Blue)" | "$699.00" |

## 7. Configuración de Permisos

### Compartir la Hoja
- **Make.com Service Account:** Editor
- **Usuario:** Propietario
- **Otros colaboradores:** Viewer (opcional)

### API de Google Sheets
- Habilitar Google Sheets API
- Crear credenciales de servicio
- Compartir hoja con email del servicio

## 8. Instrucciones para el Usuario

### Uso Diario
1. Abrir Google Sheets
2. Ir a la primera fila vacía
3. Pegar URL del producto Amazon en columna B
4. Pegar enlace de afiliado en columna C
5. Esperar 2-5 minutos para procesamiento automático
6. Verificar estado en columna D
7. Obtener URL del artículo en columna F

### Solución de Problemas
- Si estado = "Error": Verificar URLs y reintentar
- Si no se procesa: Verificar conexión Make.com
- Si artículo no se publica: Verificar configuración WordPress

## 9. Backup y Seguridad

### Backup Automático
- Google Sheets mantiene historial de versiones
- Exportar semanalmente como Excel/CSV
- Configurar notificaciones de cambios

### Seguridad
- No compartir enlaces de afiliado públicamente
- Mantener hoja privada
- Usar autenticación de 2 factores en Google

Esta estructura asegura que el trigger funcione correctamente con ambos enlaces (producto y afiliado) y proporciona un seguimiento completo del proceso de automatización.

