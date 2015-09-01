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

  var background = "none", curtain = "black", text = "#444";
  if(window.parent.location.host == window.location.host){
    if (window.location.href.indexOf("/profile/") > 0) {
      background = "#eeeeee";
    }
    else {
      background = "#212831";
      text = "white";
    }
    curtain = background;
  }

  var large_tooltip_width = 150;
  if (window.location.href.indexOf("/explore/") > 0 && window.innerWidth > 400) {
    large_tooltip_width = 250;
  }

  var tooltip = {
      "curtain": {"color": curtain},
      "html": {
        "url": function(focus_id){
          var display_id = focus_id.substring(2);
          var attr_type = build.attr_type.indexOf("hs") >= 0 ? "prod_id" : build.attr_type+"_id";
          return "/en/explore/builds/?classification="+build.classification+"&"+attr_type+"="+display_id;
        },
        "callback":function(data){
          var html_str = '<h3>Related Visualizations</h3>'
          data.builds.forEach(function(b){
            html_str += "<a target='_top' href='/en/explore/"+b.url+"' class='related'>"+b.title+"</a>";
          })
          html_str += "<hr />";
          html_str += "<a style='background-color:"+data.profile.color+";color:"+d3plus.color.text(data.profile.color)+";' target='_top' href='"+data.profile.url+"' class='profile'><img src='"+data.profile.icon+"' />"+data.profile.title+"</a>";
          return html_str;
        }
      },
      "small": 200,
      "large": large_tooltip_width,
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
    "labels": {
      "font": {
        "family": ["HelveticaNeue-CondensedBold", "HelveticaNeue-Condensed", "Helvetica-Condensed", "Arial Narrow", "sans-serif"],
        "weight": 800
      },
      "padding": 15
    },
    "legend": {"filters":true},
    "messages": {
      "branding": true,
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
      }
    },
    "tooltip": tooltip,
    "type": build.viz.slug,
    "ui": {
      "color": {
        "primary": "#63636a"
      },
      "font": {
        "color": text,
        "family": ["Source Sans Pro", "Helvetica Neue", "Helvetica", "Arial", "sans-serif"],
        "size": 13
      },
      "margin": 0,
      "padding": 4
    },
    "x": {
      "label": {
        "font": {
          "size": 16
        }
      }
    },
    "y": {
      "label": {
        "font": {
          "size": 16
        }
      }
    }
  }

}
