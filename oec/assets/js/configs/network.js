function change_layout(new_layout){
  var network_file = "/static/json/"+new_layout+".json";
  viz.nodes(network_file, function(network){
    viz.edges(network.edges);
    return network.nodes;
  }).draw();
}

function getParameterByName(name) {
  var match = RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
  return match && decodeURIComponent(match[1].replace(/\+/g, ' '));
}

configs.network = function(build, container) {
  if(build.attr_type == "sitc"){
    var ui = [];
  }
  else {
    var ui = [
      {"method":change_layout, "label":"Layout", "value":[
        {"Force Directed":"network_hs4"},
        {"Circular Spring":"network_hs4_circular_spring"},
        {"Fruchterman Reingold":"network_hs4_fr"},
        {"Complexity Circles":"network_hs4_complexity_circles"},
        {"Community Circles":"network_hs4_community_circles"},
        {"Community Rectangles":"network_hs4_community_rectangles"},
      ]}
    ];
  }

  if(build.trade_flow === "pgi"){
    // var colors = ["#f1eef6", "#bdc9e1", "#74a9cf", "#0570b0"];
    // var colors = ['#ffffcc','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#0c2c84']
    var cool_colors = ["#0e0092", "#2e34a4", "#3d5cb7", "#4483c9", "#44abdb", "#38d5ed", "#00ffff"];
    var warm_colors = ['#710000','#9a0a04','#be2404','#db3f02','#f05d00','#fc7b00','#ff9a00'];
    var colors = ['#ff0000','#ff7300','#ffb700','#fdff00','#c1ff26','#82ff50','#00ff7d'];
    // var colors = ["#016AA3", "#5493CC", "#96BCEB", "#D7E4F6", "#F7A78B", "#D87442", "#9D511C"]
    var diverging_colors2 = ["#225ea8", "#41b6c4", "#a1dab4", "#ffffcc", '#fee8c8','#fdbb84','#e34a33']
    var diverging_colors = ["#2166ac", "#67a9cf", "#d1e5f0", "#f7f7f7", "#fddbc7", "#ef8a62", "#b2182b"]
    var color_scale = d3.scale.quantile().range(d3.range(7)).domain([32, 53]);
    var color = function(d){
      if(d.id.constructor === Array){
        var thisId = d.id[0].id;
      }
      else {
        var thisId = d.id;
      }
      if(build.attrs[thisId]){
        if(build.attrs[thisId]["pini"]){
          if(getParameterByName('colors') === "warm"){
            return warm_colors[color_scale(build.attrs[thisId]["pini"])]
          }
          if(getParameterByName('colors') === "cool"){
            return cool_colors[color_scale(build.attrs[thisId]["pini"])]
          }
          if(getParameterByName('colors') === "diverging"){
            return diverging_colors[color_scale(build.attrs[thisId]["pini"])]
          }
          if(getParameterByName('colors') === "diverging2"){
            return diverging_colors2[color_scale(build.attrs[thisId]["pini"])]
          }
          return colors[color_scale(build.attrs[thisId]["pini"])]
          // return colors[build.attrs[thisId]["pini_class"] - 1]
        }
      }
      // console.log(d)
      return "blue";
    };
    var id = ["pini_class","id"];
  }
  else {
    var color = "color";
    var id = ["nest","id"];
  }

  return {
    "active": {
      "value": build.origin.id !== "xxwld" ? function(d){
        return d.export_rca >= 1;
      } : false,
      "spotlight": true
    },
    "color": color,
    "depth": 1,
    // "edges": {
    //     "value": "/static/json/just_edges.json",
    //     "callback": function(network){
    //       return network.edges
    //     }
    // },
    "id": id,
    "nodes": {
      "overlap": 1.1,
    },
    // "nodes": {
    //   "overlap": 1.1,
    //   "value": {
    //     "value": "/static/json/just_nodes.json",
    //     "callback": function(network){
    //       return network.nodes
    //     }
    //   }
    // },
    "size": "export_val",
    "ui": ui
  }
}
