configs.stacked = function(build, container) {
  function change_layout(new_layout){
    viz.y({"scale": new_layout}).draw();
  }

  if(build.attr_type == "dest" || build.attr_type == "origin"){
    var depth_ui = {"method":"depth", "value":[{"Continent": 0}, {"Country":1}], "label":"Depth"}
  }
  else if(build.attr_type == "sitc"){
    var depth_ui = {"method":"depth", "value":[{"SITC2": 0}, {"SITC4":1}], "label":"Depth"}
  }
  else {
    var depth_ui = {"method":"depth", "value":[{"HS2": 0}, {"HS4":1}], "label":"Depth"}
  }

  return {
    "depth": 1,
    "shape": "area",
    "x": "year",
    "y": {"scale": "linear"},
    "color": "color",
    "order": "nest",
    "timeline": {
      "play": false
    },
    "ui": [
      depth_ui,
      {"method":change_layout, "value":[{"Value": "linear"}, {"Share": "share"}], "label":"Layout"}
    ]
  }
}
