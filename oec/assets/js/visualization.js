var configs = {};

var visualization = function(build) {

  var trade_flow = build.trade_flow,
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

  var q = queue()
              .defer(d3.json, build.data_url)
              .defer(d3.json, build.attr_url);

  /* unleash the dogs... make the AJAX requests in order to the server and when
     they return execute the go() func */
  q.await(function(error, raw_data, raw_attrs){
    
    var attrs = format_attrs(raw_attrs, build)
    var data = format_data(raw_data, attrs, build)
  
    viz.data(raw_data.data).attrs(attrs).draw();
    
    d3.select("#loading")
      .style("display", "none")

    d3.select("#viz")
      .style("display", "block")
  
  });
  
  return viz;

}
