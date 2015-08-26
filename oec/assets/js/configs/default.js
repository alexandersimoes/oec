function share(build){
  return function(){
    // var lang = build.lang;
    var lang = "en";
    var same_origin = window.parent.location.host == window.location.host;
    var url = encodeURIComponent(window.location.pathname + "?lang="+lang)
    if(same_origin){
      if(window.location != window.parent.location){
        var url = encodeURIComponent(window.parent.location.pathname + "?lang="+lang)
      }
    }
    // make post request to server for short URL
    d3.json("/"+lang+"/explore/shorten/")
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
    // set social media link URLs
    d3.selectAll(".modal-body a#Facebook").attr("href", build.social.facebook)
    d3.selectAll(".modal-body a#Twitter").attr("href", build.social.twitter)
    d3.selectAll(".modal-body a#Google").attr("href", build.social.google)
    // open modal window
    d3.selectAll(".modal#share").classed("active", true)
  }
}

configs.default = function(build) {

  /*  If we're looking at countries their icons are flags and we don't
      want to show the colored background because the flags don't take up
      100% of the icon square.

      Also we want to show RCA if we're looking at products. */
  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var icon = {"value":"icon", "style":{"nest":"knockout","id":"default"}};
    var id_nesting = ["nest", "id"];
    var tooltip = ["display_id", build.trade_flow+"_val"];
  }
  else {
    var icon = {"value":"icon", "style":"knockout"};
    var id_nesting = ["nest", "nest_mid", "id"];
    var tooltip = ["display_id", build.trade_flow+"_val", build.trade_flow+"_rca"]
  }

  var background = "none";
  if(window.parent.location.host == window.location.host){
    background = "#eeeeee";
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
    "background": background,
    "color": { "heatmap": ["#cccccc","#0085BF"] },
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
    "id": id_nesting,
    "legend": {"filters":true},
    "messages": {"branding": true, "style": "large"},
    "size": {
      "value": build.trade_flow+"_val",
      "threshold": false
    },
    "text": {"nest":"name", "id":["name", "display_id"]},
    "time": {"value": "year", "solo": build.year },
    "tooltip": { "small": 225 },
    "tooltip": tooltip,
    "type": build.viz.slug
  }

}
