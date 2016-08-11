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
