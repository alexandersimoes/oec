function App() {
  var width = 950, // default width
    height = 500, // default height
    margin = {top: 20, right: 20, bottom: 50, left: 65},
    highlight,
    layout = "value",
    order = "community",
    labels = "on",
    year,
    stroke = 1,
    attr_data,
    data,
    svg,
    viz;

  function stacked(selection) {
    selection.each(function(data, i) {
      
      var chart = {
        width: width-margin.left-margin.right,
        height: height-margin.top-margin.bottom,
        x: margin.left,
        y: margin.top
      }
      
      attr_data = data.attr_data;
      
      years = year.split(".").map(function(y){ return parseInt(y); });
      years = d3.range(years[0], years[1]+1, years[2]);
      
      // trim data to current year and make sure we have attribute data
      current_years_data = data.data.filter(function(d){
        return years.indexOf(d.year) > -1 && attr_data[d.item_id];
      })
      
      var year_totals = d3.nest().key(function(d){return d.year}).rollup(function(leaves){return d3.sum(leaves, function(d){return d.value;})}).entries(current_years_data)
      data_max = layout == "value" ? d3.max(year_totals, function(d){ return d.values; }) : 1;
      var nested_data = nest_data(years, current_years_data)
      
      // Select the svg element, if it exists.
      var svg = d3.select(this).selectAll("svg").data([data]);

      // Otherwise, create the basic structure for the app.
      var svg_enter = svg.enter().append("svg")
        .attr("width",width)
        .attr("height",height)      
      
      // If it's the first time the app is being built, add this group element
      var viz_enter = svg_enter.append("g").attr("class", "viz")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      
      var rect = viz_enter.append('rect')
        .style('stroke','#000')
        .style('stroke-width',stroke)
        .style('fill','#fff')
        .attr('width',chart.width)
        .attr('height',chart.height)
        .attr('x',0)
        .attr('y',0)
      
      var x_scale = d3.scale.linear()
          .domain([years[0],years[years.length-1]])
          .range([0, chart.width])

      var y_scale = d3.scale.linear()
          .domain([0, data_max])
          .range([chart.height, 0])
      
      var x_axis = d3.svg.axis()
        .scale(x_scale)
        .ticks(years.length)
        .tickSize(0)
        .tickPadding(15)
        .tickFormat(function(d, i){
          d3.select(this.parentNode).append("line")
            .attr("x1", 0)
            .attr("x2", 0)
            .attr("y1", 0-stroke)
            .attr("y2", -chart.height+stroke)
            .attr("stroke", "#ccc")
            .attr("stroke-width",stroke/2)
          d3.select(this.parentNode).append("line")
            .attr("x1", 0)
            .attr("x2", 0)
            .attr("y1", 0+stroke)
            .attr("y2", 10)
            .attr("stroke", "#000")
            .attr("stroke-width",stroke)
          return d
        })
        .orient('bottom')
      
      var y_axis = d3.svg.axis()
        .scale(y_scale)
        .tickSize(0)
        .tickPadding(15)
        .tickFormat(function(d, i){
          d3.select(this.parentNode).append("line")
            .attr("x1", 0+stroke)
            .attr("x2", 0+chart.width-stroke)
            .attr("y1", 0)
            .attr("y2", 0)
            .attr("stroke", "#ccc")
            .attr("stroke-width",stroke/2)
          d3.select(this.parentNode).append("line")
            .attr("x1", -10)
            .attr("x2", 0-stroke)
            .attr("y1", 0)
            .attr("y2", 0)
            .attr("stroke", "#000")
            .attr("stroke-width",stroke)
          if(layout == "share"){
            return d3.format("p")(d);
          }
          return format_big_num(d)[0] + format_big_num(d)[1]
        })
        .orient('left')
      
      viz_enter.append('g')
        .attr("transform", "translate(0," + chart.height + ")")
        .attr('class','x_axis_ticks')
                    
      viz_enter.append('g')
        .attr('class','y_axis_ticks')
      
      viz_enter.append('text')
        .attr('width',chart.width)
        .attr('x',chart.width/2)
        .attr('y',chart.height+40)
        .attr('class','axis_title')
        .attr('text-anchor','middle')
        .text("Year")
      
      viz_enter.append('text')
        .attr('width',chart.width)
        .attr('class','axis_title')
        .attr('text-anchor','middle')
        .attr("transform", "translate(" + (chart.x-112) + "," + (chart.y+chart.height/2) + "), rotate(-90)")
        .text("Value (USD)")
      
      d3.select(".x_axis_ticks").call(x_axis)
      d3.select(".y_axis_ticks").call(y_axis)
      
      var offset = layout == "value" ? "zero" : "expand";
      var stack = d3.layout.stack()
          .offset(offset)
          .values(function(d) { return d.values.leaves; })
          .x(function(d) { return d.year; })
          .y(function(d) { return d["value"]; })

      var area = d3.svg.area()
        .interpolate("linear")
        .x(function(d) { return x_scale(d.year); })
        .y0(function(d) { return y_scale(d.y0); })
        .y1(function(d) { return y_scale(d.y0 + d.y); })
      
      /////////////////////////////////////////////////
      // Enter
      //////////////////////////////////////////////////
      var layers = stack(nested_data)
      var paths = d3.select(".viz").selectAll(".layer")
          .data(layers, function(d){ return d.key; })
      
      var height_scale = d3.scale.linear()
        .domain([0, data_max])
        .range([0, 1])
      
      var text_layers = layers.filter(function(d){
        var a = d3.max(d.values.leaves, function(dd){ return height_scale(dd.y); });
        return a > 0.02;
      })
      if(labels == "off"){
        text_layers = []
      }
      
      var texts = d3.select(".viz").selectAll(".name")
          .data(text_layers, function(d){ return d.key; })

      paths.enter().append("path")
        .attr("class", "layer");
      texts.enter().append("text")
        .attr("class", "name");
      
      /////////////////////////////////////////////////
      // Update
      //////////////////////////////////////////////////
      paths
        .attr("d", function(d) { return area(d.values.leaves); })
        .attr("stroke", "none")
        .style("fill", function(d, i) {
          if(attr_data[parseInt(d.key)]){
            if(highlight && highlight != attr_data[parseInt(d.key)].category_id){
              return "#ccc"
            }
            return attr_data[parseInt(d.key)].category_color;
          }
          return "white";
        })
        .on("mousemove", mouseover)
        .on("mouseout", mouseout)
        
      texts
        .attr("x", function(d){
          var max_val = d3.max(d.values.leaves, function(dd){ return dd.value; })
          var largest = d.values.leaves.filter(function(dd){ return dd.value == max_val; })[0]
          return x_scale(largest.year)
        })
        .attr("y", function(d){
          var max_val = d3.max(d.values.leaves, function(dd){ return dd.value; })
          var largest = d.values.leaves.filter(function(dd){ return dd.value == max_val; })[0]
          var height = y_scale(largest.y0 - largest.y) - y_scale(largest.y0 + largest.y);
          return y_scale(largest.y0 + largest.y) + (height/4);
        })
        .attr("text-anchor", function(d){
          var max_val = d3.max(d.values.leaves, function(dd){ return dd.value; })
          var largest = d.values.leaves.filter(function(dd){ return dd.value == max_val; })[0]
          if(years.indexOf(largest.year) == 0) return "start";
          if(years.indexOf(largest.year) == years.length-1) return "end";
          return "middle"
        })
        .attr("fill", function(d){
          return attr_data[parseInt(d.key)].category_text_color;
        })
        .style("text-shadow", "#ddd 1px 1px 3px")
        .style("pointer-events", "none")
        .text(function(d){ return d.values.name; })
      
      /////////////////////////////////////////////////
      // Exit
      //////////////////////////////////////////////////
      paths.exit().remove()
      texts.exit().remove()
      
      // Draw foreground bounding box
      var rect = viz_enter.append('rect')
        .style('stroke','#000')
        .style('stroke-width',stroke*2)
        .style('fill','none')
        .attr('width',chart.width)
        .attr('height',chart.height)
        .attr('x',0)
        .attr('y',0)
            
    })
  }
  
  ////////////////////////////////////////////
  // PRIVATE functions for this app shhhhh...
  ////////////////////////////////////////////
  function mouseover(d){
    d3.select(this)
      .attr("stroke", "black")
      .attr("stroke-width", 2)
    make_mouseover({
      "width": width,
      "title": d.values.name,
      "category": attr_data[d.key].category_name,
      "category_color": attr_data[d.key].category_color,
      "category_text_color": attr_data[d.key].category_text_color
    });
  }
  
  function mouseout(){
    d3.select(this)
      .attr("stroke", "none")
    make_mouseover();
  }
  
  function nest_data(years, data){
    var value_name = "value";
    var nested = d3.nest()
      .key(function(d){return d.item_id})
      .rollup(function(leaves) {
        this_years = leaves.reduce(function(a, b){ return a.concat(b.year)}, [])
        missing_years = diff = years.filter(function(x) { return this_years.indexOf(x) < 0 })
        missing_years.forEach(function(y){ 
          leaves.push({"year": y, "value": 0})
        })
        return {
          "years": leaves.length, 
          "val": d3.sum(leaves, function(d) {return parseFloat(d.value);}),
          "community": attr_data[leaves[0].item_id].category_id,
          "name": attr_data[leaves[0].item_id].name,
          "leaves": leaves.sort(function(a,b){return a.year-b.year;})
        } 
      })
      .entries(data)
    return nested.sort(function(a,b){
      if(a.values[order]<b.values[order]) return 1;
      if(a.values[order]>b.values[order]) return -1;
      return 0;
    });
  }
  
  ////////////////////////////////////////////
  // PUBLIC getter / setter functions
  ////////////////////////////////////////////
  stacked.width = function(value) {
    if (!arguments.length) return width;
    width = value;
    return stacked;
  };

  stacked.height = function(value) {
    if (!arguments.length) return height;
    height = value;
    return stacked;
  };
  
  stacked.year = function(value) {
    if (!arguments.length) return year;
    year = value;
    return stacked;
  };
  
  stacked.highlight = function(value) {
    if (!arguments.length) return highlight;
    highlight = value;
    return stacked;
  };
  
  stacked.labels = function(value) {
    if (!arguments.length) return labels;
    labels = value;
    return stacked;
  };
  
  stacked.layout = function(value) {
    if (!arguments.length) return layout;
    layout = value;
    return stacked;
  };
  
  stacked.order = function(value) {
    if (!arguments.length) return order;
    order = value;
    return stacked;
  };
  
  /////////////////////////////////////////////////////////////////////
  // BE SURE TO ALWAYS RETURN THE APP TO ALLOW FOR METHOD CHAINING
  ///////////////////////////////////////////////////////////////////// 
  return stacked;
}