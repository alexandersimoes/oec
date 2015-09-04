configs.rings = function(build, container) {
  var h = container.offsetHeight || window.innerHeight;

  return {
    "active": {
      "value": function(d){
        return build.origin === "all" ? true : d.export_rca >= 1;
      },
      "spotlight":true
    },
    "color": "color",
    "focus": build.prod.id,
    "id": ["nest","id"],
    "depth": 1,
    "labels": h > 400,
    "size": "export_val",
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}
