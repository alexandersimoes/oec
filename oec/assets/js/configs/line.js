configs.line = function(build, container) {
  return {
    "color": "color",
    "depth": 0,
    "icon": {"style": "knockout"},
    "id": "test",
    "timeline": false,
    "x": "year",
    "y": "trade",
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}
