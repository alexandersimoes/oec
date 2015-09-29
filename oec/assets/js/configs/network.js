function change_layout(new_layout){
  var network_file = "/static/json/"+new_layout+".json";
  viz.nodes(network_file, function(network){
    viz.edges(network.edges);
    return network.nodes;
  }).draw();
}

configs.network = function(build, container) {
  if(build.attr_type == "sitc"){
    var ui = [{"method":share(build), "value":["Share"], "type":"button"}];
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
      ]},
      {"method":share(build), "value":["Share"], "type":"button"}
    ]
  }
  
  return {
    "active": {
      "value": function(d){
        return d.export_rca >= 1;
      },
      "spotlight":true      
    },
    "color": "color",
    "depth": 1,
    // "edges": {
    //     "value": "/static/json/just_edges.json",
    //     "callback": function(network){
    //       return network.edges
    //     }
    // },
    "id": ["nest","id"],
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
