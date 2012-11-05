function build_app(api_uri, type_of_app, dimensions, embed){
  
  // show loading icon and clear current HTML container
  d3.select("#dataviz").html("")
  d3.select("#loader").style("display", "block");
  
  // get data from server
  d3.json(api_uri, function(data){
    // build the app with data from server
    build(data, dimensions)
    // hide loading icon
    d3.select("#loader").style("display", "none");
  })
  
  // Given raw data from the server clean it and build an app
  function build(data, dimensions){
    
    // clean up attribute data
    data.attr_data = clean_attr_data(data.attr_data)
    var showing = data.item_type;
    
    // initialize the app (build it for the first time)
    app = App()
      .width(dimensions[0])
      .height(dimensions[1])
      .year(data.year)

    // call app function (depending on which is loaded with the page)
    // on the given selection(s)
    d3.select("#dataviz")
      .style("height", dimensions[1]+"px")
      .datum(data)
      .call(app);

    if(!embed){
      key = Key()
        .classification(data.other.product_classification)
        .showing(showing)

      timeline = Timeline()
        .app_type(type_of_app)
        .year(year)

      controls = Controls()
        .app_type(type_of_app)
        .year(year)
    
      d3.select(".key")
        .datum(data.attr_data)
        .call(key);
    
      d3.select("#timeline")
        .datum(data.data)
        .call(timeline);

      d3.select("#tool_pane")
        .datum(data)
        .call(controls);
    }
  }
  
}

function clean_attr_data(attrs){
  // replace certain keys with common names used generically throughout apps
  attrs.forEach(function(attr){
    var id_property = attr["community_id"] ? "community_id" : "region_id",
      name_property = attr["community__name"] ? "community__name" : "region__name",
      color_property = attr["community__color"] ? "community__color" : "region__color",
      text_color_property = attr["community__text_color"] ? "community__text_color" : "region__text_color";
    attr["category_id"] = attr[id_property]; delete attr[id_property];
    attr["category_name"] = attr[name_property]; delete attr[name_property];
    attr["category_color"] = attr[color_property]; delete attr[color_property];
    attr["category_text_color"] = attr[text_color_property]; delete attr[text_color_property];
    attr["heirarchical_id"] = attr["category_id"].toString().substr(0,1) + "." + attr["category_id"] + "." + attr["id"];
  })

  // turn flat attributes array into indexed object with ids
  // either country or products as the key
  attrs = d3.nest()
    .key(function(d) { return d["id"]; })
    .rollup(function(d){ return d[0] })
    .map(attrs);

  // return this cleaned up version
  return attrs
}

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

function make_mouseover(options){
  if(!options){
    $("#mouseover").remove();
    return;
  }
  if($("#mouseover").length){
    $("#mouseover").remove();
  }
  
  var cont = $("<div id='mouseover'>").appendTo("#dataviz");
  
  var cat = $("<div id='mouseover_cat'>").appendTo("#mouseover");
  cat.css("background", options.category_color)
  cat.css("color", options.category_text_color)
  cat.text(options.category)
  
  var title = $("<div id='mouseover_title'>").appendTo("#mouseover");
  title.text(options.title)
  
  if(options.values){
    var table = $("<table id='mouseover_table'>").appendTo("#mouseover");
    options.values.forEach(function(v){
      var tr = $("<tr>").appendTo(table);
      tr.append("<td>"+v[0]+"</td>")
      tr.append("<td>"+v[1]+"</td>")
    })
  }
  
  var left = d3.mouse(d3.select("#dataviz").node())[0];
  left = (left + $("#mouseover").width()/2) > options.width ? options.width - $("#mouseover").width()/2 : left;
  left = (left - $("#mouseover").width()/2) < 0 ? $("#mouseover").width()/2 : left;
  
  var top = d3.mouse(d3.select("#dataviz").node())[1] - $("#mouseover").height() - 40;
  top = top < 0 ? d3.mouse(d3.select("#dataviz").node())[1] + 40 : top;
  
  cont.css({
    "left": left - ($("#mouseover").width()/2),
    "top":  top
  })
}

function get_root(d){
  if(!d.parent){ 
    return d
  }
  return get_root(d.parent)
}