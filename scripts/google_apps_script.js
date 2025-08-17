/**
 * Google Apps Script para Automatización de Artículos de Amazon
 * Este script proporciona funcionalidades avanzadas para la hoja de cálculo
 */

// Configuración global
const CONFIG = {
  SHEET_NAME: 'Amazon_Products',
  WEBHOOK_URL: 'https://hook.eu2.make.com/p6v3c95jn9sogebq45gweqovpnvjge5h', // Reemplazar con tu webhook de Make.com
  COLUMNS: {
    TIMESTAMP: 0,    // A
    PRODUCT_URL: 1,  // B
    AFFILIATE_LINK: 2, // C
    STATUS: 3,       // D
    ARTICLE_TITLE: 4, // E
    ARTICLE_URL: 5,  // F
    NOTES: 6,        // G
    PRODUCT_TITLE: 7, // H
    PRODUCT_PRICE: 8, // I
    PRODUCT_RATING: 9 // J
  },
  STATUS: {
    PENDING: 'Pendiente',
    PROCESSING: 'Procesando',
    COMPLETED: 'Completado',
    ERROR: 'Error'
  }
};

/**
 * Función que se ejecuta cuando se edita la hoja
 * Detecta nuevas entradas y activa el procesamiento
 */
function onEdit(e) {
  try {
    const sheet = e.source.getActiveSheet();
    
    // Verificar que sea la hoja correcta
    if (sheet.getName() !== CONFIG.SHEET_NAME) {
      return;
    }
    
    const range = e.range;
    const row = range.getRow();
    const col = range.getColumn();
    
    // Solo procesar si se editó la columna B (Product URL) o C (Affiliate Link)
    if (col === CONFIG.COLUMNS.PRODUCT_URL + 1 || col === CONFIG.COLUMNS.AFFILIATE_LINK + 1) {
      processNewEntry(sheet, row);
    }
    
  } catch (error) {
    console.error('Error en onEdit:', error);
    Logger.log('Error en onEdit: ' + error.toString());
  }
}

/**
 * Procesa una nueva entrada en la hoja
 */
function processNewEntry(sheet, row) {
  try {
    // Obtener datos de la fila
    const productUrl = sheet.getRange(row, CONFIG.COLUMNS.PRODUCT_URL + 1).getValue();
    const affiliateLink = sheet.getRange(row, CONFIG.COLUMNS.AFFILIATE_LINK + 1).getValue();
    const currentStatus = sheet.getRange(row, CONFIG.COLUMNS.STATUS + 1).getValue();
    
    // Verificar que ambos campos estén llenos y no haya sido procesado
    if (productUrl && affiliateLink && !currentStatus) {
      
      // Validar URLs
      if (!isValidAmazonUrl(productUrl)) {
        setRowStatus(sheet, row, CONFIG.STATUS.ERROR, 'URL de Amazon inválida');
        return;
      }
      
      if (!isValidAffiliateLink(affiliateLink)) {
        setRowStatus(sheet, row, CONFIG.STATUS.ERROR, 'Enlace de afiliado inválido');
        return;
      }
      
      // Establecer timestamp y estado
      sheet.getRange(row, CONFIG.COLUMNS.TIMESTAMP + 1).setValue(new Date());
      setRowStatus(sheet, row, CONFIG.STATUS.PENDING, 'Preparado para procesamiento');
      
      // Enviar webhook a Make.com
      sendWebhookToMake(productUrl, affiliateLink, row);
      
      // Actualizar estado a procesando
      setRowStatus(sheet, row, CONFIG.STATUS.PROCESSING, 'Enviado a Make.com para procesamiento');
      
      Logger.log(`Nueva entrada procesada en fila ${row}: ${productUrl}`);
    }
    
  } catch (error) {
    console.error('Error procesando nueva entrada:', error);
    setRowStatus(sheet, row, CONFIG.STATUS.ERROR, 'Error interno: ' + error.toString());
  }
}

/**
 * Establece el estado de una fila
 */
function setRowStatus(sheet, row, status, notes = '') {
  sheet.getRange(row, CONFIG.COLUMNS.STATUS + 1).setValue(status);
  if (notes) {
    sheet.getRange(row, CONFIG.COLUMNS.NOTES + 1).setValue(notes);
  }
  
  // Aplicar formato condicional
  applyConditionalFormatting(sheet, row, status);
}

/**
 * Aplica formato condicional basado en el estado
 */
function applyConditionalFormatting(sheet, row, status) {
  const range = sheet.getRange(row, 1, 1, 10); // Toda la fila
  
  switch (status) {
    case CONFIG.STATUS.PENDING:
      range.setBackground('#fff3cd'); // Amarillo claro
      break;
    case CONFIG.STATUS.PROCESSING:
      range.setBackground('#d1ecf1'); // Azul claro
      break;
    case CONFIG.STATUS.COMPLETED:
      range.setBackground('#d4edda'); // Verde claro
      break;
    case CONFIG.STATUS.ERROR:
      range.setBackground('#f8d7da'); // Rojo claro
      break;
    default:
      range.setBackground('#ffffff'); // Blanco
  }
}

/**
 * Valida si una URL es de Amazon
 */
function isValidAmazonUrl(url) {
  if (!url || typeof url !== 'string') return false;
  
  const amazonDomains = [
    'amazon.com', 'amazon.es', 'amazon.co.uk', 'amazon.de',
    'amazon.fr', 'amazon.it', 'amazon.ca', 'amazon.com.mx'
  ];
  
  return amazonDomains.some(domain => url.includes(domain)) && url.includes('/dp/');
}

/**
 * Valida si un enlace es de afiliado de Amazon
 */
function isValidAffiliateLink(link) {
  if (!link || typeof link !== 'string') return false;
  
  return link.includes('amzn.to') || 
         (link.includes('amazon.') && link.includes('tag='));
}

/**
 * Envía webhook a Make.com
 */
function sendWebhookToMake(productUrl, affiliateLink, row) {
  try {
    const payload = {
      product_url: productUrl,
      affiliate_link: affiliateLink,
      row_number: row,
      timestamp: new Date().toISOString(),
      sheet_id: SpreadsheetApp.getActiveSpreadsheet().getId()
    };
    
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(payload)
    };
    
    const response = UrlFetchApp.fetch(CONFIG.WEBHOOK_URL, options);
    
    if (response.getResponseCode() === 200) {
      Logger.log('Webhook enviado exitosamente a Make.com');
    } else {
      throw new Error(`Error HTTP: ${response.getResponseCode()}`);
    }
    
  } catch (error) {
    console.error('Error enviando webhook:', error);
    Logger.log('Error enviando webhook: ' + error.toString());
    throw error;
  }
}

/**
 * Función para actualizar el resultado desde Make.com
 * Se llama mediante webhook desde Make.com cuando el procesamiento termina
 */
function updateProcessingResult(data) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
    const row = data.row_number;
    
    if (data.success) {
      // Actualizar con datos del artículo generado
      sheet.getRange(row, CONFIG.COLUMNS.ARTICLE_TITLE + 1).setValue(data.article_title || '');
      sheet.getRange(row, CONFIG.COLUMNS.ARTICLE_URL + 1).setValue(data.article_url || '');
      sheet.getRange(row, CONFIG.COLUMNS.PRODUCT_TITLE + 1).setValue(data.product_title || '');
      sheet.getRange(row, CONFIG.COLUMNS.PRODUCT_PRICE + 1).setValue(data.product_price || '');
      sheet.getRange(row, CONFIG.COLUMNS.PRODUCT_RATING + 1).setValue(data.product_rating || '');
      
      setRowStatus(sheet, row, CONFIG.STATUS.COMPLETED, 'Artículo generado y publicado exitosamente');
      
    } else {
      setRowStatus(sheet, row, CONFIG.STATUS.ERROR, data.error || 'Error desconocido en el procesamiento');
    }
    
    Logger.log(`Resultado actualizado para fila ${row}: ${data.success ? 'Éxito' : 'Error'}`);
    
  } catch (error) {
    console.error('Error actualizando resultado:', error);
    Logger.log('Error actualizando resultado: ' + error.toString());
  }
}

/**
 * Función para configurar la hoja inicialmente
 * Ejecutar una vez para configurar headers y formato
 */
function setupSheet() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAME);
    
    // Crear hoja si no existe
    if (!sheet) {
      sheet = spreadsheet.insertSheet(CONFIG.SHEET_NAME);
    }
    
    // Configurar headers
    const headers = [
      'Timestamp', 'Product URL', 'Affiliate Link', 'Status',
      'Article Title', 'Article URL', 'Processing Notes',
      'Product Title', 'Product Price', 'Product Rating'
    ];
    
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    
    // Formatear headers
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setBackground('#4CAF50');
    headerRange.setFontColor('#FFFFFF');
    headerRange.setFontWeight('bold');
    
    // Configurar validación de datos para columna B (Product URL)
    const productUrlRange = sheet.getRange(2, CONFIG.COLUMNS.PRODUCT_URL + 1, 1000, 1);
    const urlValidation = SpreadsheetApp.newDataValidation()
      .requireTextContains('amazon.')
      .setHelpText('Debe ser una URL válida de Amazon')
      .build();
    productUrlRange.setDataValidation(urlValidation);
    
    // Configurar validación para columna C (Affiliate Link)
    const affiliateRange = sheet.getRange(2, CONFIG.COLUMNS.AFFILIATE_LINK + 1, 1000, 1);
    const affiliateValidation = SpreadsheetApp.newDataValidation()
      .requireTextContains('amzn.to')
      .setHelpText('Debe ser un enlace de afiliado válido de Amazon')
      .build();
    affiliateRange.setDataValidation(affiliateValidation);
    
    // Configurar anchos de columna
    sheet.setColumnWidth(1, 150); // Timestamp
    sheet.setColumnWidth(2, 300); // Product URL
    sheet.setColumnWidth(3, 200); // Affiliate Link
    sheet.setColumnWidth(4, 100); // Status
    sheet.setColumnWidth(5, 300); // Article Title
    sheet.setColumnWidth(6, 300); // Article URL
    sheet.setColumnWidth(7, 200); // Notes
    sheet.setColumnWidth(8, 250); // Product Title
    sheet.setColumnWidth(9, 100); // Price
    sheet.setColumnWidth(10, 100); // Rating
    
    Logger.log('Hoja configurada exitosamente');
    
  } catch (error) {
    console.error('Error configurando hoja:', error);
    Logger.log('Error configurando hoja: ' + error.toString());
  }
}

/**
 * Función para limpiar filas completadas (opcional)
 * Mueve filas completadas a una hoja de archivo
 */
function archiveCompletedRows() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sourceSheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAME);
    
    // Crear hoja de archivo si no existe
    let archiveSheet = spreadsheet.getSheetByName('Archivo');
    if (!archiveSheet) {
      archiveSheet = spreadsheet.insertSheet('Archivo');
      // Copiar headers
      const headers = sourceSheet.getRange(1, 1, 1, 10).getValues();
      archiveSheet.getRange(1, 1, 1, 10).setValues(headers);
    }
    
    const data = sourceSheet.getDataRange().getValues();
    const rowsToArchive = [];
    
    // Encontrar filas completadas (más de 30 días)
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    for (let i = 1; i < data.length; i++) { // Empezar desde 1 para saltar headers
      const timestamp = data[i][CONFIG.COLUMNS.TIMESTAMP];
      const status = data[i][CONFIG.COLUMNS.STATUS];
      
      if (status === CONFIG.STATUS.COMPLETED && timestamp < thirtyDaysAgo) {
        rowsToArchive.push({
          data: data[i],
          rowIndex: i + 1
        });
      }
    }
    
    // Mover filas al archivo
    if (rowsToArchive.length > 0) {
      const lastRow = archiveSheet.getLastRow();
      
      rowsToArchive.forEach((row, index) => {
        archiveSheet.getRange(lastRow + index + 1, 1, 1, 10).setValues([row.data]);
      });
      
      // Eliminar filas del sheet principal (en orden inverso)
      rowsToArchive.reverse().forEach(row => {
        sourceSheet.deleteRow(row.rowIndex);
      });
      
      Logger.log(`${rowsToArchive.length} filas archivadas`);
    }
    
  } catch (error) {
    console.error('Error archivando filas:', error);
    Logger.log('Error archivando filas: ' + error.toString());
  }
}

/**
 * Función para configurar triggers automáticos
 * Ejecutar una vez para configurar los triggers
 */
function setupTriggers() {
  try {
    // Eliminar triggers existentes
    const triggers = ScriptApp.getProjectTriggers();
    triggers.forEach(trigger => {
      if (trigger.getHandlerFunction() === 'onEdit') {
        ScriptApp.deleteTrigger(trigger);
      }
    });
    
    // Crear nuevo trigger para onEdit
    ScriptApp.newTrigger('onEdit')
      .onEdit()
      .create();
    
    Logger.log('Triggers configurados exitosamente');
    
  } catch (error) {
    console.error('Error configurando triggers:', error);
    Logger.log('Error configurando triggers: ' + error.toString());
  }
}

/**
 * Función de utilidad para testing
 */
function testWebhook() {
  const testData = {
    product_url: 'https://www.amazon.com/dp/B08N5WRWNW',
    affiliate_link: 'https://amzn.to/3xyz123',
    row_number: 2
  };
  
  sendWebhookToMake(testData.product_url, testData.affiliate_link, testData.row_number);
}

