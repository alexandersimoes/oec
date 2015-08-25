configs.scatter = function(build) {
  return {
    "color": "color",
    "depth": 1,
    "size": "export_val",
    "x": "eci",
    "y": {
      "scale": "log",
      "value": build.trade_flow
    },
    "ui": [{"method":share(build), "value":["Share"], "type":"button"}]
  }
}
