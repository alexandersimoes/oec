configs.line = function(build) {
  return {
    "color": "id",
    "depth": 1,
    "x": "year",
    "y": "trade",
    "ui": [{"method":share(build), "value":["Share"], "type":"button"}]
  }
}
