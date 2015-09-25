function get_container(container){
  if (d3plus.util.d3selection(container)) {
      return container.node();
  }
  return container;
}
function download(container, csv_data){
  return function(){
    var this_container = get_container(container);

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
        var svg = d3.select(this_container).select("svg")
          .attr("title", title)
          .attr("version", 1.1)
          .attr("xmlns", "http://www.w3.org/2000/svg");

        // Add this content as the value of input
        var content = (new XMLSerializer).serializeToString(svg.node());
      }
      else if(format == "csv"){
        // var content = d3.csv.format(csv_data);
        var content = JSON.stringify(csv_data);
      }

      var form = d3.select("form#download");
      form.select("input[name=content]").attr("value", content);
      form.select("input[name=format]").attr("value", format);
      form.select("input[name=title]").attr("value", title);

      form.node().submit();

      d3.event.preventDefault();

    });

  }

}
