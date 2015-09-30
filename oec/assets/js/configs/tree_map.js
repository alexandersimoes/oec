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
