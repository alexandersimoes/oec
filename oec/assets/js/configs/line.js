configs.line = function(build) {
  return {
    "color": function(d){ 
      if(d.name=="Exports"){ return "#0b1097" } 
      else{ return "#c8140a" } 
    },
    "depth": 0,
    "id": "test",
    "x": "year",
    "y": "trade"
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"},
      {"method":download(container), "value":["Download"], "type":"button"}
    ]
  }
}
