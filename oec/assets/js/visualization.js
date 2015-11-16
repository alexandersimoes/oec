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
