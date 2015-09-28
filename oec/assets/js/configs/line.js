configs.line = function(build, container) {

  if (build.trade_flow === "show") {

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
  else if (build.trade_flow === "eci") {

    var unique_years = d3plus.util.uniques(build.data, "year");
    var years = d3.range(unique_years[0], unique_years[unique_years.length - 1], 5);
    years = years.concat([unique_years[unique_years.length - 1]]);
    first_years = 0;

    var countries = d3plus.util.uniques(build.data, "eci_rank");
    var oldest_year = build.data.reduce(function(obj, d){
      if (!obj[d.id]) obj[d.id] = [];
      if (d.year === years[0]) first_years++;
      obj[d.id].push(d);
      return obj;
    }, {});
    for (var id in oldest_year) {
      var year = d3.min(oldest_year[id], function(d){ return d.year; });
      oldest_year[id] = oldest_year[id].filter(function(d){ return d.year === year; })[0].eci_rank;
    }

    years = years.map(function(y){ return new Date("01/01/"+y)});

    var heatmap = ["#282F6B", "#419391", "#AFD5E8", "#EACE3F", "#B35C1E", "#B22200"];
    var color_scale = d3.scale.linear()
      .domain(d3plus.util.buckets([1, first_years], heatmap.length))
      .range(heatmap);
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

    var ui = [{"method":share(build), "value":["Share"], "type":"button"}];
    if (build.dest !== "all") {
      ui.unshift({"method": "color", "value":[{"On": "highlight"},{"Off": "eci_color"}], "type":"toggle", "label": "Highlight"});
    }


    return {
      "color": build.dest !== "all" ? "highlight" : "eci_color",
      "id": "origin_id",
      "legend": false,
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
      "depth": build.attr_type == "dest" || build.attr_type == "origin" ? 1 : 0,
      "shape": "line",
      "x": "year",
      "y": {"scale": "linear"},
      "color": "color",
      "timeline": {
        "play": false
      },
      "ui": [
        depth_ui,
        {"method":change_layout, "value":[{"Value": "linear"}, {"Share": "share"}], "label":"Layout"},
        {"method":share(build), "value":["Share"], "type":"button"}
      ]
    }

  }

}
