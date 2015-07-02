configs.default = function(build) {
  
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
      },
      "text": function( text , key , vars ){

        if(key){
          if(key == "display_id"){ return text.toUpperCase(); }
        }
        if(text){
          if(text == "share"){ return "{{ _('Percent') }}"; }
          if(text == "display_id"){ return "{{ _('ID') }}"; }
          if(text == "export_val"){ return "{{ _('Export Value') }}"; }
          if(text == "net_export_val"){ return "{{ _('Net Export') }} {{ _('Value') }}"; }
          if(text == "import_val"){ return "{{ _('Import Value') }}"; }
          if(text == "net_import_val"){ return "{{ _('Net Import') }} {{ _('Value') }}"; }
          if(text == "market_val"){ return "{{ _('Market Value') }}"; }
          if(text == "export_rca"){ return "{{ _('Export') }} RCA"; }
          if(text == "import_rca"){ return "{{ _('Import') }} RCA"; }
          if(text == "gdp"){ return "{{ _('GDP') }}"; }
          if(text == "gdp_pc_constant"){ return "{{ _('GDPpc (constant \'05 US$)') }}"; }
          if(text == "gdp_pc_current"){ return "{{ _('GDPpc (current US$)') }}"; }
          if(text == "gdp_pc_constant_ppp"){ return "{{ _('GDPpc PPP (constant \'11)') }}"; }
          if(text == "gdp_pc_current_ppp"){ return "{{ _('GDPpc PPP (current)') }}"; }
          if(text == "eci"){ return "{{ _('ECI') }}"; }

          if(text == trade_flow+"_val_growth_pct"){ return "{{ _('Annual Growth Rate (1 year)') }}"; }
          if(text == trade_flow+"_val_growth_pct_5"){ return "{{ _('Annual Growth Rate (5 year)') }}"; }
          if(text == trade_flow+"_val_growth_val"){ return "{{ _('Growth Value (1 year)') }}"; }
          if(text == trade_flow+"_val_growth_val_5"){ return "{{ _('Growth Value (5 year)') }}"; }

          if(text.indexOf("Values") >= 0 && !key){
            return trade_flow.charAt(0).toUpperCase() + trade_flow.substr(1).toLowerCase() + " " + text;
          }

          return d3plus.string.title( text , key , vars );
        }
      }
    },
    "icon": "icon",
    "id": ["nest", "id"],
    "messages": {"branding": true},
    "size": {
      "value": build.trade_flow+"_val",
      "threshold": false
    },
    "text": ["name", "display_id"],
    "time": {"value": "year", "solo": build.year },
    "tooltip": { "small": 225 },
    "type": build.viz.slug
  }

}
