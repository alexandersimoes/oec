var configs = {};

var visualization = function(build) {

  var attrs = {}, 
      trade_flow = build.trade_flow,
      opposite_trade_flow = trade_flow == "export" ? "import" : "export",
      attr_id = build.attr_type + "_id",
      default_config = configs["default"](build),
      viz_config = configs[build.viz.slug](build);

  var viz_height = window.innerHeight;
  var viz_width = window.innerWidth;

  var viz = d3plus.viz()
              .config(default_config)
              .config(viz_config)
              .height(viz_height)
              .width(viz_width);
  
  /* Need to set text formatting in HTML for translations */
  viz.format({"text": function(text, key, vars){
      if(key){
        if(key.key == "display_id"){ return text.toUpperCase(); }
      }
      if(text){
        if(text == "display_id"){ 
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

        if(text.indexOf("Values") >= 0 && !key){
          return trade_flow.charAt(0).toUpperCase() + trade_flow.substr(1).toLowerCase() + " " + text;
        }

        return d3plus.string.title(text, key, vars);
      }
    }
  })


  var q = queue()
              .defer(d3.json, build.data_url)
              .defer(d3.json, build.attr_url);

  /* unleash the dogs... make the AJAX requests in order to the server and when
     they return execute the go() func */
  q.await(function(error, raw_data, raw_attrs){
  
    // set key 'nest' to their id
    raw_attrs.data.forEach(function(d){
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

    // go through raw data and set each items nest and id vars properly
    // also calculate net values
    raw_data.data.forEach(function(d){
      d.nest = d[attr_id].substr(0, 2)
      if(attr_id.indexOf("hs") == 0){
        d.nest_mid = d[attr_id].substr(0, 6)
      }
      d.id = d[attr_id]
      var net_val = parseFloat(d[trade_flow+"_val"]) - parseFloat(d[opposite_trade_flow+"_val"]);
      if(net_val > 0){
        d["net_"+trade_flow+"_val"] = net_val;
      }
    })
  
    viz.data(raw_data.data).attrs(attrs).draw();
  
    d3.select("#loading")
      .style("display", "none")

    d3.select("#viz")
      .style("display", "block")
  
  });

}

configs.default = function(build) {
  
  /*  If we're looking at countries their icons are flags and we don't
      want to show the colored background because the flags don't take up
      100% of the icon square. 
  
      Also we want to show RCA if we're looking at products. */
  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var icon = {"value":"icon", "style":{"nest":"knockout","id":"default"}};
    var tooltip = ["display_id", build.trade_flow+"_val"];
  }
  else {
    var icon = {"value":"icon", "style":"knockout"};
    var tooltip = ["display_id", build.trade_flow+"_val", build.trade_flow+"_rca"]
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
    "background": "none",
    "color": { "heatmap": ["#cccccc","#0085BF"] },
    "container": "#viz",
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
    "id": ["nest", "id"],
    "messages": {"branding": true},
    "size": {
      "value": build.trade_flow+"_val",
      "threshold": false
    },
    "text": ["name", "display_id"],
    "time": {"value": "year", "solo": build.year },
    "tooltip": { "small": 225 },
    "tooltip": tooltip,
    "type": build.viz.slug
  }

}

configs.stacked = function(build) {
  return {
    "depth": 1,
    "shape": "area",
    "x": "year",
    "color": "color",
    "order": "nest"
  }
}


configs.tree_map = function(build) {
  return {
    "depth": 1,
    "shape": "square",
    "labels": {"align": "start", "valign":"top"},
    "color": "color",
    "zoom": false
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
