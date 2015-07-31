function x(){
  // do json
  // format data
  // pass to viz
  // update UI
  alert('getting all years!')
}
configs.tree_map = function(build) {
  return {
    "depth": 1,
    "shape": "square",
    "labels": {"align": "start", "valign":"top"},
    "color": "color",
    "zoom": false,
    "ui": [
      {"method":"depth", "value":[{"HS2": 0}, {"HS6":1}], "label":"Depth"},
      {"method":x, "value":["Show all years"], "type":"button"}
    ]
  }
}
