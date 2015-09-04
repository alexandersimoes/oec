configs.line = function(build, container) {
  return {
    "color": function(d){
      if(d.name=="Exports"){ return "#0b1097" }
      else{ return "#c8140a" }
    },
    "depth": 0,
    "id": "test",
    "timeline": {
      "play": false
    },
    "x": "year",
    "y": "trade",
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}
