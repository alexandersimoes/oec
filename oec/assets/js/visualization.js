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

  /* need to grab json network file for rings and product space */
  if(build.viz.slug == "network" || build.viz.slug == "rings"){
    viz.nodes("/static/json/network_hs.json", function(network){
      viz.edges(network.edges);
      return network.nodes;
    })
  }
  
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

  console.log(build)
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
    
    // for geo map, get rid of small island nations that don't exist
    // in geography
    if(build.viz.slug == "geo_map"){
      delete attrs["octkl"]
      delete attrs["octon"]
      delete attrs["ocwlf"]
      delete attrs["ocwsm"]
    }

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
    
    console.log(raw_data.data.length)
    if(build.viz.slug == "line"){
      raw_data.data = raw_data.data.map(function(d){
        d.trade = d.export_val;
        d.id = d.id + "_export";
        d.name = "Exports";
        return d;
      })
      var clones = raw_data.data.map(function(d){
        var x = JSON.parse(JSON.stringify(d));
        x.trade = x.import_val;
        x.id = x.id + "_import";
        x.name = "Imports"
        return x;
      })
      raw_data.data = raw_data.data.concat(clones);
      console.log(raw_data.data.length)
    }
  
    viz.data(raw_data.data).attrs(attrs).draw();
    
    d3.select("#loading")
      .style("display", "none")

    d3.select("#viz")
      .style("display", "block")
  
  });
  
  return viz;

}
