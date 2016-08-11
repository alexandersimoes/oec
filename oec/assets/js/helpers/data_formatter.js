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
