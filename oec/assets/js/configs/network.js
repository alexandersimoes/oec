function change_layout(new_layout){
  var network_file = "/static/json/"+new_layout+".json";
  viz.nodes(network_file, function(network){
    viz.edges(network.edges);
    return network.nodes;
  }).draw();
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
    var colors = ["#f1eef6", "#bdc9e1", "#74a9cf", "#0570b0"];
    var color = function(d){
      if(d.id.constructor === Array){
        var thisId = d.id[0].id;
      }
      else {
        var thisId = d.id;
      }
      if(build.attrs[thisId]){
        if(build.attrs[thisId]["pini_class"]){
          return colors[build.attrs[thisId]["pini_class"] - 1]
        }
      }
      // console.log(d)
      return "blue";
    };
    var id = ["nest","id"];
  }
  else {
    var color = "color";
    var id = ["pini_class","id"];
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
