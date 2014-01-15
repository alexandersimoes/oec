function make_timeline(container, min, max, init, min_required, callback){
  var margin = {top: 5, right: 10, bottom: 5, left: 0},
      width = container.node().offsetWidth - margin.left - margin.right,
      height = container.node().offsetHeight - margin.top - margin.bottom,
      min_required = min_required || 1;

  var x = d3.time.scale()
      .domain([new Date(min, 0, 1), new Date(max+1, 0, 1)])
      .range([0, width]);

  var brush = d3.svg.brush()
      .x(x)
      .extent([new Date(init, 0, 1), new Date(init+1, 0, 1)])
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
      .attr("height", height/2);

  svg.append("g")
      .attr("class", "x grid")
      .attr("transform", "translate(0," + height/2 + ")")
      .call(d3.svg.axis()
          .scale(x)
          .orient("bottom")
          .ticks(d3.time.years, 1)
          .tickSize(-height)
          .tickFormat(""))
    .selectAll(".tick")

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height/2 + ")")
      .call(d3.svg.axis()
        .scale(x)
        .orient("bottom")
        // .ticks(d3.time.years)
        .ticks(function(start, end){
          var new_end = end.setFullYear(end.getFullYear()-1)
          return d3.time.years(start, new_end, 2)
        })
        .tickPadding(0))
    .selectAll("text")
        .attr("y", function(d){
          return -this.getBBox().width/6
          // return -this.getBBox().width
        })
        .style("font", "11px sans-serif")
        .attr("x", 4)
        // .attr("y", 0)
        .attr("dy", ".35em")
        .attr("transform", "rotate(70)")
        .style("text-anchor", "start");
  
  svg.selectAll(".domain").style("display", "none")
  d3.selectAll(".tick line").style("stroke", "white")

  var gBrush = svg.append("g")
      .attr("class", "brush")
      .style("stroke", "#000")
      .style("fill-opacity", ".125")
      .call(brush);

  gBrush.selectAll("rect")
      .attr("height", height/2);

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