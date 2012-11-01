function Key() {
  var showing = "product",
    classification = "hs4";
    
  function key(selection) {
    selection.each(function(attrs, i) {
      
      // unique list of categories
      cats = pretty_cats(attrs);
      
      d3.select(this)
        .attr("id", classification)
        .selectAll("a").data(d3.values(cats))
        .enter()
          .append("a")
          .call(key_icon)
      
      // put tooltip on mouseover
      $('#key a').tipsy({"gravity":'s',"fade":true});      
    })
  }
  
  ////////////////////////////////////////////
  // PRIVATE functions for this app shhhhh...
  ////////////////////////////////////////////
  
  // Find the unique categories from list of attributes
  function pretty_cats(attrs){
    cats = {}
    d3.values(attrs).forEach(function(d){
      cats[d.category_id] = {}
      d3.keys(d).forEach(function(dd){
        if(dd.indexOf("category") > -1){
          cats[d.category_id][dd.replace("category_", "")] = d[dd]
        }
      })
    })
    return cats
  }
  
  // Format the anchor how we want for the given category
  function key_icon(a){
    a.attr("title", function(d){ return d.name; })
    .attr("class", function(d){ return showing + " cat_"+d.id; })
    // depending on whether we're showing products or countries
    // show icons or just text of that region
    if(showing == "product"){
      a.append("img")
        .attr("src", function(d){
          return "/media/img/icons/community_"+d.id+".png"
        })
    }
    else {
      a.style("background", function(d){ return d.color; })
        .text(function(d){ return name(d.name); })
    }
    // mouseover events (extends the specific apps highlight funciton)
    a.on("mouseover", function(d){
        d3.select("#dataviz").call(app.highlight(d.id));
      })
      .on("mouseout", function(d){
        d3.select("#dataviz").call(app.highlight(null));
      })
  }
  
  // HELPER FUNCTION to shorten names so they fit on one line
  // totally for aesthetics braaaaaa....
  function name(long_name){
    var short_name = long_name;
    short_name = short_name.replace("South-Eastern", "SE")
    short_name = short_name.replace("Eastern", "E")
    short_name = short_name.replace("Northern", "N")
    short_name = short_name.replace("Southern", "S")
    short_name = short_name.replace("South", "S")
    short_name = short_name.replace("Western", "W")
    short_name = short_name.replace("Central", "C")
    return short_name;
  }
  
  ////////////////////////////////////////////
  // PUBLIC getter / setter functions
  ////////////////////////////////////////////
  key.showing = function(value) {
    if (!arguments.length) return showing;
    showing = value;
    return key;
  };
  
  key.classification = function(value) {
    if (!arguments.length) return classification;
    classification = value;
    return key;
  };
  
  /////////////////////////////////////////////////////////////////////
  // BE SURE TO ALWAYS RETURN THE APP TO ALLOW FOR METHOD CHAINING
  ///////////////////////////////////////////////////////////////////// 
  return key;
}