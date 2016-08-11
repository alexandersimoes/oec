// WARNING: Do not edit the contents of this file. It is compiled dynamically
// from multiple source files located in the assets/js directory.

var configs = {};

var visualization = function(build, container) {

  if (!d3plus.util.d3selection(container)) {
    container = d3.select(container);
  }

  var trade_flow = build.trade_flow,
      default_config = configs["default"](build, container);

  var viz = d3plus.viz()
              .container(container)
              .config(default_config)
              .error(oec.translations.loading_viz)
              .edges({"color": default_config.edges.color})
              .draw();

  container.append("div")
    .attr("class", "viz_loader")
    .style("background-color", build.dark ? "rgb(129, 145, 157)" : "rgb(255, 255, 255)");

  /* need to grab json network file for rings and product space */
  if(build.viz.slug == "network" || build.viz.slug == "rings"){
    if(build.attr_type == "sitc"){
      var network_file = "/static/json/network_sitc.json";
    }
    else {
      var network_file = "/static/json/network_hs4.json";
      if(build.viz.slug == "rings" && build.prod.id.length == 8){
        network_file = "/static/json/network_hs6.json";
      }
    }
    viz.nodes(network_file, function(network){
      viz.edges(network.edges);
      return network.nodes;
    })
  }

  /* Need to set text formatting in HTML for translations */
  viz.format({"text": function(text, key, vars){

      if(text){

        if (text.indexOf("<img") === 0) {
          return text;
        }

        if (key) {
          if(key.key === "display_id"){
            return text.toUpperCase();
          }
        }

        if (text.indexOf("HS") === 0 || text.indexOf("SITC") === 0) {
          return text;
        }

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
  try {
    var same_origin = window.parent.location.host == window.location.host;
  }
  catch (e) {
    var same_origin = false;
  }
  if (same_origin && window.parent.location.href.indexOf("/embed/") > 0) {
    viz.title(build.title.toUpperCase());
  }

  load(build.attr_url, function(raw_attrs){
    build.attrs = format_attrs(raw_attrs, build);

    /* unleash the dogs... make the AJAX requests in order to the server and when
       they return execute the go() func */
    d3.json(build.data_url, function(error, raw_data){
      build.data = format_data(raw_data, build.attrs, build);

      var csv_data = format_csv_data(build.data, build.attrs, build);

      viz.config(configs[build.viz.slug](build, container));

      var ui = viz.ui() || [];
      var suffix = !build.dark ? "_dark" : "";
      ui = ui.concat([
        {"method": share(build), "value": ["<img src='/static/img/profile/share" + suffix +".png' />"], "type": "button"},
        {"method": download(container, csv_data), "value": ["<img src='/static/img/profile/download" + suffix +".png' />"], "type": "button"}
      ]);

      var viz_width = viz.width();

      viz
        .data(build.data)
        .attrs(build.attrs)
        .error(false)
        .ui(ui)
        .tooltip({
          "large": (viz_width < 768 && build.viz.slug != "rings" && build.viz.slug != "geo_map") ? viz_width * 0.9 : 200,
          "stacked": viz_width < 768 ? true : false
        })
        .draw();

      d3.select("#viz")
        .style("display", "block");

    });

  })

  return viz;

}

configs.default = function(build, container) {

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
    var tooltip_data = ["display_id", build.trade_flow+"_val", build.trade_flow+"_rca"]
    var id_nesting = ["nest", "nest_mid", "id"];
    if(build.attr_type == "sitc"){
      var id_nesting = ["nest","id"];
    }
  }
  icon.back = "fa-long-arrow-left";

  if (["eci", "show"].indexOf(build.trade_flow) >= 0) {
    tooltip_data.push("year");
  }

  var background = "none", curtain = "black", text = "#333333";
  try {
    var same_origin = window.parent.location.host == window.location.host;
  }
  catch (e) {
    var same_origin = false;
  }
  if(same_origin){
    if (window.location.href.indexOf("/profile/") > 0) {
      background = d3.select(container.node().parentNode.parentNode.parentNode).style("background-color");
    }
    else if (window.parent.location !== window.location) {
      background = "#212831";
    }
    else {
      // background = "#212831";
      background = "#fff";
    }
    text = d3plus.color.text(background);
    curtain = background;
  }
  
  if(build.viz.slug == "network" && build.trade_flow === "gini"){
    tooltip_data.push("pini");
  }

  var edges = "#ddd",
      grid = "#ccc",
      missing = "#ddd",
      chart = background,
      ui_color = oec.ui.light,
      heatmap = ["#3B447A", "#419391", "#AFD5E8", "#EACE3F", "#B35C1E", "#B22200"],
      highlight = "#a0a0a0";

  build.dark = background !== "none" && d3.hsl(background).l < 0.5;

  if (build.dark) {
    missing = d3plus.color.lighter(background, 0.7);
    missing = "#3f464f";
    edges = d3plus.color.lighter(background, 0.2);
    grid = background;
    chart = d3plus.color.lighter(background, 0.1);
    ui_color = oec.ui.dark;
    heatmap = ["#3B447A", "#419391", "#AFD5E8", "#EACE3F", "#B35C1E", "#B22200"];
  }

  var tooltip = {
      "children": false,
      "curtain": {"color": curtain},
      "font": {
        "color": "#333"
      },
      "html": {
        "url": function(focus_id){
          container.select(".viz_loader").classed("visible", true);
          var display_id = focus_id.substring(2).replace("_export", "").replace("_import", "");
          var attr_type = (build.attr_type.indexOf("hs") >= 0 || build.attr_type=="sitc") ? "prod_id" : build.attr_type+"_id";
          var url_args = "?trade_flow="+build.trade_flow+"&classification="+build.classification+"&"+attr_type+"="+display_id+"&focus="+attr_type;
          ['origin', 'dest', 'prod'].forEach(function(filter){
            if(typeof build[filter] != "string"){
              url_args += "&"+filter+"_id="+build[filter].display_id;
            }
          })
          // console.log("/en/visualize/builds/"+url_args)
          return "/"+build.lang+"/visualize/builds/"+url_args;
        },
        "callback":function(data){
          var buttons = [];
          buttons.push("<a target='_top' href='"+data.profile.url+"' class='profile' style='color:"+d3plus.color.lighter(data.profile.color)+"'><img src='"+data.profile.icon+"'/><h3>"+data.profile.title+"</h3></a><h3 class='related_viz'>Related Visualizations</h3>");
          data.builds.forEach(function(b){
            buttons.push("<a target='_top' href='/"+build.lang+"/visualize/"+b.url+"' class='related "+b.viz+"'>"+b.title+"</a>");
          });
          container.select(".viz_loader").classed("visible", false);
          return buttons.join("");
        }
      },
      "small": 200,
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
    "axes": {
      "background": {
        "color": chart,
        "stroke": {
          "color": grid
        }
      },
      "ticks": false
    },
    "background": background,
    "color": {
      "heatmap": heatmap,
      "missing": missing,
      "primary": highlight
    },
    "edges": {"color": edges},
    "focus": {"tooltip": window.innerWidth > 768},
    "font": {
      "color": text
    },
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
    "labels": {
      "font": {
        "family": ["HelveticaNeue-CondensedBold", "HelveticaNeue-Condensed", "Helvetica-Condensed", "Arial Narrow", "sans-serif"],
        "weight": 800
      },
      "padding": 15
    },
    "legend": {"filters":true},
    "messages": {
      "branding": {
        "image": {
          "light": "/static/img/d3plus/icon-transparent.png",
          "dark": "/static/img/d3plus/icon-transparent-invert.png"
        },
        "value": true
      },
      "font": {"color": text},
      "style": "large"
    },
    "size": {
      "value": build.trade_flow+"_val",
      "threshold": false
    },
    "text": {"nest":"name", "id":["name", "display_id"]},
    "time": {"value": "year", "solo": build.year },
    "title": {
      "font": {
        "color": text,
        "family": ["Montserrat", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
        "weight": 400
      },
      "sub": {
        "font": {
          "color": text,
          "family": ["Montserrat", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
          "size": 16,
          "transform": "uppercase",
          "weight": 400
        }
      },
      "total": {
        "font": {
          "color": text,
          "family": ["Montserrat", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
          "size": 16,
          "transform": "uppercase",
          "weight": 400
        },
        "value": ["line", "scatter"].indexOf(build.viz.slug) < 0
      }
    },
    "tooltip": tooltip,
    "type": build.viz.slug,
    "ui": {
      "border": oec.ui.border,
      "color": ui_color,
      "font": {
        "color": text,
        "family": oec.ui.font.family,
        "size": oec.ui.font.size,
        "weight": oec.ui.font.weight
      },
      "margin": oec.ui.margin,
      "padding": oec.ui.padding
    },
    "x": {
      "grid": {
        "color": grid
      },
      "label": {
        "font": {
          "size": 16
        }
      },
      "ticks": {
        "color": text,
        "font": {"size": 12}
      }
    },
    "y": {
      "grid": {
        "color": grid
      },
      "label": {
        "font": {
          "size": 16
        }
      },
      "ticks": {
        "color": text,
        "font": {"size": 12}
      }
    }
  }

}

configs.geo_map = function(build, container) {
  return {
    "color": build.trade_flow+"_val",
    "coords": {
      "key": "countries",
      "padding": 0,
      "mute": ["anata"],
      "value": "/static/json/country_coords.json"
    },
    "depth": 1,
    "size": "export_val",
    "ui": [
      {"method":show_all_years, "value":["Show all years"], "type":"button"},
      {"method":"color", "value": [
        {"Value": build.trade_flow+"_val"},
        {"Annual Growth Rate (1 year)": build.trade_flow+"_val_growth_pct"},
        {"Annual Growth Rate (5 year)": build.trade_flow+"_val_growth_pct_5"},
        {"Growth Value (1 year)": build.trade_flow+"_val_growth_val"},
        {"Growth Value (5 year)": build.trade_flow+"_val_growth_val_5"},
      ]}
    ]
  }
}

configs.line = function(build, container) {

  if (build.trade_flow === "show") {

    return {
      "color": "color",
      "depth": 0,
      "icon": {"style": "knockout"},
      "id": "test",
      "size": 2,
      "timeline": false,
      "x": "year",
      "y": "trade"
    }

  }
  else if (build.trade_flow === "eci") {

    var unique_years = build.year || d3plus.util.uniques(build.data, "year");
    var years = d3.range(unique_years[0], unique_years[unique_years.length - 1], 5);
    years = years.concat([unique_years[unique_years.length - 1]]);
    first_years = 0;

    var countries = d3plus.util.uniques(build.data, "eci_rank");
    var oldest_year = build.data.reduce(function(obj, d){
      if (!obj[d.id]) obj[d.id] = [];
      if (d.year === years[0]) first_years++;
      if (d.year >= years[0]) obj[d.id].push(d);
      return obj;
    }, {});
    for (var id in oldest_year) {
      var year = d3.min(oldest_year[id], function(d){ return d.year; });
      oldest_year[id] = oldest_year[id].filter(function(d){ return d.year === year; })[0].eci_rank;
    }

    years = years.map(function(y){ return new Date("01/01/"+y)});

    //var heatmap = ["#282F6B", "#419391", "#AFD5E8", "#EACE3F", "#B35C1E", "#B22200"];
    var line_color = ["#4C447C", "#192C81", "#074F99", "#1796D6", "#3EB6B8", "#CDD76A", "#F19825", "#E00C24", "#935F4F"];

    var normal_stroke = 1,
        highlight_stroke = 2,
        line_weight = function(l, vars) {
          return vars.color.value === "eci_color" ? normal_stroke : l.origin_id === build.dest.id ? highlight_stroke : normal_stroke;
        };

    var color_scale = d3.scale.linear()
      .domain(d3plus.util.buckets([1, first_years], line_color.length))
      .range(line_color);
    build.data.forEach(function(d){
      d.eci_color = color_scale(oldest_year[d.id]);
      if (build.dest !== "all") {
        if (d.origin_id !== build.dest.id) {
          d.highlight = build.dark ? "#666" : "#f7f7f7";
        }
        else {
          d.highlight = !build.dark ? "#666" : "#f7f7f7";
        }
      }
    });

    var ui = [];
    if (build.dest !== "all") {
      ui.unshift({"method": "color", "value":[{"On": "highlight"},{"Off": "eci_color"}], "type":"toggle", "label": "Highlight"});
    }

    return {
      "color": build.dest !== "all" ? "highlight" : "eci_color",
      "id": "origin_id",
      "legend": false,
      "order": {
        "sort": "asc",
        "value": line_weight
      },
      "shape": {"interpolate": "monotone"},
      "size": line_weight,
      "timeline": false,
      "x": {
        "ticks": years,
        "value": "year"
      },
      "y": {
        "range": [countries.length, 1],
        "ticks": [1].concat(d3.range(5, countries.length + 1, 5)),
        "value": "eci_rank"
      },
      "ui": ui
    }

  }
  else {

    if(build.attr_type == "dest" || build.attr_type == "origin"){
      var depth_ui = {"method":"depth", "value":[{"Continent": 0}, {"Country":1}], "label":"Depth"}
    }
    else if(build.attr_type == "sitc"){
      var depth_ui = {"method":"depth", "value":[{"SITC2": 0}, {"SITC4":1}], "label":"Depth"}
    }
    else {
      var depth_ui = {"method":"depth", "value":[{"HS2": 0}, {"HS4":1}], "label":"Depth"}
    }

    return {
      "color": "color",
      "depth": build.attr_type == "dest" || build.attr_type == "origin" ? 1 : 0,
      "shape": "line",
      "size": 2,
      "timeline": {
        "play": false
      },
      "ui": [depth_ui],
      "x": "year",
      "y": {
        "scale": "linear",
        "value": build.trade_flow + "_val"
      }
    }

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
  if(build.attr_type == "sitc"){
    var ui = [];
  }
  else {
    var ui = [
      {"method":change_layout, "label":"Layout", "value":[
        {"Force Directed":"network_hs4"},
        {"Circular Spring":"network_hs4_circular_spring"},
        {"Fruchterman Reingold":"network_hs4_fr"},
        {"Complexity Circles":"network_hs4_complexity_circles"},
        {"Community Circles":"network_hs4_community_circles"},
        {"Community Rectangles":"network_hs4_community_rectangles"},
      ]}
    ];
  }
  
  var legend = {"filters":true};
  if(build.trade_flow === "gini"){
    legend["order"] = "text";
  }

  return {
    "active": {
      "value": build.origin.id !== "xxwld" ? function(d){
        return d.export_rca >= 1;
      } : false,
      "spotlight": true
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
    "legend": legend,
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
    "ui": ui
  }
}

configs.rings = function(build, container) {

  var h = container.offsetHeight || window.innerHeight;

  var active = false;
  if (build.origin !== "all") {
    active = {
      "value": function(d){
        return d.export_rca >= 1;
      },
      "spotlight":true
    };
  }

  return {
    "active": active,
    "color": "color",
    "focus": build.prod.id,
    "id": ["nest","id"],
    "depth": 1,
    "labels": h > 400,
    "size": "export_val"
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
    }
  }
}

configs.stacked = function(build, container) {
  function change_layout(new_layout){
    viz.y({"scale": new_layout}).draw();
  }

  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var depth_ui = {"method":"depth", "value":[{"Continent": 0}, {"Country":1}], "label":"Depth"}
  }
  else if(build.attr_type == "sitc"){
    var depth_ui = {"method":"depth", "value":[{"SITC2": 0}, {"SITC4":1}], "label":"Depth"}
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
    "timeline": {
      "play": false
    },
    "ui": [
      depth_ui,
      {"method":change_layout, "value":[{"Value": "linear"}, {"Share": "share"}], "label":"Layout"}
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
  else if(build.attr_type == "sitc"){
    var depth_ui = {"method":"depth", "value":[{"SITC2": 0}, {"SITC4":1}], "label":"Depth"}
  }
  else {
    var depth_ui = {"method":"depth", "value":[{"HS2": 0}, {"HS4":1}, {"HS6":2}], "label":"Depth"}
  }

  return {
    "depth": window.innerWidth <= 480 ? 0 : 1,
    "shape": "square",
    "labels": {"align": "start", "valign":"top"},
    "color": "color",
    "zoom": false,
    "ui": [
      depth_ui,
      {"method":show_all_years, "value":["Show all years"], "type":"button"},
      {"method":"color", "value": [
        {"Category": "color"},
        {"Annual Growth Rate (1 year)": build.trade_flow+"_val_growth_pct"},
        {"Annual Growth Rate (5 year)": build.trade_flow+"_val_growth_pct_5"},
        {"Growth Value (1 year)": build.trade_flow+"_val_growth_val"},
        {"Growth Value (5 year)": build.trade_flow+"_val_growth_val_5"},
      ]}
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
    if(build.viz.slug == "network" && build.trade_flow === "gini"){
      d.nest = attrs[d.id].nest
    }
  })

  // special case for line chart of trade balance (need to duplicate data)
  if(build.viz.slug == "line" && build.trade_flow === "show"){

    data = data.map(function(d){
      d.trade = d.export_val;
      d.test = d.id + "_export";
      d.name = "Exports";
      d.color = "#17bcef";
      d.icon = "/static/img/icons/balance/export_val.png";
      return d;
    });

    var clones = d3plus.util.copy(data).map(function(d){
      d.trade = d.import_val;
      d.test = d.id + "_import";
      d.name = "Imports";
      d.color = "#c8140a";
      d.icon = "/static/img/icons/balance/import_val.png";
      return d;
    });

    data = data.concat(clones);

  }

  return data;

}

function format_attrs(raw_attrs, build){
  var attrs = {};
  var attr_id = attr_id = build.attr_type + "_id";
  var bin_lookup = {
    "bin0": "#4575b4",
    "bin1": "#91bfdb",
    "bin2": "#fee090",
    "bin3": "#fc8d59",
    "bin4": "#D73038"
  }

  raw_attrs.data.forEach(function(d){
    // d.nest = d.id.substr(0, 2);
    d.nest = "bin"+d.pini_class;
    attrs[d.id] = d;
    
    if(attr_id == "origin_id" || attr_id == "dest_id"){
      attrs[d.id]["icon"] = "/static/img/icons/country/country_"+d.id+".png"
    }
    else if(attr_id.indexOf("hs") == 0){
      attrs[d.id]["icon"] = "/static/img/icons/hs/hs_"+d.id.substr(0, 2)+".png"
    }
    else if(attr_id == "sitc_id"){
      attrs[d.id]["icon"] = "/static/img/icons/sitc/sitc_"+d.id.substr(0, 2)+".png"
    }
    
    if(build.viz.slug == "network" && build.trade_flow === "gini"){
      attrs[d.id]["color"] = bin_lookup[d.nest];
      attrs[d.id]["icon"] = "/static/img/icons/sitc/sitc_90.png";
    }
  })

  if(build.viz.slug == "network" && build.trade_flow === "gini"){
    attrs["bin0"] = {"color":"#4575b4","id":"bin0","nest":"bin0","icon":"/static/img/icons/sitc/sitc_90.png","name":"Product GINI < 32.8"}
    attrs["bin1"] = {"color":"#91bfdb","id":"bin1","nest":"bin1","icon":"/static/img/icons/sitc/sitc_90.png","name":"Product GINI 32.8 - 38.6"}
    attrs["bin2"] = {"color":"#fee090","id":"bin2","nest":"bin2","icon":"/static/img/icons/sitc/sitc_90.png","name":"Product GINI 38.7 - 41.9"}
    attrs["bin3"] = {"color":"#fc8d59","id":"bin3","nest":"bin3","icon":"/static/img/icons/sitc/sitc_90.png","name":"Product GINI 42.0 - 45.7"}
    attrs["bin4"] = {"color":"#D73038","id":"bin4","nest":"bin4","icon":"/static/img/icons/sitc/sitc_90.png","name":"Product GINI > 45.7"}
  }

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
          if(attr){
            datum.push(attr["display_id"] ? attr["display_id"].toUpperCase() : attr["id"].substring(2).toUpperCase())
          }
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

function get_container(container){
  if (d3plus.util.d3selection(container)) {
      return container.node();
  }
  return container;
}
function download(container, csv_data){
  return function(){
    var this_container = get_container(container);

    d3.selectAll(".modal#download").classed("active", true);
    d3.selectAll("#mask").classed("visible", true);
    d3.selectAll("body").classed("frozen", true);

    d3.selectAll(".modal#download a.download_button").on("click", function(){

      var format = d3.select(this).attr("id");

      var title = window.location.pathname.split("/")
      title.splice(0, 1)
      title.splice(0, 1)
      title.splice(title.length-1, 1)
      title = title.join("_").replace("embed", "explore")

      if(format == "svg" || format == "png"){
        var svg = d3.select(this_container).select("svg")
          .attr("title", title)
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg");

        // Add this content as the value of input
        var content = (new XMLSerializer).serializeToString(svg.node());
      }
      else if(format == "csv"){
        // var content = d3.csv.format(csv_data);
        var content = JSON.stringify(csv_data);
      }

      var form = d3.select("form#download");
      form.select("input[name=content]").attr("value", content);
      form.select("input[name=format]").attr("value", format);
      form.select("input[name=title]").attr("value", title);

      form.node().submit();

      d3.event.preventDefault();

    });

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

function share(build){

  return function(){
    var lang = build.lang;
    try {
      var same_origin = window.parent.location.host == window.location.host;
    }
    catch (e) {
      var same_origin = false;
    }
    var url = encodeURIComponent("/"+lang+"/visualize/"+build.url)

    // make post request to server for short URL
    d3.json("/"+lang+"/visualize/shorten/")
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

    // set embed link
    d3.select(".modal-body input.embed_code").property("value", '<iframe width="560" height="315" src="http://atlas.media.mit.edu/'+lang+'/visualize/embed/'+build.url+'?controls=false" frameborder="0" ></iframe>')

    // set social media link URLs
    d3.selectAll(".modal-body a#Facebook").attr("href", build.social.facebook)
    d3.selectAll(".modal-body a#Twitter").attr("href", build.social.twitter)
    // d3.selectAll(".modal-body a#Google").attr("href", build.social.google)

    // open modal window
    d3.selectAll(".modal#share").classed("active", true);
    d3.selectAll("#mask").classed("visible", true);
    d3.selectAll("body").classed("frozen", true);
  }

}

function popup(href) {
  var width = 600,
      height = 400,
      left = window.screenLeft + window.innerWidth/2 - width/2,
      top = window.screenTop + window.innerHeight/2 - height/2;
  window.open(href, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=" + height + ",width=" + width + ",left=" + left + ",top=" + top);
  return false;
}
