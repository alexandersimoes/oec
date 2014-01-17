function tabulate(selection, data, columns) {
  var table = d3.select(selection).selectAll("table").data([data]);
      t_enter = table.enter().append("table");
  
  var thead = t_enter.append("thead").append("tr");
  var tbody = t_enter.append("tbody");

  // append the header row
  table.select("thead tr")
      .selectAll("th")
      .data(columns)
      .enter()
      .append("th")
  
  // update
  table.selectAll("th").text(function(column) { return column; });
  
  // create a row for each object in the data
  table.select("tbody").selectAll("tr")
      .data(data)
      .enter()
      .append("tr");
  
  var rows = table.selectAll("tbody tr")
  
  // create a cell in each row for each column
  var cells = rows.selectAll("td")
      .data(function(row) {
          return columns.map(function(column) {
              return {column: column, value: row[column]};
          });
      })
      .enter()
      .append("td")
  
  rows.selectAll("td")
      .text(function(d) { return d.value; });
  
  return table;
}