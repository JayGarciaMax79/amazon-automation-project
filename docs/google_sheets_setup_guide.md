# Guía Completa: Configuración de Google Sheets como Trigger

## 1. Introducción

Esta guía te ayudará a configurar Google Sheets como el trigger principal para la automatización de artículos de Amazon. El sistema detectará automáticamente cuando ingreses nuevas URLs de productos y activará todo el proceso de generación de artículos.

## 2. Creación de la Hoja de Cálculo

### Paso 1: Crear Nueva Hoja de Google Sheets

1. Ve a [Google Sheets](https://sheets.google.com)
2. Haz clic en "Crear nueva hoja de cálculo en blanco"
3. Nombra la hoja como "Amazon Products Automation"

### Paso 2: Configurar la Estructura

Copia y pega la siguiente estructura en tu hoja:

| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| **Timestamp** | **Product URL** | **Affiliate Link** | **Status** | **Article Title** | **Article URL** | **Processing Notes** | **Product Title** | **Product Price** | **Product Rating** |

### Paso 3: Configurar Fórmulas Automáticas

#### Columna A (Timestamp) - Fila 2 en adelante:
```
=IF(B2<>"", NOW(), "")
```

#### Columna D (Status) - Fila 2 en adelante:
```
=IF(AND(B2<>"", C2<>""), "Pendiente", "")
```

## 3. Configuración de Validación de Datos

### Para la Columna B (Product URL):

1. Selecciona el rango B2:B1000
2. Ve a **Datos > Validación de datos**
3. Configura:
   - **Criterios:** Texto contiene
   - **Valor:** `amazon.`
   - **Mostrar texto de ayuda:** ✓
   - **Texto de ayuda:** "Debe ser una URL válida de Amazon"
   - **Rechazar entrada:** ✓
   - **Mostrar advertencia:** ✓

### Para la Columna C (Affiliate Link):

1. Selecciona el rango C2:C1000
2. Ve a **Datos > Validación de datos**
3. Configura:
   - **Criterios:** Texto contiene
   - **Valor:** `amzn.to`
   - **Mostrar texto de ayuda:** ✓
   - **Texto de ayuda:** "Debe ser un enlace de afiliado válido de Amazon"
   - **Rechazar entrada:** ✓

## 4. Formato Condicional

### Configurar Colores por Estado:

1. Selecciona todo el rango de datos (A1:J1000)
2. Ve a **Formato > Formato condicional**
3. Agrega las siguientes reglas:

#### Regla 1 - Estado "Pendiente":
- **Rango:** A2:J1000
- **Condición:** La fórmula personalizada es `=$D2="Pendiente"`
- **Color de fondo:** Amarillo claro (#fff3cd)

#### Regla 2 - Estado "Procesando":
- **Rango:** A2:J1000
- **Condición:** La fórmula personalizada es `=$D2="Procesando"`
- **Color de fondo:** Azul claro (#d1ecf1)

#### Regla 3 - Estado "Completado":
- **Rango:** A2:J1000
- **Condición:** La fórmula personalizada es `=$D2="Completado"`
- **Color de fondo:** Verde claro (#d4edda)

#### Regla 4 - Estado "Error":
- **Rango:** A2:J1000
- **Condición:** La fórmula personalizada es `=$D2="Error"`
- **Color de fondo:** Rojo claro (#f8d7da)

## 5. Configuración de Google Apps Script

### Paso 1: Abrir Editor de Scripts

1. En tu hoja de Google Sheets, ve a **Extensiones > Apps Script**
2. Elimina el código por defecto
3. Copia y pega el código del archivo `google_apps_script.js`

### Paso 2: Configurar Variables

En el código, actualiza las siguientes variables:

```javascript
const CONFIG = {
  SHEET_NAME: 'Amazon_Products', // Cambia si usas otro nombre
  WEBHOOK_URL: 'TU_WEBHOOK_URL_DE_MAKE', // URL de webhook de Make.com
  // ... resto de configuración
};
```

### Paso 3: Ejecutar Configuración Inicial

1. En el editor de Apps Script, selecciona la función `setupSheet`
2. Haz clic en **Ejecutar**
3. Autoriza los permisos cuando se solicite
4. Ejecuta también `setupTriggers` para configurar los triggers automáticos

## 6. Configuración de Permisos

### Compartir la Hoja con Make.com:

1. Haz clic en **Compartir** en la esquina superior derecha
2. Agrega la cuenta de servicio de Make.com como **Editor**
3. Copia el ID de la hoja de cálculo (está en la URL)

### Habilitar APIs Necesarias:

1. Ve a [Google Cloud Console](https://console.cloud.google.com)
2. Habilita las siguientes APIs:
   - Google Sheets API
   - Google Drive API
3. Crea credenciales de cuenta de servicio si es necesario

## 7. Prueba de Funcionamiento

### Prueba Manual:

1. Ingresa una URL de producto Amazon en la columna B
2. Ingresa un enlace de afiliado en la columna C
3. Verifica que:
   - Se genere automáticamente el timestamp en columna A
   - El estado cambie a "Pendiente" en columna D
   - Se aplique el formato condicional (fondo amarillo)

### Ejemplo de Datos de Prueba:

| Product URL | Affiliate Link |
|-------------|----------------|
| https://www.amazon.com/dp/B08N5WRWNW | https://amzn.to/3xyz123 |

## 8. Configuración Avanzada

### Webhook de Respuesta (Opcional):

Para recibir actualizaciones desde Make.com:

1. En Apps Script, ve a **Implementar > Nueva implementación**
2. Selecciona **Aplicación web**
3. Configura:
   - **Ejecutar como:** Yo
   - **Acceso:** Cualquier persona
4. Copia la URL de la aplicación web
5. Úsala en Make.com para enviar actualizaciones de vuelta

### Automatización de Limpieza:

Para archivar automáticamente filas antiguas:

1. En Apps Script, configura un trigger temporal:
   ```javascript
   ScriptApp.newTrigger('archiveCompletedRows')
     .timeBased()
     .everyWeeks(1)
     .create();
   ```

## 9. Solución de Problemas

### Problema: Las fórmulas no se ejecutan automáticamente
**Solución:** Verifica que las fórmulas estén en las celdas correctas y que no haya espacios extra.

### Problema: La validación de datos no funciona
**Solución:** Asegúrate de que los rangos estén seleccionados correctamente y que los criterios sean exactos.

### Problema: Los triggers no se activan
**Solución:** 
1. Ve a Apps Script > Triggers
2. Verifica que el trigger `onEdit` esté configurado
3. Ejecuta `setupTriggers()` nuevamente si es necesario

### Problema: Error de permisos
**Solución:**
1. Verifica que la hoja esté compartida correctamente
2. Asegúrate de que las APIs estén habilitadas
3. Revisa las credenciales de la cuenta de servicio

## 10. Mantenimiento

### Tareas Semanales:
- Revisar filas con estado "Error" y corregir problemas
- Archivar filas completadas antiguas
- Verificar que los enlaces de afiliado sigan funcionando

### Tareas Mensuales:
- Revisar y actualizar las fórmulas si es necesario
- Verificar que los triggers sigan activos
- Hacer backup de la hoja de cálculo

## 11. Mejores Prácticas

### Para el Usuario:
1. **Siempre ingresa URLs completas** de Amazon (incluyendo https://)
2. **Verifica que los enlaces de afiliado sean correctos** antes de ingresarlos
3. **No edites las columnas automáticas** (A, D, E, F, G, H, I, J) manualmente
4. **Espera a que el estado cambie a "Completado"** antes de ingresar nuevos productos

### Para el Mantenimiento:
1. **Mantén backups regulares** de la hoja de cálculo
2. **Monitorea los logs de Apps Script** para detectar errores
3. **Actualiza el código** cuando sea necesario
4. **Revisa periódicamente** que Make.com esté funcionando correctamente

## 12. Integración con Make.com

La hoja está preparada para integrarse con Make.com mediante:

1. **Webhook saliente:** Cuando se detecta una nueva entrada
2. **Webhook entrante:** Para recibir actualizaciones del procesamiento
3. **API de Google Sheets:** Para leer y escribir datos

El siguiente paso es configurar el escenario en Make.com que recibirá estos datos y activará el procesamiento de artículos.

---

**¡Importante!** Guarda esta guía y manténla accesible para futuras referencias y solución de problemas.

