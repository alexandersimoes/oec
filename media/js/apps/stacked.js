function Stacked(args){
	
	this.attr_data = args.attr_data;
	this.raw_data = args.raw_data;
	this.selector = args.selector || window;
	this.width = args.width || $(selector).width();
	this.height = args.height || $(selector).height();
	this.padding = [0, 45, 30, 0];
	
	var year_parts = args.year.split(".").map(function(y){ return parseInt(y); });
	this.years = d3.range(year_parts[0], year_parts[1]+1, year_parts[2]);
	
	this.mouseover = args.other ? args.other.mouseover || "true" : "true";
	this.sort = args.other ? args.other.sort || "category" : "category";
	this.labels = args.other ? args.other.labels || "true" : "true";
	this.layout = args.other ? args.other.layout || "value" : "value";
	
	var stacked_width = this.width - this.padding[1] - this.padding[3];
	var stacked_height = this.height - this.padding[0] - this.padding[2];
	
	// Nest raw data
	this.raw_data = d3.nest()
		.key(function(d) { return d["item_id"]; })
		.key(function(d) { return d["year"]; })
		.rollup(function(d){
			return d[0]
		})
		.map(this.raw_data);
	
	this.std = st_data(this.raw_data, this.attr_data, this.years, this.sort);
	
	this.stack = d3.layout.stack()
		.values(function(d) { return d["years"]; })
	this.layout == "value" ? this.stack.offset("zero") : this.stack.offset("expand");
	this.data = this.stack(this.std);

	this.color = d3.interpolateRgb("#daa", "#955");
	this.max_x = this.years.length - 1;
	this.max_y = d3.max(this.data, function(d) {
		return d3.max(d["years"], function(d) {
			return d.y0 + d.y;
		});
	});

	this.area = d3.svg.area()
		.x(function(d) { return d.x * stacked_width / this.max_x; })
		.y0(function(d) { return stacked_height - d.y0 * stacked_height / this.max_y; })
		.y1(function(d) { return stacked_height - (d.y + d.y0) * stacked_height / this.max_y; });

}

Stacked.prototype.build = function(){
	var _this = this;
	this.svg = d3.select(this.selector).html("").append("svg")
		.attr("width", this.width)
		.attr("height", this.height);

	var stacked = this.svg.append("g")
		.attr("class", "stacked")
		.attr("transform", "translate(" + this.padding[3] + "," + this.padding[0] + ")");
		
	var paths = stacked.selectAll("path")
		.data(this.data).enter().append("path")
		.attr("class", function(d){
			return "cat_"+d.meta.category_id;
		})
		.attr("fill", function(d) {
			return d.meta.category_color;
		})
		.attr("d", function(d, i){
			return _this.area(d.years)
		})
	
	// Y axis
	this.y_axis();
	// X axis
	this.x_axis();
	
	// Other options
	if(this.mouseover == "true"){
		this.add_mouse_events();
	}
	if(this.labels == "true"){
		this.draw_labels();
	}
}

Stacked.prototype.add_mouse_events = function(){
	var _this = this;
	this.svg.selectAll("g.stacked path").on("mouseover", function(d){
		var sub_text = ""
		var mouseover_d = {
			"title": d.meta.name,
			"img_src": d.meta.code ? "http://atlas.media.mit.edu/media/img/icons/community_"+d.meta.category_id+".png" : "http://atlas.media.mit.edu/media/img/icons/flag_"+d.meta.name_3char.toLowerCase()+".png",
			"sub_text": sub_text
		}
		make_mouseover(this, [_this.width, _this.height], mouseover_d)
		// to highlight the node create new box around it
		d3.select(this)
			.attr("stroke", "black")
			.attr("stroke-width", 2)
	})
	this.svg.selectAll("g.stacked path").on("mouseout", function(d){
		_this.svg.select(".info").remove()
		d3.select(this)
			.attr("stroke", null)
	})
}

Stacked.prototype.change_layout = function(layout){
	var _this = this;
	
	this.std = st_data(this.raw_data, this.attr_data, this.years, this.sort);
	if(layout == "stacked_value"){
		this.data = this.stack.offset("zero")(this.std)
	}
	else {
		this.data = this.stack.offset("expand")(this.std)
	}

	this.max_y = d3.max(this.data, function(d) {
		return d3.max(d["years"], function(d) {
			return d.y0 + d.y;
		});
	});

	this.svg.selectAll("path").data(this.data).attr("d", function(d, i){
		return _this.area(d.years)
	})
	
	// update y axis
	this.y_axis();
	
	if(this.labels == "true"){
		this.draw_labels();
	}
}

Stacked.prototype.y_axis = function(){
	var _this = this;
	var stacked_height = _this.height - _this.padding[0] - _this.padding[2];
	var y = d3.scale.linear()
		.domain([0, _this.max_y])
		.range([stacked_height, 0]);

	var xx = (this.width - _this.padding[1]) + 2;
	
	var y_axis = _this.svg.select("g.y_axis");
	if(y_axis.node()){
		y_axis.remove();
	}
	y_axis = _this.svg.append("g")
		.attr("class", "y_axis")
		.attr("transform", "translate(" + xx + "," + _this.padding[0] + ")")

	y_axis.selectAll("line")
		.data(y.ticks(10))
		.enter().append("line")
		.attr("class", "ticks")
		.attr("x1", 0)
		.attr("x2", 8)
		.attr("y1", y)
		.attr("y2", y)
		.attr("stroke", "black");

	y_axis.append("line")
		.attr("x1", 0)
		.attr("x2", 0)
		.attr("y1", stacked_height)
		.attr("y2", 0)
		.attr("stroke", "black");
	
	y_axis.selectAll("text")
		.data(y.ticks(10))
		.enter().append("text")
		.style("font", "11px sans-serif")
		.attr("x", 10)
		.attr("y", function(d, i){
			if(d == 1) return y(d) + 3;
			return y(d);
		})
		.attr("dy", 5)
		.attr("text-anchor", "left")
		.text(st_format_text);
}

Stacked.prototype.x_axis = function(){
	var _this = this;
	var stacked_width = _this.width - this.padding[1] - this.padding[3];
	var x = d3.scale.linear()
		.domain([0, _this.max_x])
		.range([0, stacked_width]);

	var yy = (this.height - this.padding[2]) + 2;
	var x_axis = _this.svg.append("g")
		.attr("class", "x_axis")
		.attr("transform", "translate(" + _this.padding[3] + "," + yy + ")")

	x_axis.selectAll("line")
		.data(x.ticks(_this.max_x))
		.enter().append("line")
		.attr("x1", x)
		.attr("x2", x)
		.attr("y1", 0)
		.attr("y2", 10)
		.attr("stroke", "black");
	
	x_axis.append("line")
		.attr("x1", 0)
		.attr("x2", stacked_width)
		.attr("y1", 0)
		.attr("y2", 0)
		.attr("stroke", "black");

	x_axis.selectAll("text")
		.data(x.ticks(10))
		.enter().append("text")
		.style("font", "11px sans-serif")
		.attr("x", x)
		.attr("y", 25)
		.attr("dy", -3)
		.attr("text-anchor", function(d, i){
			if(i == 0) return "start";
			if(i == _this.years.length-1) return "end";
			return "middle"
		})
		.text(function(d){
			return _this.years[d]
		});
}

Stacked.prototype.draw_labels = function(){
	var _this = this;
	this.svg.select("g.stacked").selectAll("text").remove();
	var labels = this.svg.select("g.stacked").selectAll("text")
		.data(this.data).enter().append("text")
		.attr("x", function(d){
			var max = 0;
			var max_index = 0;
			d.years.forEach(function(year, i){
				if(year.y > max){
					max = year.y;
					max_index = i;
				}
			})
			var paths = _this.area(d.years).split("L");
			var largest_path = paths[max_index]
			if(max_index == d.years.length-1){
				return largest_path.split(",")[0].replace("M", "") - 10;
			}
			else if(max_index == 0){
				return largest_path.split(",")[0].replace("M", "") + 10;
			}
			return largest_path.split(",")[0].replace("M", "");
		})
		.attr("y", function(d){
			var max = 0;
			var max_index = 0;
			d.years.forEach(function(year, i){
				if(year.y > max){
					max = year.y;
					max_index = i;
				}
			})
			var paths = _this.area(d.years).split("L");
			var largest_path_top = paths[max_index]
			var largest_path_bottom = paths[paths.length - 1 - max_index]
			var y = (parseFloat(largest_path_bottom.split(",")[1]) + parseFloat(largest_path_top.split(",")[1])) / 2;
			return y;
		})
		.attr("text-anchor", function(d){
			var max = 0;
			var max_index = 0;
			d.years.forEach(function(year, i){
				if(year.y > max){
					max = year.y;
					max_index = i;
				}
			})
			if(max_index == d.years.length-1){
				return "end";	
			}
			else if(max_index == 0){
				return "start";	
			}
			return "middle";
		})
		.attr("fill", function(d){
			return d.meta.ps ? d.meta.category.text_color : "white";
		})
		.style("text-shadow", "#bbb 1px 1px 2px")
		.attr("font-family", "'PT Sans Narrow', 'Helvetica Neue', Helvetica, Arial, sans-serif")
		.attr("font-size", function(d){
			var max = 0;
			var max_index = 0;
			d.years.forEach(function(year, i){
				if(year.y > max){
					max = year.y;
					max_index = i;
				}
			})
			var paths = _this.area(d.years).split("L");
			var largest_path_top = paths[max_index]
			var largest_path_bottom = paths[paths.length - 1 - max_index]
			var diff = parseFloat(largest_path_bottom.split(",")[1]) - parseFloat(largest_path_top.split(",")[1]);
			if(diff > 100){
				return "28px";
			}
			if(diff > 50){
				return "24px";
			}
			if(diff > 30){
				return "16px";
			}
			if(diff > 20){
				return "12px";
			}
			return "9px"
		})
		.text(function(d){
			return d.meta.name;
		})
		.style("display", function(d){
			var max = 0;
			var max_index = 0;
			d.years.forEach(function(year, i){
				if(year.y > max){
					max = year.y;
					max_index = i;
				}
			})
			var paths = _this.area(d.years).split("L");
			var largest_path_top = paths[max_index]
			var largest_path_bottom = paths[paths.length - 1 - max_index]
			// console.log(largest_path_top, largest_path_bottom)
			// console.log(d.meta.name, max, area(d.years).split("L"))
			// return largest_path.split(",")[0].replace("M", "");
			var diff = parseFloat(largest_path_bottom.split(",")[1]) - parseFloat(largest_path_top.split(",")[1]);
			// console.log(diff)
			if(diff < 15){
				return "none";
			}
			return "block";
		})
}






























/*
 * stacked helper functions
 */
function st_data(raw_data, attributes, years, sorting){
	var data = [];
	var attribute_ids = d3.keys(raw_data);

	attribute_ids.forEach(function(id){
		var d = attributes ? {"years":[], "meta":attributes[id]} : {"years":[]};
		years.forEach(function(y, i){
			var result = {"x": i, "y": 0};
			if(raw_data[id][y]){
				result["y"] = raw_data[id][y]["value"];
			}
			d["years"].push(result)
		})
		data.push(d)
	})

	data.forEach(function(s) {
		s.max = d3.max(s.years, function(d) { return d.y; });
		s.sum = d3.sum(s.years, function(d) { return d.y; });
	});

	if(sorting == "value"){
		// Sort by totals
		data.sort(function(a, b) {
			return b.sum - a.sum;
		})
	}
	else if(sorting == "name"){
		// Sort by community name
		data.sort(function(a, b) {
			var name_a = a.meta.name.toLowerCase();
			var name_b = b.meta.name.toLowerCase();
			if (name_a < name_b) {return -1}
			if (name_a > name_b) {return 1}
			return 0;
		})
	}
	else{
		// Sort by category id
		data.sort(function(a, b) {
			// var cat_a = a.meta.community ? a.meta.community.id : a.meta.region.id;
			// var cat_b = b.meta.community ? b.meta.community.id : b.meta.region.id;
			var cat_a = a.meta.category_id;
			var cat_b = b.meta.category_id;
			if (cat_a < cat_b) {return -1}
			if (cat_a > cat_b) {return 1}
			return 0;
		})
	}

	return data;
}
function st_format_text(d){
	var n = d;
	if(d >= 0){
		n = d3.format("%")(d)
	}
	if(d >= 1e3){
		n = d3.format("2g")(d/1e3) + " k"
	}
	if(d >= 1e6){
		n = d3.format("2g")(d/1e6) + " M"
	}
	if(d >= 1e9){
		n = d3.format("2g")(d/1e9) + " B"
	}
	if(d >= 1e12){
		n = d3.format("2g")(d/1e12) + " T"
	}
	if(d == 0){
		n = 0;
	}
	return n;
}