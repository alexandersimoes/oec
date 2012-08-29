function find_parent(e, name){
  if(e.nodeName == name){
    return e;
  }
  return find_parent(e.parentNode, name);
}

function format_big_num(d){
  d = parseFloat(d);
  var n = d;
  var s = "";
  var sign = "";
  if(d < 0){
    sign = "-"
  }
  d = Math.abs(d);
  if(d >= 1e3){
    n = d3.format(".2r")(d/1e3);
    s = "k";
  }
  if(d >= 1e6){
    n = d3.format(".2r")(d/1e6);
    s = "M";
  }
  if(d >= 1e9){
    n = d3.format(".2r")(d/1e9);
    s = "B";
  }
  if(d >= 1e12){
    n = d3.format(".2r")(d/1e12);
    s = "T";
  }
  if(d == 0){
    n = 0;
  }
  return [sign+n, s];
}

function make_mouseover(element, dimensions, data, padding){
  // unpack function parameters
  var w = dimensions[0],
    h = dimensions[1],
    title = data.title,
    img_src = data.img_src,
    sub_text = data.sub_text,
    svg = find_parent(element, "svg"),
    info_h = 36,
    edge_padding = info_h * .10,
    padding = padding ? padding : 0;
  
  // var padding = info_h * .10;
  // create grouping
  var info = d3.select(svg).append("g")
    .attr("class", "info")
    .attr("transform", function(d){
      var mouse_y = d3.svg.mouse(svg)[1];
      var y = mouse_y > (h - info_h - padding) ? 0 : h - info_h - padding;
      return "translate(0, "+y+")";
    })
  // create semi-transparent background
  info.append("rect")
    .attr("fill", "black")
    .attr("opacity", 0.5)
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", w)
    .attr("height", info_h)
  // <image xlink:href="firefox.jpg" x="0" y="0" height="50px" width="50px"/>
  info.append("image")
    .attr("xlink:href", img_src)
    .attr("x", edge_padding)
    .attr("y", edge_padding)
    .attr("height", info_h-edge_padding*2)
    .attr("width", info_h-edge_padding*2)
  info.append("text")
    .attr("x", edge_padding + info_h)
    .attr("y", edge_padding)
    .attr("dy", info_h/2 - edge_padding)
    .attr("font-size", 16)
    .attr("font-weight", "bold")
    .attr("fill", "white")
    .style("text-shadow", "1px 1px 2px black")
    .text(title)
  info.append("text")
    .attr("x", edge_padding + info_h)
    .attr("y", info_h - (edge_padding*2))
    .attr("dy", info_h/4 - (edge_padding*2))
    .attr("font-size", 12)
    .attr("fill", "white")
    .style("text-shadow", "1px 1px 2px black")
    .text(sub_text)
}