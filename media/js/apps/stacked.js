function stacked_draw(args){
	
	var attr_data = args.attr_data,
		raw_data = args.raw_data,
		selector = args.selector || window,
		width = args.width || $(selector).width(),
		height = args.height || $(selector).height(),
		padding = [0, 45, 30, 0],
		w = width - padding[1] - padding[3],
		h = height - padding[0] - padding[2],
		year_parts = args.year.split(".").map(function(y){ return parseInt(y); }),
		years = d3.range(year_parts[0], year_parts[1]+1, year_parts[2]),
		mouseover = args.mouseover || "true",
		sort = args.sort || "category",
		labels = args.labels || "true",
		layout = args.layout || "value";
	
	// Nest raw data
	var raw_data = d3.nest()
		.key(function(d) { return d["item_id"]; })
		.key(function(d) { return d["year"]; })
		.rollup(function(d){
			return d[0]
		})
		.map(raw_data);
	
	var std = st_data(raw_data, attr_data, years, sort);
	
	var stacked_value = d3.layout.stack()
		.values(function(d) { return d["years"]; })
		.offset("zero")
	var stacked_share = d3.layout.stack()
		.values(function(d) { return d["years"]; })
		.offset("expand");
	var data = layout == "value" ? stacked_value(std) : stacked_share(std);

	var color = d3.interpolateRgb("#daa", "#955");
	var max_x = years.length - 1;
    var max_y = d3.max(data, function(d) {
		return d3.max(d["years"], function(d) {
			return d.y0 + d.y;
		});
	});

	var area = d3.svg.area()
	    .x(function(d) { return d.x * w / max_x; })
	    .y0(function(d) { return h - d.y0 * h / max_y; })
	    .y1(function(d) { return h - (d.y + d.y0) * h / max_y; });

	var svg = d3.select(selector).html("").append("svg:svg")
		.attr("width", w + padding[1] + padding[3])
		.attr("height", h + padding[0] + padding[2]);

	var stacked = svg.append("svg:g")
		.attr("class", "stacked")
		.attr("transform", "translate(" + padding[3] + "," + padding[0] + ")");
		
	var paths = stacked.selectAll("path")
		.data(data).enter().append("svg:path")
		.attr("class", function(d){
			return d.meta.category_id;
		})
		.attr("fill", function(d) {
			return d.meta.category_color;
		})
		.attr("d", function(d, i){
			return area(d.years)
		})
	
	if(mouseover == "true"){
		paths.on("mouseover", function(d){
			// var sub_text = "Value: " + format_big_num(d.value)[0] + format_big_num(d.value)[1]
			// 	sub_text += " Share: " + d3.format(".2p")(d.value / d.parent.parent.parent.value)
			// 	sub_text += d.data.rca ? " RCA: " + d3.format(".2f")(d.data.rca) : "";
			var sub_text = ""
			var mouseover_d = {
				"title": d.meta.name,
				"img_src": d.meta.code ? "http://atlas.media.mit.edu/media/img/community_icons/community_"+d.meta.category_id+".png" : "http://atlas.media.mit.edu/media/img/flags/flag_"+d.meta.name_3char.toLowerCase()+".png",
				"sub_text": sub_text
			}
			make_mouseover(this, [width, height], mouseover_d)
			// to highlight the node create new box around it
			d3.select(this)
				.attr("stroke", "black")
				.attr("stroke-width", 2)
		})
		paths.on("mouseout", function(d){
			svg.select(".info").remove()
			d3.select(this)
				.attr("stroke", null)
		})
	}
	
	
	if(labels == "true"){
		draw_labels(stacked, data, area);
	}
	
	
	
	
	st_yaxis(svg, w, h, padding, max_y);
	
	var x = d3.scale.linear()
		.domain([0, max_x])
		.range([0, w]);

	// x = d3.time.scale().range([0, w]).domain([d3.time.format("%Y").parse(years[0]+""), d3.time.format("%Y").parse(years[years.length - 1]+"")])
	// var xAxis = d3.svg.axis().scale(x).ticks(5).orient("bottom").tickSize(20).tickSubdivide(false);

	var yy = padding[0]+h+2;
	var x_axis = svg.append("svg:g")
		.attr("class", "x_axis")
		.attr("transform", "translate(" + padding[3] + "," + yy + ")")

	x_axis.selectAll("line")
		.data(x.ticks(max_x))
		.enter().append("svg:line")
		.attr("x1", x)
		.attr("x2", x)
		.attr("y1", 0)
		.attr("y2", 10)
		.attr("stroke", "black");
	
	x_axis.append("svg:line")
		.attr("x1", 0)
		.attr("x2", w)
		.attr("y1", 0)
		.attr("y2", 0)
		.attr("stroke", "black");

	x_axis.selectAll("text")
		.data(x.ticks(10))
		.enter().append("svg:text")
		.style("font", "11px sans-serif")
		.attr("x", x)
		.attr("y", 25)
		.attr("dy", -3)
		.attr("text-anchor", function(d, i){
			if(i == 0) return "start";
			if(i == years.length-1) return "end";
			return "middle"
		})
		.text(function(d){
			return years[d]
		});
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


function st_yaxis(svg, w, h, padding, max_y, update){
	var y = d3.scale.linear()
		.domain([0, max_y])
		.range([h, 0]);

	var xx = padding[3]+w+2;
	
	var y_axis = svg.append("svg:g")
		.attr("class", "y_axis")
		.attr("transform", "translate(" + xx + "," + padding[0] + ")")
		// .call(yAxis);

	y_axis.selectAll("line")
		.data(y.ticks(10))
		.enter().append("svg:line")
		.attr("class", "ticks")
		.attr("x1", 0)
		.attr("x2", 8)
		.attr("y1", y)
		.attr("y2", y)
		.attr("stroke", "black");

	y_axis.append("svg:line")
		.attr("x1", 0)
		.attr("x2", 0)
		.attr("y1", h)
		.attr("y2", 0)
		.attr("stroke", "black");
	
	y_axis.selectAll("text")
		.data(y.ticks(10))
		.enter().append("svg:text")
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
function draw_labels(stacked, data, area){
	var labels = stacked.selectAll("text")
		.data(data).enter().append("svg:text")
		.attr("x", function(d){
			var max = 0;
			var max_index = 0;
			d.years.forEach(function(year, i){
				if(year.y > max){
					max = year.y;
					max_index = i;
				}
			})
			var paths = area(d.years).split("L");
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
			var paths = area(d.years).split("L");
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
			var paths = area(d.years).split("L");
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
			var paths = area(d.years).split("L");
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