configs.spaghetti = function(build, container) {

  var countries = d3plus.util.uniques(build.data, "eci_rank");
  var oldest_year = build.data.reduce(function(obj, d){
    if (!obj[d.id]) obj[d.id] = [];
    obj[d.id].push(d);
    return obj;
  }, {});
  for (var id in oldest_year) {
    var year = d3.min(oldest_year[id], function(d){ return d.year; });
    oldest_year[id] = oldest_year[id].filter(function(d){ return d.year === year; })[0].eci_rank;
  }

  var unique_years = d3plus.util.uniques(build.data, "year");
  var years = d3.range(unique_years[0], unique_years[unique_years.length - 1], 5);
  years = years.concat([unique_years[unique_years.length - 1]]);
  years = years.map(function(y){ return new Date("01/01/"+y)});

  var heatmap = ["#282F6B", "#419391", "#AFD5E8", "#EACE3F", "#B35C1E", "#B22200"];
  var color_scale = d3.scale.linear()
    .domain(d3plus.util.buckets([1, countries.length], heatmap.length))
    .range(heatmap);

  build.data.forEach(function(d){
    d.eci_color = color_scale(oldest_year[d.id]);
  });
  return {
    "color": "eci_color",
    "id": "origin_id",
    "shape": {"interpolate": "monotone"},
    "timeline": false,
    "x": {
      "ticks": years,
      "value": "year"
    },
    "y": {
      "range": [countries.length, 1],
      "ticks": [1].concat(d3.range(5, countries.length + 1, 5)),
      "value": "eci_rank"
    },
    "ui": [
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
}
