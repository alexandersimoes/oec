function Controls() {
  var year = 1962,
    attr_data,
    this_years_data,
    app_type,
    columns;
    
  function controls(selection) {
    selection.each(function(data, i) {
      
      // Update year in title
      var year_title = year;
      if(year_title.indexOf(".") > -1){
        year_title = year_title.replace(".", " ")
        year_title = year_title.substr(0, year_title.indexOf("."))
      }
      $(".app_title#icons h2").text(year_title)
      
      // Update year in dropdown
      if(app_type == "stacked"){
        var years = year.split(".").map(function(y){ return parseInt(y); });
        years = d3.range(years[0], years[1]+1, years[2]);
        $(".dropdown_container#year_start select").val(years[0]);
        $(".dropdown_container#year_end select").val(years[years.length-1]);
        $(".dropdown_container#year_interval select").val(years[1] - years[0]);
        $(".dropdown_container#year_start select").trigger("liszt:updated");
        $(".dropdown_container#year_end select").trigger("liszt:updated");
        $(".dropdown_container#year_interval select").trigger("liszt:updated");
      }
      else{
        $(".dropdown_container#year select").val(year);
        $(".dropdown_container#year select").trigger("liszt:updated");
      }
      
      // Update embed link
      var embed_link = document.location.href.replace("explore", "embed").split("/");
      embed_link[embed_link.length-2] = year
      $("input.embed_code").val("<iframe width='560' height='315' src='"+embed_link.join("/")+"' frameborder='0'></iframe>")
      
      // Set on click event for "view as text" button, ie trigger table view
      d3.selectAll("#view_as_text a").on("click", toggle_view_table)
      // Set click event for download links
      d3.selectAll("#download a").on("click", download)
      // Build new app when button is clicked
      d3.select("button#build").on("click", new_app)
      // Actions for selecting the embed link
      d3.select("#tool_pane .embed_code").on("click", embed_link_click)
      // Change the product classification
      $(".product_class select").chosen().change(function(){
        // set session data to new product classificaiton
        var prod_class = $(this).val();
        window.location = "/set_product_classification/"+prod_class+"/";
      });
      
      // Make the table for "view as text"
      // 
      // Change columns headers depending on if the visualization
      // is showing products or countries
      columns = {"year": "Year", "code": "Code", "name": "Name", 
        "rca": "RCA", "share": "Share", "value": "Value"}
      if(data.item_type == "country"){
        columns = {"year": "Year", "name_3char": "Abbrv", "name": "Name", 
          "rca": "RCA", "share": "Share", "value": "Value"}
      }
      // set attr_data for private funcitons to have access to
      attr_data = data.attr_data;
      
      // Filter data to this only values with the year set to this year
      var years = [parseInt(year)]
      if(app_type == "stacked"){
        years = year.split(".").map(function(y){ return parseInt(y); });
        years = d3.range(years[0], years[1]+1, years[2]);
      }
      this_years_data = data.data.filter(function(d){ return years.indexOf(d.year) > -1; })
        .sort(function(a, b){
          if (b.year < a.year) { return -1; } 
          else if (b.year > a.year) { return 1; } 
          else { return b.value - a.value; }
        })
      // Get the sum for calculating share
      this_years_sum = d3.sum(this_years_data, function(d) { return d.value; })
      
      // Select the table element, if it exists.
      var table = d3.select("#text_data").selectAll("table").data([this_years_data]);

      // Otherwise, create the basic structure for the table to be.
      var table_enter = table.enter().append("table");
    
      // If it's the first time the app is being built, add the columns
      table_enter.append("thead").append("tr").selectAll("td")
        .data(d3.values(columns)).enter()
          .append("td")
          .text(function(d){ return d; })
      
      table_enter.append("tbody")
      
      var data_rows = table.select("tbody").selectAll("tr")
        .data(this_years_data, function(d){ return d.year; })
      
      // Add all the things to the table!!!
      data_rows.enter().append("tr")
        .call(tbody_tr)
      
      // take out old rows of data
      data_rows.exit().remove()
      
    })
  }

  ////////////////////////////////////////////
  // PUBLIC getter / setter functions
  ////////////////////////////////////////////
  controls.year = function(value) {
    if (!arguments.length) return year;
    year = value;
    return controls;
  };
  
  controls.app_type = function(value) {
    if (!arguments.length) return app_type;
    app_type = value;
    return controls;
  };
  
  ////////////////////////////////////////////
  // PRIVATE functions for this app shhhhh...
  ////////////////////////////////////////////
  function tbody_tr(rows){
    d3.keys(columns).forEach(function(c){
      rows.append("td").text(function(d){
        var attr = attr_data[d.item_id]
        if(!attr){
          return ""
        }
        // if(c == "code"){
        //   console.log(d, c)
        // }
        if(c == "share"){
          return d3.format(".2%")(d["value"] / this_years_sum);
        }
        if(attr[c]){
          return pretty(attr[c]);
        }
        return pretty(d[c]);
      })
    })
  }
  
  function pretty(n){
    // floating point 2 decimal places
    if(typeof n === 'number' && n % 1 != 0){
      return d3.format(",.2f")(n)
    }
    // integer excluding years
    else if(typeof n === 'number' && !(n>1961 && n<2012)){
      return d3.format(",f")(n)
    }
    // straight text or years
    return n;
  }
  
  function toggle_view_table(){
    if(d3.select("#text_data").style("display") == "none"){
      d3.select(this).select("span").text("View app")
      d3.select("#dataviz").style("display", "none")
      d3.event.preventDefault();
      return d3.select("#text_data").style("display", "block")
    }
    d3.select(this).select("span").text("View as text")
    d3.select("#dataviz").style("display", "block")
    d3.event.preventDefault();
    return d3.select("#text_data").style("display", "none")
  }
  
  function download(){
    // Get the d3js SVG element
    // var svg = document.getElementById("ex1");
    // Extract the data as SVG text string
    // var svg_xml = (new XMLSerializer).serializeToString(svg);

    // Submit the <FORM> to the server.
    // The result will be an attachment file to download.
    // var form = document.getElementById("svgform");
    // form['output_format'].value = output_format;
    // form['data'].value = svg_xml ;
    // form.submit();

    var title = window.location.pathname.split("/")
    title.splice(0, 1)
    title.splice(0, 1)
    title.splice(title.length-1, 1)
    $("input[name='title']").val(title.join("_"));

    var svg = d3.select("svg")
      .attr("title", title.join("_"))
      .attr("version", 1.1)
      .attr("xmlns", "http://www.w3.org/2000/svg")

    // Add this content as the value of input
    var svg_xml = (new XMLSerializer).serializeToString(svg.node());
    $("input[name='content']").val(svg_xml)
    
    var format = $(this).attr("class");
    $("input[name='format']").val(format);
    
    // Submitting the form will trigger the action with will bring up
    // the /export page. The view for this page takes the values from
    // POST request and prompts the user to download the file
    $('form.download').submit();
    d3.event.preventDefault();
  }
  
  function new_app(){
    // set defaults
    var uri_parts = ["trade_flow", "country1", "country2", "product", "year"]
    var uri_replacements = [trade_flow, country1, country2, product, year]
    // replace defaults with values from control pane
    uri_parts.forEach(function(uri_item, i){
      if($(".dropdown_container#"+uri_item).length){
        uri_parts[i] = $(".dropdown_container#"+uri_item+" select").val();
      }
      else {
        uri_parts[i] = uri_replacements[i];
      }
      // handle if stacked with start and end years
      if(uri_item == "year" && app_type == "stacked"){
        year_start = $(".dropdown_container#year_start :selected").val()
        year_end = $(".dropdown_container#year_end :selected").val()
        year_interval = $(".dropdown_container#year_interval :selected").val()
        uri_parts[i] = year_start+"."+year_end+"."+year_interval;
      }
    })
    new_url = "/explore/" + app_name + "/" + uri_parts.join("/") + "/";
    return window.location = new_url;
  }
  
  function embed_link_click(){
    this.focus();
    this.select();
  }
  
  /////////////////////////////////////////////////////////////////////
  // BE SURE TO ALWAYS RETURN THE APP TO ALLOW FOR METHOD CHAINING
  ///////////////////////////////////////////////////////////////////// 
  return controls;
}