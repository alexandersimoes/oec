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
