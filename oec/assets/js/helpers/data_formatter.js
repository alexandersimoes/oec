function format_data(raw_data, attrs, build){
  
  var data = raw_data.data;
  var opposite_trade_flow = build.trade_flow == "export" ? "import" : "export";
  var attr_id = attr_id = build.attr_type + "_id";
  var pini_domain = [32, 53];
  var pini_scale = d3.scale.quantile().range(d3.range(7)).domain(pini_domain);
  var pini_buckets = [32].concat(pini_scale.quantiles()).concat([53])

  // remove germany for tree maps before 1985
  if(build.classification === "sitc" && build.viz.slug === "tree_map") {
    data = data.filter(function(d) {
      return !(d.year < 1985 && d.origin_id === "eudeu");
    })
  }

  // go through raw data and set each items nest and id vars properly
  // also calculate net values
  data.forEach(function(d){

    // only assign "pini_class" if the dataset is SITC
    if(build.attr_type === "sitc") {
      if(attrs[d[attr_id]]) {
        var bucket = pini_scale(attrs[d[attr_id]].pini);
        d.pini_class = "PGIs ("+pini_buckets[bucket]+" - "+pini_buckets[bucket+1]+")";
      }
    }

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
  var csv_data = [];

  if(build.trade_flow === "show" && build.viz.slug === "line") {
    var cols = ["year", "country_id", "country_name", "eci", "export_val", "import_val", "gdp", "gdp_pc_constant", "gdp_pc_constant_ppp", "gdp_pc_current", "gdp_pc_current_ppp"];
    csv_data.push(cols)
    data.forEach(function(d){
      var row = [];
      cols.forEach(function(column){
        if(column.indexOf("country_id") > -1){
          row.push(attrs[d.id].display_id);
        }
        else if(column.indexOf("country_name") > -1){
          row.push(attrs[d.id].name);
        }
        else {
          row.push(d[column]);
        }
      })
      csv_data.push(row);
    });
    return csv_data;
  }

  // format columns
  var ccp = ["origin", "dest", "prod"];
  var show_id = build.attr_type + "_id";
  var trade_flow = build.trade_flow + "_val";
  csv_data.push(['year', 'country_origin_id', 'country_destination_id', build.classification+'_product_id', trade_flow, trade_flow+"_pct"])

  // format data
  var total_val = d3.sum(data, function(d){ return d[trade_flow]; });
  data.forEach(function(d){
    if(d[trade_flow] || trade_flow === "show_val"){
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
