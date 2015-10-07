configs.line = function(build, container) {

  if (build.trade_flow === "show") {

    return {
      "color": "color",
      "depth": 0,
      "icon": {"style": "knockout"},
      "id": "test",
      "size": 2,
      "timeline": false,
      "x": "year",
      "y": "trade"
    }

  }
  else if (build.trade_flow === "eci") {

    var unique_years = build.year || d3plus.util.uniques(build.data, "year");
    var years = d3.range(unique_years[0], unique_years[unique_years.length - 1], 5);
    years = years.concat([unique_years[unique_years.length - 1]]);
    first_years = 0;

    var countries = d3plus.util.uniques(build.data, "eci_rank");
    var oldest_year = build.data.reduce(function(obj, d){
      if (!obj[d.id]) obj[d.id] = [];
      if (d.year === years[0]) first_years++;
      if (d.year >= years[0]) obj[d.id].push(d);
      return obj;
    }, {});
    for (var id in oldest_year) {
      var year = d3.min(oldest_year[id], function(d){ return d.year; });
      oldest_year[id] = oldest_year[id].filter(function(d){ return d.year === year; })[0].eci_rank;
    }

    years = years.map(function(y){ return new Date("01/01/"+y)});

    //var heatmap = ["#282F6B", "#419391", "#AFD5E8", "#EACE3F", "#B35C1E", "#B22200"];
    var line_color = ["#4C447C", "#192C81", "#074F99", "#1796D6", "#3EB6B8", "#CDD76A", "#F19825", "#E00C24", "#935F4F"];

    var normal_stroke = 1,
        highlight_stroke = 2,
        line_weight = function(l, vars) {
          return vars.color.value === "eci_color" ? normal_stroke : l.origin_id === build.dest.id ? highlight_stroke : normal_stroke;
        };

    var color_scale = d3.scale.linear()
      .domain(d3plus.util.buckets([1, first_years], line_color.length))
      .range(line_color);
    build.data.forEach(function(d){
      d.eci_color = color_scale(oldest_year[d.id]);
      if (build.dest !== "all") {
        if (d.origin_id !== build.dest.id) {
          d.highlight = build.dark ? "#666" : "#f7f7f7";
        }
        else {
          d.highlight = !build.dark ? "#666" : "#f7f7f7";
        }
      }
    });

    var ui = [];
    if (build.dest !== "all") {
      ui.unshift({"method": "color", "value":[{"On": "highlight"},{"Off": "eci_color"}], "type":"toggle", "label": "Highlight"});
    }

    return {
      "color": build.dest !== "all" ? "highlight" : "eci_color",
      "id": "origin_id",
      "legend": false,
      "order": {
        "sort": "asc",
        "value": line_weight
      },
      "shape": {"interpolate": "monotone"},
      "size": line_weight,
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
      "ui": ui
    }

  }
  else {

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
      "color": "color",
      "depth": build.attr_type == "dest" || build.attr_type == "origin" ? 1 : 0,
      "shape": "line",
      "size": 2,
      "timeline": {
        "play": false
      },
      "ui": [depth_ui],
      "x": "year",
      "y": {
        "scale": "linear",
        "value": build.trade_flow + "_val"
      }
    }

  }

}
