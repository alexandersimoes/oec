function download(container, csv_data){
  return function(){

    d3.selectAll(".modal#download").classed("active", true);
    d3.selectAll("#mask").classed("visible", true);
    d3.selectAll("body").classed("frozen", true);

    d3.selectAll(".modal#download a.download_button").on("click", function(){

      var format = d3.select(this).attr("id");

      var title = window.location.pathname.split("/")
      title.splice(0, 1)
      title.splice(0, 1)
      title.splice(title.length-1, 1)
      title = title.join("_").replace("embed", "explore")

      if(format == "svg" || format == "png"){
        var svg = d3.select(container).select("svg")
          .attr("title", title)
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg")

        // Add this content as the value of input
        var content = (new XMLSerializer).serializeToString(svg.node());
      }
      else if(format == "csv"){
        // var content = d3.csv.format(csv_data);
        var content = JSON.stringify(csv_data);
      }

      var form = d3.select("body").append("form").attr("id", "download").attr("action", "/en/visualize/download/").attr("method", "post");
      form.append("input").attr("type", "text").attr("name", "content").attr("value", content);
      form.append("input").attr("type", "text").attr("name", "format").attr("value", format);
      form.append("input").attr("type", "text").attr("name", "title").attr("value", title);

      form.node().submit();

      d3.event.preventDefault();

    });

  }

}
