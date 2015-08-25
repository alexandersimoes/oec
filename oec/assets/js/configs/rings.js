configs.rings = function(build) {
  return {
    "active": {
      "value": function(d){
        return d.export_rca >= 1;
      },
      "spotlight":true      
    },
    "color": "color",
    "focus": build.prod.id,
    "id": ["nest","id"],
    "depth": 1,
    "size": "export_val",
    "ui": [{"method":share(build), "value":["Share"], "type":"button"}]
  }
}
