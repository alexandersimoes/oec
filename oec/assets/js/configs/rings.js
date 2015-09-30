configs.rings = function(build, container) {

  var h = container.offsetHeight || window.innerHeight;

  var active = false;
  if (build.origin !== "all") {
    active = {
      "value": function(d){
        return d.export_rca >= 1;
      },
      "spotlight":true
    };
  }

  return {
    "active": active,
    "color": "color",
    "focus": build.prod.id,
    "id": ["nest","id"],
    "depth": 1,
    "labels": h > 400,
    "size": "export_val"
  }
}
