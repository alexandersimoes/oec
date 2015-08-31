// WARNING: Do not edit the contents of this file. It is compiled dynamically
// from multiple source files located in the assets/js directory.

var configs = {};

var visualization = function(build, container) {

  var trade_flow = build.trade_flow,
      default_config = configs["default"](build),
      viz_config = configs[build.viz.slug](build, container);

  var viz = d3plus.viz()
              .container(container)
              .config(default_config)
              .config(viz_config)
              .error("Loading Visualization")
              .draw();

  /* need to grab json network file for rings and product space */
  if(build.viz.slug == "network" || build.viz.slug == "rings"){
    var network_file = "/static/json/network_hs4.json";
    if(build.viz.slug == "rings" && build.prod.id.length == 8){
      network_file = "/static/json/network_hs6.json";
    }
    viz.nodes(network_file, function(network){
      viz.edges(network.edges);
      return network.nodes;
    })
  }

  /* Need to set text formatting in HTML for translations */
  viz.format({"text": function(text, key, vars){

      if(key){
        if(key.key === "display_id"){
          return text.toUpperCase();
        }
      }

      if(text){

        if(text === "display_id"){
          if(build.attr_type == "origin" || build.attr_type == "dest"){
            return oec.translations["id"];
          }
          else {
            return build.attr_type.toUpperCase() + " ID";
          }
        }

        if(d3.keys(oec.translations).indexOf(text) > -1){
          return oec.translations[text];
        }

        if (text === "trade") {
          return "Trade in USD";
        }

        if(text.indexOf("Values") >= 0 && !key){
          return trade_flow.charAt(0).toUpperCase() + trade_flow.substr(1).toLowerCase() + " " + text;
        }

        return d3plus.string.title(text, key, vars);
      }
    }
  })

  /* If not on the explore page, show the title! */
  if (window.parent.location.href.indexOf("/explore/") < 0 || window.parent.location.href.indexOf("/embed/") > 0) {
    viz.title(build.title);
  }

  load(build.attr_url, function(raw_attrs){
    var attrs = format_attrs(raw_attrs, build);

    /* unleash the dogs... make the AJAX requests in order to the server and when
       they return execute the go() func */
    d3.json(build.data_url, function(error, raw_data){
      var data = format_data(raw_data, attrs, build);

      var csv_data = format_csv_data(data, attrs, build);

      viz.data(data)
        .attrs(attrs)
        .error(false)
        .ui(viz.ui().concat([{"method":download(container, csv_data), "value":["Download"], "type":"button"}]))
        .draw();

      d3.select("#viz")
        .style("display", "block");

    });

  })

  return viz;

}

function share(build){
  return function(){
    // var lang = build.lang;
    var lang = "en";
    var same_origin = window.parent.location.host == window.location.host;
    var url = encodeURIComponent(window.location.pathname + "?lang="+lang)
    if(same_origin){
      if(window.location != window.parent.location){
        var url = encodeURIComponent(window.parent.location.pathname + "?lang="+lang)
      }
    }
    // make post request to server for short URL
    d3.json("/"+lang+"/explore/shorten/")
      .header("Content-type","application/x-www-form-urlencoded")
      .post("url="+url, function(error, data) {
        if (data.error) {
          console.log(data.error)
        }
        else{
          d3.select("#short").style("display", "block")
          d3.selectAll(".modal#share input.short_url").property("value", "http://"+location.host+"/"+data.slug)
        }
      })
    // set social media link URLs
    d3.selectAll(".modal-body a#Facebook").attr("href", build.social.facebook)
    d3.selectAll(".modal-body a#Twitter").attr("href", build.social.twitter)
    d3.selectAll(".modal-body a#Google").attr("href", build.social.google)
    // open modal window
    d3.selectAll(".modal#share").classed("active", true)
  }
}

configs.default = function(build) {

  /*  If we're looking at countries their icons are flags and we don't
      want to show the colored background because the flags don't take up
      100% of the icon square.

      Also we want to show RCA if we're looking at products. */
  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var icon = {"value":"icon", "style":{"nest":"knockout","id":"default"}};
    var id_nesting = ["nest", "id"];
    var tooltip_data = ["display_id", build.trade_flow+"_val"];
  }
  else {
    var icon = {"value":"icon", "style":"knockout"};
    var id_nesting = ["nest", "nest_mid", "id"];
    var tooltip_data = ["display_id", build.trade_flow+"_val", build.trade_flow+"_rca"]
  }

  var background = "none", curtain = "black";
  if(window.parent.location.host == window.location.host){
    background = "#eeeeee", curtain = background;
  }

  var tooltip = {
      "curtain": {"color": curtain},
      "html": {
        "url": function(focus_id){
          var display_id = focus_id.substring(2);
          var attr_type = build.attr_type.indexOf("hs") >= 0 ? "prod_id" : build.attr_type+"_id";
          return "/en/explore/builds/?classification="+build.classification+"&"+attr_type+"="+display_id;
        },
        "callback":function(data){
          var html_str = '<h3>Related Visualizations</h3>'
          data.builds.forEach(function(b){
            html_str += "<a target='_top' href='/en/explore/"+b.url+"' class='related'>"+b.title+"</a>";
          })
          html_str += "<hr />";
          html_str += "<a style='background-color:"+data.profile.color+";color:"+d3plus.color.text(data.profile.color)+";' target='_top' href='"+data.profile.url+"' class='profile'><img src='"+data.profile.icon+"' />"+data.profile.title+"</a>";
          return html_str;
        }
      },
      "small": 225,
      "value": tooltip_data
    }

  return {
    "aggs": {
      "export_val_growth_pct": "mean",
      "export_val_growth_pct_5": "mean",
      "export_val_growth_val": "mean",
      "export_val_growth_val_5": "mean",
      "import_val_growth_pct": "mean",
      "import_val_growth_pct_5": "mean",
      "import_val_growth_val": "mean",
      "import_val_growth_val_5": "mean",
      "distance": "mean",
      "opp_gain": "mean",
      "pci": "mean",
      "eci": "mean",
      "export_rca": "mean",
      "import_rca": "mean"
    },
    "background": background,
    "color": { "heatmap": ["#cccccc","#0085BF"] },
    "focus": {"tooltip": false},
    "format": {
      "number": function( number , key , vars ){
        var key = key.key;
        if(key && key.index){
          if(key.indexOf("pct") > -1){ return d3.format(".2%")(number); }
          if(key == "year"){ return number; }
        }
        var ret = d3plus.number.format( number , {"key":key, "vars":vars})
        if (key && ["export_val","import_val","net_export_val","net_import_val"].indexOf(key) >= 0) {
          ret = "$"+ret
        }
        return ret
      }
    },
    "icon": icon,
    "id": id_nesting,
    "legend": {"filters":true},
    "messages": {"branding": true, "style": "large"},
    "size": {
      "value": build.trade_flow+"_val",
      "threshold": false
    },
    "text": {"nest":"name", "id":["name", "display_id"]},
    "time": {"value": "year", "solo": build.year },
    "title": {
      "font": {
        "weight": 800
      }
    },
    "tooltip": tooltip,
    "type": build.viz.slug,
    "x": {
      "label": {
        "font": {
          "size": 16
        }
      }
    },
    "y": {
      "label": {
        "font": {
          "size": 16
        }
      }
    }
  }

}

configs.geo_map = function(build, container) {
  return {
    "color": build.trade_flow+"_val",
    "coords": {
      "center": [10,0],
      "padding": 0,
      "mute": ["anata"],
      "value": "/static/json/country_coords.json"
    },
    "depth": 1,
    "size": "export_val",
    "x": "eci",
    "y": {
      "scale": "log",
      "value": build.trade_flow
    },
    "ui": [
      {"method":show_all_years, "value":["Show all years"], "type":"button"},
      {"method":"color", "value": [
        {"Value": build.trade_flow+"_val"},
        {"Annual Growth Rate (1 year)": build.trade_flow+"_val_growth_pct"},
        {"Annual Growth Rate (5 year)": build.trade_flow+"_val_growth_pct_5"},
        {"Growth Value (1 year)": build.trade_flow+"_val_growth_val"},
        {"Growth Value (5 year)": build.trade_flow+"_val_growth_val_5"},
      ]},
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}

configs.line = function(build, container) {
  return {
    "color": function(d){ 
      if(d.name=="Exports"){ return "#0b1097" } 
      else{ return "#c8140a" } 
    },
    "depth": 0,
    "id": "test",
    "x": "year",
    "y": "trade",
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}

function change_layout(new_layout){
  var network_file = "/static/json/"+new_layout+".json";
  viz.nodes(network_file, function(network){
    viz.edges(network.edges);
    return network.nodes;
  }).draw();
}

configs.network = function(build, container) {
  return {
    "active": {
      "value": function(d){
        return d.export_rca >= 1;
      },
      "spotlight":true      
    },
    "color": "color",
    "depth": 1,
    // "edges": {
    //     "value": "/static/json/just_edges.json",
    //     "callback": function(network){
    //       return network.edges
    //     }
    // },
    "id": ["nest","id"],
    "nodes": {
      "overlap": 1.1,
    },
    // "nodes": {
    //   "overlap": 1.1,
    //   "value": {
    //     "value": "/static/json/just_nodes.json",
    //     "callback": function(network){
    //       return network.nodes
    //     }
    //   }
    // },
    "size": "export_val",
    "ui": [
      {"method":change_layout, "label":"Layout", "value":[
        {"Force Directed":"network_hs4"}, 
        {"Circular Spring":"network_hs4_circular_spring"},
        {"FR":"network_hs4_fr"},
        {"Complexity Circles":"network_hs4_complexity_circles"},
        {"Community Circles":"network_hs4_community_circles"},
        {"Community Rectangles":"network_hs4_community_rectangles"},
      ]},
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}

configs.rings = function(build, container) {
  return {
    "active": {
      "value": function(d){
        return d.export_rca >= 1;
      },
      "spotlight":true      
    },
    "color": "color",
    "focus": build.prod.id,
    "id": ["nest","id"],
    "depth": 1,
    "size": "export_val",
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}

configs.scatter = function(build, container) {
  return {
    "color": "color",
    "depth": 1,
    "size": "export_val",
    "x": "eci",
    "y": {
      "scale": "log",
      "value": build.trade_flow
    },
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}

configs.stacked = function(build, container) {
  function change_layout(new_layout){
    viz.y({"scale": new_layout}).draw();
  }
  
  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var depth_ui = {"method":"depth", "value":[{"Continent": 0}, {"Country":1}], "label":"Depth"}
  }
  else {
    var depth_ui = {"method":"depth", "value":[{"HS2": 0}, {"HS4":1}], "label":"Depth"}
  }
  
  return {
    "depth": 1,
    "shape": "area",
    "x": "year",
    "y": {"scale": "linear"},
    "color": "color",
    "order": "nest",
    "ui": [
      depth_ui,
      {"method":change_layout, "value":[{"Value": "linear"}, {"Share": "share"}], "label":"Layout"},
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}


function show_all_years(){
  // remove show all years ui element
  var ui = viz.ui().filter(function(u){
    return u.value[0] != "Show all years"
  })
  
  // hide viz and show "loading"
  d3.select("#viz").style("display", "none");
  d3.select("#loading").style("display", "block");
  
  // reformat data url aka replace current year with "all"
  var data_url = build.data_url;
  data_url = data_url.split("/");
  data_url[3] = "all";
  data_url = data_url.join("/");
  
  var q = queue()
    .defer(d3.json, data_url)
    .defer(d3.json, build.attr_url)
    .await(function(error, raw_data, raw_attrs){
  
      var attrs = format_attrs(raw_attrs, build)
      var data = format_data(raw_data, attrs, build)
     
      viz.data(raw_data.data).attrs(attrs).ui(ui).draw();
      
      d3.select("#viz").style("display", "block");
      d3.select("#loading").style("display", "none");

    });

}

configs.tree_map = function(build, container) {
  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var depth_ui = {"method":"depth", "value":[{"Continent": 0}, {"Country":1}], "label":"Depth"}
  }
  else {
    var depth_ui = {"method":"depth", "value":[{"HS2": 0}, {"HS4":1}, {"HS6":2}], "label":"Depth"}
  }
  
  return {
    "depth": 1,
    "shape": "square",
    "labels": {"align": "start", "valign":"top"},
    "color": "color",
    "zoom": false,
    "ui": [
      depth_ui,
      {"method":show_all_years, "value":["Show all years"], "type":"button"},
      {"method":"color", "value": [
        {"Category": "color"},
        {"Annual Growth Rate (1 year)": build.trade_flow+"_growth_pct"},
        {"Annual Growth Rate (5 year)": build.trade_flow+"_growth_pct_5"},
        {"Growth Value (1 year)": build.trade_flow+"_growth_val"},
        {"Growth Value (5 year)": build.trade_flow+"_growth_val_5"},
      ]},
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}

function format_data(raw_data, attrs, build){

  var data = raw_data.data;
  var opposite_trade_flow = build.trade_flow == "export" ? "import" : "export";
  var attr_id = attr_id = build.attr_type + "_id";

  // go through raw data and set each items nest and id vars properly
  // also calculate net values
  data.forEach(function(d){
    d.nest = d[attr_id].substr(0, 2)
    if(attr_id.indexOf("hs") == 0){
      d.nest_mid = d[attr_id].substr(0, 6)
    }
    d.id = d[attr_id]
    var net_val = parseFloat(d[build.trade_flow+"_val"]) - parseFloat(d[opposite_trade_flow+"_val"]);
    if(net_val > 0){
      d["net_"+build.trade_flow+"_val"] = net_val;
    }
  })

  // special case for line chart of trade balance (need to duplicate data)
  if(build.viz.slug == "line"){
    // data = data.map(function(d){
    //   d.trade = d.export_val - d.import_val;
    //   // d.id = d.id + "_export";
    //   d.name = "Exports";
    //   return d;
    // })
    data = data.map(function(d){
      d.trade = d.export_val;
      // d.id = d.id + "_export";
      d.test = d.id + "_export";
      d.name = "Exports";
      return d;
    })
    var clones = d3plus.util.copy(data);
    var clones = clones.map(function(d){
      // var x = JSON.parse(JSON.stringify(d));
      var x = d
      x.trade = x.import_val;
      // x.id = x.id + "_import";
      d.test = d.id + "_import";
      x.name = "Imports"
      return x;
    })
    data = data.concat(clones);
  }

  return data;

}

function format_attrs(raw_attrs, build){
  var attrs = {};
  var attr_id = attr_id = build.attr_type + "_id";

  raw_attrs.data.forEach(function(d){
    d.nest = d.id.substr(0, 2);
    attrs[d.id] = d
    if(attr_id == "origin_id" || attr_id == "dest_id"){
      attrs[d.id]["icon"] = "/static/img/icons/country/country_"+d.id+".png"
    }
    else if(attr_id.indexOf("hs") == 0){
      attrs[d.id]["icon"] = "/static/img/icons/hs/hs_"+d.id.substr(0, 2)+".png"
    }
    else if(attr_id == "sitc_id"){
      attrs[d.id]["icon"] = "/static/img/icons/sitc/sitc_"+d.id.substr(0, 2)+".png"
    }
  })

  // for geo map, get rid of small island nations that don't exist
  // in geography
  if(build.viz.slug == "geo_map"){
    delete attrs["octkl"]
    delete attrs["octon"]
    delete attrs["ocwlf"]
    delete attrs["ocwsm"]
  }

  return attrs;
}

function format_csv_data(data, attrs, build){
  csv_data = [];
  ccp = ["origin", "dest", "prod"]

  // format columns
  var show_id = build.attr_type + "_id";
  var trade_flow = build.trade_flow + "_val";
  csv_data.push(['year', 'country_origin_id', 'country_destination_id', build.classification+'_product_id', trade_flow, trade_flow+"_pct"])

  // format data
  var total_val = d3.sum(data, function(d){ return d[trade_flow]; });
  data.forEach(function(d){
    if(d[trade_flow]){
      var attr = attrs[d[show_id]]
      datum = [d['year']]
      ccp.forEach(function(x){
        if(build[x] == "show"){
          datum.push(attr["display_id"] ? attr["display_id"].toUpperCase() : attr["id"].substring(2).toUpperCase())
        }
        else if(build[x] == "all"){
          datum.push("ALL")
        }
        else {
          datum.push(build[x].display_id.toUpperCase())
        }
      })
      var this_pct = (d[trade_flow]/total_val)*100
      datum.push(d[trade_flow])
      datum.push(d3.format(",.2g")(this_pct)+"%")
      csv_data.push(datum)
    }
  })

  return csv_data;
}

function download(container, csv_data){
  return function(){
  
    d3.selectAll(".modal#download").classed("active", true)
    d3.selectAll(".modal#download a.download_button").on("click", function(){
      
      var format = d3.select(this).attr("id");
      
      var title = window.location.pathname.split("/")
      title.splice(0, 1)
      title.splice(0, 1)
      title.splice(title.length-1, 1)
      title = title.join("_").replace("embed", "explore")
      
      if(format == "svg" || format == "png"){
        var svg = d3.select(container).select("svg")
          .attr("title", title)
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg")

        // Add this content as the value of input
        var content = (new XMLSerializer).serializeToString(svg.node());
      }
      else if(format == "csv"){
        // var content = d3.csv.format(csv_data);
        var content = JSON.stringify(csv_data);
      }
      
      var form = d3.select("body").append("form").attr("id", "download").attr("action", "/en/explore/download/").attr("method", "post");
      form.append("input").attr("type", "text").attr("name", "content").attr("value", content);
      form.append("input").attr("type", "text").attr("name", "format").attr("value", format);
      form.append("input").attr("type", "text").attr("name", "title").attr("value", title);
      
      form.node().submit();
      
      d3.event.preventDefault();
      
    })
  }
  
}
var load = function(url, callback) {

  localforage.getItem("cache_version", function(error, c){

    if (c !== cache_version) {
      localforage.clear();
      localforage.setItem("cache_version", cache_version, loadUrl);
    }
    else {
      loadUrl();
    }

    function loadUrl() {

      localforage.getItem(url, function(error, data) {

        if (data) {
          callback(data);
        }
        else {
          d3.json(url, function(error, data){
            localforage.setItem(url, data);
            callback(data);
          })
        }

      });

    }

  });

}
