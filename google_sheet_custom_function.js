function onOpen() {
    var ui = SpreadsheetApp.getUi();
    ui.createMenu('Monday.com')
        .addItem('Fetch Data', 'fetchMondayData')
        .addToUi();
  }
  
  function fetchMondayData() {
    var mondayApiKey = 'INSERT_API_KEY_HERE';
    var mondayApiUrl = 'https://api.monday.com/v2';
    
    var query = '{boards(ids: 1642180441) { name id description items_page { items { name column_values { column { title } text } } } } }';
    
    var options = {
      'method': 'post',
      'headers': {
        'Authorization': mondayApiKey,
        'Content-Type': 'application/json'
      },
      'payload': JSON.stringify({ 'query': query })
    };
    
    var response = UrlFetchApp.fetch(mondayApiUrl, options);
    var data = JSON.parse(response.getContentText());
    
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.clear();
    
    // Add headers
    var headers = ['Name', 'Area', 'Postcode/Address', 'Do you have diabetes (any type)?', 'Delivery instructions', 'Bag delivery date', 'Deliverer'];
    sheet.appendRow(headers);
    
    // Add data
    var items = data.data.boards[0].items_page.items;
    items.forEach(function(item) {
      var row = [item.name];
      
      headers.slice(1).forEach(function(header) {
        var columnValue = item.column_values.find(cv => cv.column.title === header);
        row.push(columnValue ? columnValue.text : '');
      });
      
      sheet.appendRow(row);
    });    
    
    // Format the table
    var dataRange = sheet.getRange("A1:G17");
    var headerRange = sheet.getRange("A1:G1");
    dataRange.setBorder(true, true, true, true, true, true);
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#b6d7a8");
    
    SpreadsheetApp.getUi().alert('Data fetched successfully!');
  }