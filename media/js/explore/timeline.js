function Timeline() {
  var year = 1962,
    app_type,
    timeout;
    
  function timeline(selection) {
    selection.each(function(data, i) {
      
      // Get unique list of years, only the ones that are available!!!
      years = {}
      data.forEach(function(d){ years[parseInt(d.year)] = 1; })
      years = d3.keys(years)
			var max_of_array = Math.max.apply(Math, years);
			var min_of_array = Math.min.apply(Math, years);
			console.log(min_of_array);
			console.log(max_of_array);
			// init the timeline
      var slider_year = [year]
      if(app_type == "stacked"){
        slider_year = [year.split(".")[0], year.split(".")[1]]
        var slider_interval = [year.split(".")[2]]
        $("#timeline .slider#year").slider({
          range: true, 
          values: slider_year,
          min: parseInt(min_of_array),//years[0]),
          max: parseInt(max_of_array)//years[years.length-1])
        });
        $("#timeline .slider#interval").slider({
          range: "min", 
          value: year.split(".")[2],
          min: 1,
          max: 10
        });
        $("#timeline .slider#interval").bind("slide", function(event, ui) {
          d3.selectAll(".slider#interval .ui-slider-handle").data([ui.value]).text(function(d){ return d; })
          var current_years = year.split(".")
          current_years[0] = $("#timeline .slider#year").slider("option", "values")[0]
          current_years[1] = $("#timeline .slider#year").slider("option", "values")[1]
          current_years[2] = ui.value
          d3.select("#dataviz").call(app.year(current_years.join(".")));
          d3.select("#tool_pane").call(controls.year(current_years.join(".")));
        })
        $("#timeline .slider#year").bind("slide", function(event, ui) {
          $("#timeline #stop").click();
          slider_year = ui.values;
          if(ui.values[1] - ui.values[0] < 2){
            return false;
          }
          var current_years = year.split(".")
          current_years[0] = ui.values[0];
          current_years[1] = ui.values[1];
          current_years[2] = $("#timeline .slider#interval").slider("option", "value");
          d3.select("#dataviz").call(app.year(current_years.join(".")));
          d3.select("#tool_pane").call(controls.year(current_years.join(".")));
          d3.selectAll("#year .ui-slider-handle").data(slider_year).text(function(d){ return d; })
          d3.selectAll(".slider#interval .ui-slider-handle").data([$("#timeline .slider#interval").slider("option", "value")]).text(function(d){ return d; })
        });
        d3.selectAll(".slider#interval .ui-slider-handle").data(slider_interval).text(function(d){ return d; })
      }
      else {
				$("#timeline .slider#year").slider({
          range: "min", 
          value: slider_year[0], 
					min: parseInt(min_of_array),//years[0]),
          max: parseInt(max_of_array)//years[years.length-1])
        });
				
				$("#timeline .slider#year").bind("slide", function(event, ui) {
          $("#timeline #stop").click();
          // check if it's a range slider or not
					slider_year = [ui.value];
          d3.select("#dataviz").call(app.year(ui.value));
          d3.select("#tool_pane").call(controls.year(ui.value));
          d3.selectAll("#year .ui-slider-handle").data(slider_year).text(function(d){ return d; })
        });
      }
      d3.selectAll(".slider#year .ui-slider-handle").data(slider_year).text(function(d){ return d; })
      
      // Handle radio buttons for stacked options
      if(app_type == "stacked"){
        $("#stacked_labels").buttonset();
        $("#stacked_order").buttonset();
        $("#stacked_layout").buttonset();
        $("#stacked_controls input[type='radio']").change(function(e){
          if($(e.target).attr("name") == "labels"){
            d3.select("#dataviz").call(app.labels($(e.target).attr("id")));
          }
          if($(e.target).attr("name") == "layout"){
            d3.select("#dataviz").call(app.layout($(e.target).attr("id")));
          }
          if($(e.target).attr("name") == "order"){
            d3.select("#dataviz").call(app.order($(e.target).attr("id")));
          }
        })
        // Now that we're done loading UI elements show the parent element
        $("#stacked_controls").show();
      }
      
      // next and prev buttons override link URLs
      $("#timeline a.prev, #timeline a.next").click(function(){
        var y = parseInt($("#timeline .slider").slider("option", "value"));
        var y_first = years[0]
        var y_last = years[years.length-1]
        if($(this).attr("class") == "next"){
          y = (y >= y_last) ? y_first : y+1;
        } else {
          y = (y <= y_first) ? y_last : y-1;
        }
        $("#timeline .slider").slider("option", "value", y);
        d3.select("#dataviz").call(app.year(y));
        d3.select("#tool_pane").call(controls.year(y));
        d3.selectAll("#year .ui-slider-handle").data([y]).text(function(d){ return d; })
        return false;
      })
      
      // next and prev buttons override link URLs
      $("#timeline #play").click(function(){
        $("#timeline #stop").show();
        $("#timeline #play").hide();
        timeout = setInterval(function(){
          var y = parseInt($("#timeline .slider").slider("option", "value"));
          var y_first = years[0]
          var y_last = years[years.length-1]
          y = (y >= y_last) ? y_first : y+1;
          $("#timeline .slider").slider("option", "value", y);
          if(y == y_last) {
            d3.select("#dataviz").call(app.year(y));
            d3.select("#tool_pane").call(controls.year(y));
            d3.selectAll("#year .ui-slider-handle").data([y]).text(function(d){ return d; })
            $("#timeline #stop").click();
            return;
          }
          d3.select("#dataviz").call(app.year(y));
          d3.select("#tool_pane").call(controls.year(y));
          d3.selectAll("#year .ui-slider-handle").data([y]).text(function(d){ return d; })
        }, 750);
      })
      $("#timeline #stop").click(function(){
        $("#timeline #stop").hide();
        $("#timeline #play").show();
        clearInterval(timeout);
      })
      
    })
  }

  ////////////////////////////////////////////
  // PUBLIC getter / setter functions
  ////////////////////////////////////////////
  timeline.year = function(value) {
    if (!arguments.length) return year;
    year = value;
    return timeline;
  };
  
  timeline.app_type = function(value) {
    if (!arguments.length) return app_type;
    app_type = value;
    return timeline;
  };
  
  ////////////////////////////////////////////
  // PRIVATE functions for this app shhhhh...
  ////////////////////////////////////////////
  
  
  /////////////////////////////////////////////////////////////////////
  // BE SURE TO ALWAYS RETURN THE APP TO ALLOW FOR METHOD CHAINING
  ///////////////////////////////////////////////////////////////////// 
  return timeline;
}