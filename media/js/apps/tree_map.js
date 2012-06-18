function TreeMap(args){
  var _this = this;
  this.attr_data = args.attr_data;
  this.raw_data = args.raw_data;
  this.selector = args.selector || window;
  this.width = args.width || $(this.selector).width();
  this.height = args.height || $(this.selector).height();
  this.year = args.year || 2009;
  this.mouseover = args.other ? args.other.mouseover || "true" : "true";
  this.total = args.other ? args.other.total || "true" : "true";
  this.current_data = this.raw_data.filter(function(x){return x.year == _this.year});

  // If there is no data
  if(!this.current_data.length){ return; }

  this.heirarchical_data = tm_make_data_heirarchical(this.current_data, this.attr_data);

  // Create treemap as SVG
  this.tree_map = d3.layout.treemap()
    .size([this.width, this.height])
    .sticky(false)
    .sort(function(a, b) { return a.value - b.value; });

  this.svg = d3.select(this.selector).html("").append("svg")
    .attr("width", this.width)
    .attr("height", this.height)
  this.viz = this.svg.append("g")
    .attr("class", "viz")
    .data([this.heirarchical_data])
  if(this.total == "true"){
    this.viz.attr("transform", "translate(0, 20)");
  }
}

TreeMap.prototype.build = function(){
	var _this = this;
	// Enter
	this.tree_map.value(function(d) {
		return d["value"];
	})
	var cell = _this.viz.selectAll("g")
		.data(this.tree_map)
		
	var cell_enter = cell.enter().append("g")
		.attr("class", function(d){
			if(!d.children){
				return "cat_"+_this.attr_data[d.data.item_id].category_id;
			}
		})
		
	cell_enter.append("rect").attr("fill", "white").attr("stroke", "white");
	cell_enter.append("text")
	// Update
	cell.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
	cell.select("rect")
		.attr("stroke", "white")
		.attr("stroke-width", 0.4)
		.attr("fill", function(d) {
			if(d.children){
				return "white";
			}
			else {
				return _this.attr_data[d.data.item_id].category_color;
			}
		})
		.attr("width", function(d){ 
			if(d.dx < 0){
				return 0;
			}
			else if(d.dx > 1){
				return d.dx-1;
			}
			return d.dx 
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
	cell.select("text")
		.attr("font-family", "'PT Sans Narrow', 'Arial Narrow', 'Helvetica Neue', Helvetica, Arial, sans-serif")
		.attr("font-stretch", "condensed")
		.attr("font-size", tmap_get_text_height("font-size"))
		.attr("letter-spacing", "-1px")
		// .attr("font-family", '"HelveticaNeue-Light", "Helvetica Neue Light", "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;')
		// .attr("font-weight", "300")
		// .attr("font-family", "'Knockout-HTF29-JuniorLiteweight'")
		.attr("x", 2)
		// .attr("y", 10)
		.attr("y", tmap_get_text_height("y"))
		.attr("fill", function(d) {
			if(d.children){
				return null;
			}
			else {
				return _this.attr_data[d.data.item_id].category_text_color ? _this.attr_data[d.data.item_id].category_text_color : "white";
			}
		})
		.attr("text-anchor", "start")
		.each(function(d, i){
			if(!d.children && (d.dx > 35 && d.dy > 25)){
				// format_text(d, this, _this.attr_data[d.data.item_id].name);
				_this.format_text(this, d);
			}
		})
  // Exit
  cell.exit().remove();
  // Events
  if(_this.mouseover == "true"){
    this.add_mouse_events();
  }
  // Show totals
  if(_this.total == "true"){
    this.add_total();
  }
}











/*
 * Tree map helper functions
 */
function tm_make_data_heirarchical(this_years_data, attrs){
	var heirarchical_data = {children: []};
	for(var i = 0; i < this_years_data.length; i++){
		tm_memoize(this_years_data[i], heirarchical_data, attrs);
	}
	return heirarchical_data;
}
function tm_memoize(node, root, attrs) {
	if(!node.heirarchical_id){
    if(!attrs[node.item_id]){
      return
    }
		node.heirarchical_id = attrs[node.item_id].heirarchical_id;
		// node.heirarchical_id = attrs[node.item_id].heirarchical_id.substr(0, 4);
	}
	var i = node.heirarchical_id.lastIndexOf("."), 
		p = i < 0 ? root : tm_memoize({"heirarchical_id": node.heirarchical_id.substring(0, i), children: []}, root, attrs), 
		n = p.children.length; 
	for (i = -1; ++i < n;) { 
		if (p.children[i].heirarchical_id === node.heirarchical_id) { 
			return p.children[i]; 
		} 
	} 
	p.children.push(node); 
	return node; 
}
TreeMap.prototype.format_text = function(element, d){
	// remove incumbent
	d3.select(element).selectAll("tspan").remove();
	if(parseInt(element) == element){
		element = this;
	}
	var title = this.attr_data[d.data.item_id].name;
	var percentage = d3.format(".2p")(d.value / d.parent.parent.parent.value), // format percentage to 2 decimal places
		text = percentage + " " + title;
		words = text.split(" "); // split text into array of words
		svg_tspan = d3.select(element).append("tspan").text(words[0]+" ")
		curr_tspan = svg_tspan;
	// loop through each word and see if it fits
	for(var i = 1; i < words.length; i++){
		// add a word and see if it fits
		curr_text = curr_tspan.text()
		curr_tspan.text(curr_text + " " + words[i]);
		// doesn't fit
		if (element.getBBox().width > (d.dx - 10)) {
			curr_tspan.text(curr_text)
			var new_text = words[i]
			curr_tspan = d3.select(element).append("tspan").text(new_text + " ")
				.attr("x", 2)
				.attr("dy", tmap_get_text_height("dy"))		
			// Just added the new tspan, see if it's still too big with that one new word.
			var frac = 6
			var second_half
		}
		if(element.getBBox().width > (d.dx -1)){
				// while the word still doesn't fit, cut off the end, add the first bit to the tspan
				while(element.getBBox().width > (d.dx-1) && frac > 2){
					point = new_text.length*frac/8
					var first_half = new_text.substring(0,point) + "-";
					if(new_text.substring(point-1,point) == "-"){
						first_half = new_text.substring(0,point);
					}
					curr_tspan.text(first_half)
					second_half = new_text.substr(point)
					frac = frac - 1
				}
				
				new_text = second_half
				// Here's the part I'm adding to the new tspan
				curr_tspan = d3.select(element).append("tspan").text(new_text + " ")
				.attr("x", 2)
				.attr("dy", tmap_get_text_height("dy"))
		}
		if (element.getBBox().height > (d.dy - 12)) {
			return;
		}
	}
}

TreeMap.prototype.add_mouse_events = function(){
	var _this = this;
	var cell = this.viz.selectAll("g")
	cell.on("mouseover", function(d){
		var sub_text = "Value: $" + format_big_num(d.value)[0] + format_big_num(d.value)[1]
			sub_text += " Share: " + d3.format(".2p")(d.value / d.parent.parent.parent.value)
			sub_text += d.data.rca ? " RCA: " + d3.format(".2f")(d.data.rca) : "";
		var a = _this.attr_data[d.data.item_id]; // This items attributes
		var mouseover_d = {
			"title": a.name,
			"img_src": a.code ? "/media/img/icons/community_"+a.category_id+".png" : "/media/img/icons/flag_"+a.name_3char.toLowerCase()+".png",
			"sub_text": sub_text
		}
		make_mouseover(this, [_this.width, _this.height], mouseover_d)
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

TreeMap.prototype.add_total = function(){
  var total_val = 0;
  this.current_data.forEach(function(x){
    total_val += parseFloat(x["value"]);
  })
  var _this = this;
  var total = _this.svg.append("g")
    .attr("class", "total")
  total.append("line")
    .attr("x1", 0).attr("y1", 10)
    .attr("x2", _this.width).attr("y2", 10)
    .attr("stroke", "#999")  
    .attr("stroke-widht", 0.5)
  total.append("line")
    .attr("x1", 1).attr("y1", 5)
    .attr("x2", 1).attr("y2", 15)
    .attr("stroke", "#999")
    .attr("stroke-widht", 0.5)
  total.append("line")
    .attr("x1", _this.width-1).attr("y1", 5)
    .attr("x2", _this.width-1).attr("y2", 15)
    .attr("stroke", "#999")
    .attr("stroke-widht", 0.5)

  var total_val = total.append("text")
    .attr("x", function(d){ return _this.width/2 })
    .attr("y", 15)
    .attr("fill", "black")
    .attr("text-anchor", "middle")
    .style("font-family", "'HelveticaNeue-Light', 'Helvetica Neue Light', 'Helvetica Neue', Helvetica, Arial, 'Lucida Grande', sans-serif")
    .style("font-weight", 300)
    .style("letter-spacing", "-.06em")
    .text(function(d){
      return "$"+d3.format(",f")(total_val);
    })
    
  var under_box = d3.select("g.total text").node().getBBox();
  var bg = total.append("rect")
    .attr("x", under_box.x-3).attr("y", under_box.y)
    .attr("width", under_box.width+6).attr("height", under_box.height)
    .attr("fill", "white")
  total_val.node().parentNode.appendChild(total_val.node())
}


function find_parent(e, name){
  if(e.nodeName == name){
    return e;
  }
  return find_parent(e.parentNode, name);
}
function format_big_num(d){
	d = parseFloat(d);
	var n = d;
	var s = "";
	var sign = "";
	if(d < 0){
		sign = "-"
	}
	d = Math.abs(d);
	if(d >= 1e3){
		n = d3.format(".2f")(d/1e3);
		s = "k";
	}
	if(d >= 1e6){
		n = d3.format(".2f")(d/1e6);
		s = "M";
	}
	if(d >= 1e9){
		n = d3.format(".2f")(d/1e9);
		s = "B";
	}
	if(d >= 1e12){
		n = d3.format(".2f")(d/1e12);
		s = "T";
	}
	if(d == 0){
		n = 0;
	}
	return [sign+n, s];
}
function make_mouseover(element, dimensions, data){
	// unpack function parameters
	var w = dimensions[0],
		h = dimensions[1],
		title = data.title,
		img_src = data.img_src,
		sub_text = data.sub_text,
		svg = find_parent(element, "svg");
		
	var info_h = h / 10;
	var padding = info_h * .10;
	// create grouping
	var info = d3.select(svg).append("g")
		.attr("class", "info")
		.attr("transform", function(d){
			var mouse_y = d3.svg.mouse(svg)[1];
			var y = mouse_y > h - info_h ? 0 : h - info_h;
			return "translate(0, "+y+")";
		})
	// create semi-transparent background
	info.append("rect")
		.attr("fill", "black")
		.attr("opacity", 0.6)
		.attr("x", 0)
		.attr("y", 0)
		.attr("width", w)
		.attr("height", info_h)
	// <image xlink:href="firefox.jpg" x="0" y="0" height="50px" width="50px"/>
	info.append("image")
		.attr("xlink:href", img_src)
		.attr("x", padding)
		.attr("y", padding)
		.attr("height", info_h/2)
		.attr("width", info_h/2)
	info.append("text")
		.attr("x", (padding*2) + (info_h/2))
		.attr("y", padding)
		.attr("dy", info_h/2 - padding)
		.attr("font-size", info_h/2)
		.attr("fill", "white")
		.style("text-shadow", "black 0.1em 0.1em 0.2em")
		.text(title)
	info.append("text")
		.attr("x", (padding*2) + (info_h/2))
		.attr("y", info_h - (padding*2))
		.attr("dy", info_h/4 - (padding*2))
		.attr("font-size", info_h/4)
		.attr("fill", "white")
		.style("text-shadow", "black 0.1em 0.1em 0.2em")
		.text(sub_text)
}
function tmap_get_text_height(attr){
	return function(d){
		var area = d.dy*d.dx
		var width = d.dx
		var height = d.dy
		if(area < 800 || width < 75 || height < 30){
			return attr == "font-size" ? "9px" : "10px";
		}
		else if(width < 75 || height < 50){
			return attr == "font-size" ? "12px" : "10px";
		}
		else if(area < 25000 && area>0){
			return attr == "font-size" ? Math.sqrt(Math.min(area/30, 900)) + "px" : Math.sqrt(Math.min(area/30, 900)) + "px";
		}
		else{
			return attr == "font-size" ? "35px" : "30px";
		}
	}
}