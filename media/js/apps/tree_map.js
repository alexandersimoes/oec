function App() {
  var width = 950, // default width
    height = 500, // default height
    margin = {top: 20, right: 0, bottom: 0, left: 0},
    format_num_abbrv = d3.format(".3s"),
    format_num = d3.format(",.0f"),
    currency = ["$", "USD"],
    format_percent = d3.format(".2p"),
    show_total = true,
    highlight,
    year,
    attr_data,
    data,
    tree_map = d3.layout.treemap()
      .size([width, height-margin.top])
      .sticky(false)
      .value(function(d){ return d.value })
      .sort(function(a, b) { return a.value - b.value; }),
    svg,
    viz;

  function a(selection) {
    selection.each(function(data, i) {
      
      attr_data = data.attr_data;
      
      // trim data to current year and cut exports below threshold
      current_year_data = data.data.filter(function(d){
        return d.year == year;
        // return d.year == year && d.share >= 0.0005;
      })
      // Nest data properly for tree map layout algorithm
      var heirarchical_data = make_data_heirarchical(current_year_data, attr_data);
      heirarchical_data = jQuery.extend(true, {}, heirarchical_data);
      
      // If there is no data, return a message saying so
      if(!current_year_data.length){ console.log("Sorry no data for this selection."); return; }
      
      // update tree map size (in case some crazy lunatic changed it)
      tree_map.size([width, height-margin.top])
      
      // Select the svg element, if it exists.
      var svg = d3.select(this).selectAll("svg").data([data]);

      // Otherwise, create the basic structure for the app.
      var svgEnter = svg.enter().append("svg");
      
      // If the show_total option is true (default) leave margin on top
      if(show_total){
        make_total(current_year_data);
      }
      
      // If it's the first time the app is being built, add this group element
      svgEnter.append("g").attr("class", "viz")
        .attr("transform", function(d){
          return "translate(0, "+margin.top+")";
        })
      
      /////////////////////////////////////////////////
      // Enter
      //////////////////////////////////////////////////
      // Ok, to get started, lets run our heirarchically nested
      // data object through the d3 treemap function to get a
      // flat array of data with X, Y, width and height vars
      var tmap_data = tree_map
        .nodes(heirarchical_data)
        .filter(function(d) { return !d.children; });
        // .value(function(d) { return d["value"]; })
      
      // add cell aka group container for each element
      var cell = d3.select("g.viz").selectAll("g")
        .data(tmap_data, function(d){ return d.item_id; })
      
      // call enter function attaching each datum to a new "g" element
      var cell_enter = cell.enter().append("g")
        .attr("class", function(d){
          return "cat_"+attr_data[d.item_id].category_id;
        })
      d3.selectAll("tspan").remove()
      cell_enter.append("rect")
      cell_enter.append("text")

      /////////////////////////////////////////////////
      // Update
      //////////////////////////////////////////////////
      // transform G
      cell.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
      // update rectangles
      cell.select("rect").call(rect)
      // update text
      cell.select("text").call(text)

      /////////////////////////////////////////////////
      // Exit
      //////////////////////////////////////////////////
      cell.exit().remove();
      
      return;
      
      if(key){
        a.set_key_behavior();
      }
      
      
    })
  }
  
  ////////////////////////////////////////////
  // PRIVATE functions for this app shhhhh...
  ////////////////////////////////////////////
  
  ////////////////////////////////////////////
  // PUBLIC getter / setter functions
  ////////////////////////////////////////////
  a.width = function(value) {
    if (!arguments.length) return width;
    width = value;
    return a;
  };

  a.height = function(value) {
    if (!arguments.length) return height;
    height = value;
    return a;
  };
  
  a.show_total = function(value) {
    if (!arguments.length) return show_total;
    show_total = value;
    return a;
  };
  
  a.year = function(value) {
    if (!arguments.length) return year;
    year = value;
    return a;
  };
  
  a.highlight = function(value) {
    if (!arguments.length) return highlight;
    highlight = value;
    return a;
  };
    
  function rect(rect){
    rect
      .attr("stroke", "white")
      .attr("stroke-width", 0.4)
      .attr("fill", function(d) {
        if(highlight && attr_data[d.item_id].category_id != highlight){
          return "#CCC";
        }
        return attr_data[d.item_id].category_color;
      })
      .attr("width", function(d){ 
        if(d.dx < 0){
          return 0;
        }
        else if(d.dx > 1){
          return d.dx-1;
        }
        return d.dx;
      })
      .attr("height", function(d){ 
        if(d.dy < 0){
          return 0;
        }
        else if(d.dy > 1){
          return d.dy-1;
        }
        return d.dy
      })
      .on("mousemove", mouseover)
      .on("mouseout", mouseout)
  }
  
  function mouseover(d){
    d3.select(this)
      .attr("stroke", "black")
      .attr("stroke-width", 2)
    make_mouseover({
      "width": width,
      "title": d.name,
      "category": attr_data[d.item_id].category_name,
      "category_color": attr_data[d.item_id].category_color,
      "category_text_color": attr_data[d.item_id].category_text_color,
      "values": [
        ["Value:", "$" + format_big_num(d.value)[0] + " " + format_big_num(d.value)[1]],
        ["RCA:", d3.format(".2f")(d.rca)],
        ["Share:", d.share]
      ]
    });    
  }
  
  function mouseout(){
    d3.select(this).attr("stroke", "none")
    make_mouseover();
  }
  
  function text(text){
    text
      .attr("font-family", "'PT Sans Narrow'," +
        "'Arial Narrow', 'Helvetica Neue', Helvetica, Arial, sans-serif")
      .attr("font-stretch", "condensed")
      .attr("letter-spacing", "-1px")
      .attr("x", 2)
      .attr("fill", function(d) {
        if(highlight && attr_data[d.item_id].category_id != highlight){
          return "#FFF";
        }
        return attr_data[d.item_id].category_text_color;
        // return attr_data[d.item_id].category_text_color ?
          // attr_data[d.item_id].category_text_color : "white";
      })
      .attr("text-anchor", "start")
      .style("pointer-events", "none")
      .each(draw_text_font_size)
      .each(draw_text_word_wrap)
  }
  
  function draw_text_font_size(d){
    var root_d = get_root(d);
    var share = format_percent(((d.value / root_d.value)));
    d.share = share;
    d.title = share + " " + attr_data[d.item_id].name;
    if(d.dx < 35 || d.dy < 25){
      return;
    }
    var size = d.dx/6,
      size = size > 40 ? 40 : size,
      size = size < 8 ? 8 : size,
      words = d.title.split(' '),
      word = words[0],
      width = d.dx,
      height = d.dy,
      length = 0;
    d3.select(this).style("font-size", size + "px").text(word);
    while(((this.getBBox().width >= width) || 
      (this.getBBox().height >= height)) && (size > 12)) {
      size--;
      d3.select(this).style("font-size", size + "px");
      this.firstChild.data = word;
    }
  }
    
  function draw_text_word_wrap(d, i){
    if(d.dx < 35 || d.dy < 25){
      return;
    }
    var max_width = d.dx;
    max_width = max_width - (parseInt(d3.select(this).style("font-size").replace('px',''))*0.25)*2;
    var max_height = d.dy;
    d3.select(this).select("tspan").remove()
    d3.select(this).text("")
    var dy = textFlow(d.title, this, max_width, max_height, 0, 10, false);
    d3.select(this).selectAll("tspan").attr("dy", "0.9em")
  }
  
  function add_mouse_events(){
    var cell = viz.selectAll("g")
    cell.on("mouseover", function(d){
      var sub_text = "Value: $" + format_big_num(d.value)[0] + format_big_num(d.value)[1]
        sub_text += " Share: " + d3.format(".2p")(d.value / d.parent.parent.parent.value)
        sub_text += d.data.rca ? " RCA: " + d3.format(".2r")(d.data.rca) : "";
      var a = attr_data[d.data.item_id]; // This items attributes
      var mouseover_d = {
        "title": a.name,
        "img_src": a.code ? "/media/img/icons/community_"+a.category_id+".png" : "/media/img/icons/flag_"+a.name_3char.toLowerCase()+".png",
        "sub_text": sub_text
      }
      make_mouseover(this, [width, height+margin.top], mouseover_d, margin.top)
      // to highlight the node create new box around it
      d3.select(this).select("rect")
        .attr("stroke", "black")
        .attr("stroke-width", 2)
    })
    cell.on("mouseout", function(d){
      d3.select("g.info").remove()
      d3.select(this).select("rect")
        .attr("stroke", "white")
        .attr("stroke-width", 1)
    })
  }
  
  function make_total(current_year_data){
    // Get the total value from the data passed.
    total_val = d3.sum(current_year_data, function(d){ return d["value"] })
    
    // Set the total value as data for element.
    var total = d3.select("svg").selectAll("g.title").data([total_val])
    
    // Draw lines and other chachki when element first enters.
    var total_enter = total.enter().append("g").attr("class", "title")
    total_enter.append("line")
      .attr("x1", 0).attr("y1", 10)
      .attr("x2", width).attr("y2", 10)
      .attr("stroke", "#999")  
      .attr("stroke-widht", 0.5)
    total_enter.append("line")
      .attr("x1", 1).attr("y1", 5)
      .attr("x2", 1).attr("y2", 15)
      .attr("stroke", "#999")
      .attr("stroke-widht", 0.5)
    total_enter.append("line")
      .attr("x1", width-1).attr("y1", 5)
      .attr("x2", width-1).attr("y2", 15)
      .attr("stroke", "#999")
      .attr("stroke-widht", 0.5)
    total_enter.append("text")
      .attr("x", function(d){ return width/2 })
      .attr("y", 15)
      .attr("fill", "black")
      .attr("text-anchor", "middle")
      .attr("font-family", "'PT Sans Narrow'," +
        "'Arial Narrow', 'Helvetica Neue', Helvetica, Arial, sans-serif")
      .style("font-weight", 300)
      .style("letter-spacing", "-.06em")
    total_enter.append("rect")
      .attr("fill", "white")
    
    // Set the text value to the total $$$ amount
    total_text = total.select("text").text(function(d){
      return "$"+d3.format(",f")(d);
    })
    // Funny little trick to make a white box under the text for legibility.
    var under_box = total.select("text").node().getBBox();
    total.select("rect")
      .attr("x", under_box.x-3).attr("y", under_box.y)
      .attr("width", under_box.width+6).attr("height", under_box.height)
    total_text.node().parentNode.appendChild(total_text.node())
  }
  
  /*
  Scripts to create flowText (rectangular) in SVG 1.1 UAs
  Copyright (C) <2007>  <Andreas Neumann>
  Version 1.0, 2007-02-26
  neumann@karto.baug.ethz.ch
  http://www.carto.net/
  http://www.carto.net/neumann/

  ----

  Documentation: http://www.carto.net/papers/svg/textFlow/

  ----
  */
  
  function textFlow(myText,textToAppend,maxWidth,maxHeight,x,ddy,justified) {
    
    var svgNS = "http://www.w3.org/2000/svg";
    var xlinkNS = "http://www.w3.org/1999/xlink";
    var cartoNS = "http://www.carto.net/attrib";
    var attribNS = "http://www.carto.net/attrib";
    var batikNS = "http://xml.apache.org/batik/ext";
    
    //extract and add line breaks for start
    var dashArray = new Array();
    var dashFound = true;
    var indexPos = 0;
    var cumulY = 0;
    while (dashFound == true) {
      var result = myText.indexOf("-",indexPos);
      if (result == -1) {
        //could not find a dash
        dashFound = false;
      }
      else {
        dashArray.push(result);
        indexPos = result + 1;
      }
    }
    //split the text at all spaces and dashes
    var words = myText.split(/[\s-]/);
    var line = "";
    var dy = 0;
    var dx = "0.15em"
    var curNumChars = 0;
    var computedTextLength = 0;
    var myTextNode;
    var tspanEl;
    var lastLineBreak = 0;

    for (i=0;i<words.length;i++) {
      var word = words[i];
      curNumChars += word.length + 1;
      if (computedTextLength > maxWidth || i == 0) {
        if (computedTextLength > maxWidth) {
          var tempText = tspanEl.firstChild.nodeValue;
          tempText = tempText.slice(0,(tempText.length - words[i-1].length - 2)); //the -2 is because we also strip off white space
          tspanEl.firstChild.nodeValue = tempText;
          if (justified) {
            //determine the number of words in this line
            var nrWords = tempText.split(/\s/).length;
            computedTextLength = tspanEl.getComputedTextLength();
            var additionalWordSpacing = (maxWidth - computedTextLength) / (nrWords - 1);
            tspanEl.setAttributeNS(null,"word-spacing",additionalWordSpacing);
            //alternatively one could use textLength and lengthAdjust, however, currently this is not too well supported in SVG UA's
          }
        }
        if(cumulY > maxHeight){
          return;
        }
        tspanEl = document.createElementNS(svgNS,"tspan");
        tspanEl.setAttributeNS(null,"x",x);
        tspanEl.setAttributeNS(null,"dx",dx);
        tspanEl.setAttributeNS(null,"dy",dy);
        myTextNode = document.createTextNode(line);
        tspanEl.appendChild(myTextNode);
        textToAppend.appendChild(tspanEl);

        if(checkDashPosition(dashArray,curNumChars-1)) {
          line = word + "-";
        }
        else {
          line = word + " ";
        }
        if (i != 0) {
          line = words[i-1] + " " + line;
        }
        dy = ddy;
        cumulY += dy + parseInt(d3.select(textToAppend).style("font-size").replace("px", ""));
      }
      
      else {
        if(checkDashPosition(dashArray,curNumChars-1)) {
          line += word + "-";
        }
        else {
          line += word + " ";
        }
      }
      tspanEl.firstChild.nodeValue = line;
      computedTextLength = tspanEl.getComputedTextLength();
      if (i == words.length - 1) {
        if (computedTextLength > maxWidth) {
          var tempText = tspanEl.firstChild.nodeValue;
          tspanEl.firstChild.nodeValue = tempText.slice(0,(tempText.length - words[i].length - 1));
          if(cumulY  > maxHeight){
            return;
          }
          tspanEl = document.createElementNS(svgNS,"tspan");
          tspanEl.setAttributeNS(null,"x",x);
          tspanEl.setAttributeNS(null,"dx",dx);
          tspanEl.setAttributeNS(null,"dy",dy);
          myTextNode = document.createTextNode(words[i]);
          tspanEl.appendChild(myTextNode);
          textToAppend.appendChild(tspanEl);
        }

      }
    }
    return cumulY;
  }

  //this function checks if there should be a dash at the given position, instead of a blank
  function checkDashPosition(dashArray,pos) {
    var result = false;
    for (var i=0;i<dashArray.length;i++) {
      if (dashArray[i] == pos) {
        result = true;
      }
    }
    return result;
  }
  
  /*
   * Tree map helper functions
   */
  function make_data_heirarchical(this_years_data, attrs){
    var heirarchical_data = {children: []};
    for(var i = 0; i < this_years_data.length; i++){
      memoize(this_years_data[i], heirarchical_data, attrs);
    }
    return heirarchical_data;
  }
  function memoize(node, root, attrs) {
  	if(!node.heirarchical_id){
      if(!attrs[node.item_id]){
        return
      }
      node.heirarchical_id = attrs[node.item_id].heirarchical_id;
    }
    var i = node.heirarchical_id.lastIndexOf("."), 
        p = i < 0 ? root : memoize({"heirarchical_id": node.heirarchical_id.substring(0, i), children: []}, root, attrs),
        n = p.children.length; 
    for (i = -1; ++i < n;) { 
      if (p.children[i].heirarchical_id === node.heirarchical_id) { 
        return p.children[i]; 
      } 
    } 
    p.children.push(node); 
    return node; 
  }
  
  /////////////////////////////////////////////////////////////////////
  // BE SURE TO ALWAYS RETURN THE APP TO ALLOW FOR METHOD CHAINING
  ///////////////////////////////////////////////////////////////////// 
  return a;
}