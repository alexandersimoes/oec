function make_timeline(container, min, max, init, min_required, callback){
  var margin = {top: 0, right: 0, bottom: 0, left: 0},
      width = container.node().offsetWidth - margin.left - margin.right,
      height = container.node().offsetHeight - margin.top - margin.bottom,
      min_required = min_required || 1,
      grid_height = height / 4,
      axis_height = grid_height * 3,
      tick_width = width / (parseInt(max+1) - parseInt(min));

  var x = d3.time.scale()
      .domain([new Date(parseInt(min), 0, 1), new Date(parseInt(max+1), 0, 1)])
      .range([0, width]);
  
  var start_year = init instanceof Array ? init[0] : parseInt(init);
  var end_year = init instanceof Array ? init[init.length-1] : start_year;
  var brush = d3.svg.brush()
      .x(x)
      .extent([new Date(start_year, 0, 1), new Date(end_year+1, 0, 1)])
      .on("brush", brushed)
      .on("brushend", brushend);

  var svg = container.append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("rect")
      .attr("class", "grid-background")
      .style("fill", "#ddd")
      .attr("width", width)
      .attr("height", grid_height);

  svg.append("g")
      .attr("class", "x grid")
      .attr("transform", "translate(0," + grid_height + ")")
      .call(d3.svg.axis()
          .scale(x)
          .orient("bottom")
          .ticks(d3.time.years, 1)
          .tickSize(-grid_height)
          .tickFormat(""))
    .selectAll(".tick")

  svg.append("g")
      .attr("class", "x axis")
      // .attr("transform", "translate(0," + axis_height/2 + ")")
      .call(d3.svg.axis()
        .scale(x)
        .orient("bottom")
        // .ticks(d3.time.years)
        .ticks(function(start, end){
          var new_end = end.setFullYear(end.getFullYear()-1)
          var interval = (start - new_end) > 20 ? 2 : 1;
          return d3.time.years(start, new_end, interval)
        })
        .tickSize(0)
        .tickPadding(0))
    .selectAll("text")
        .style("font", "11px sans-serif")
        .attr("y", 0)
        .attr("x", 0)
        // .attr("dy", ".35em")
        .attr("transform", function(d){
          var y_offset = tick_width/2;
          var x_offset = axis_height/10;
          return "translate("+(tick_width/2)+", 10)rotate(70)"
        })
        .style("text-anchor", "start");
  
  svg.selectAll(".domain").style("display", "none")
  d3.selectAll(".tick line").style("stroke", "white")

  var gBrush = svg.append("g")
      .attr("class", "brush")
      .style("stroke", "#000")
      .style("fill-opacity", ".125")
      .call(brush);

  gBrush.selectAll("rect")
      .attr("height", grid_height);

  function brushed() {
    var extent0 = brush.extent(),
        extent1;
    
    extent1 = extent0.map(d3.time.year.round);
    
    var min_req_sec = 31536000000 * min_required;
    var time_diff = extent1[1] - extent1[0];
    // console.log(time_diff)
    if (time_diff < min_req_sec) {
      
      if(min_required > 1){
        extent1[0] = d3.time.year.round(d3.time.year.offset(extent0[0], -min_required/2));
        extent1[1] = d3.time.year.round(d3.time.year.offset(extent0[1], min_required/2));
      }
      else {
        extent1[0] = d3.time.year.floor(extent0[0]);
        extent1[1] = d3.time.year.ceil(extent0[1]);
      }
      
    }
    
    d3.select(this).call(brush.extent(extent1));
  }

  function brushend() {
    callback(brush.extent()[0].getFullYear(), brush.extent()[1].getFullYear())
  }
  
}