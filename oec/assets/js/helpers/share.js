function share(build){

  return function(){
    var lang = build.lang;
    try {
      var same_origin = window.parent.location.host == window.location.host;
    }
    catch (e) {
      var same_origin = false;
    }
    var url = encodeURIComponent("/"+lang+"/visualize/"+build.url)

    // make post request to server for short URL
    d3.json("/"+lang+"/visualize/shorten/")
      .header("Content-type","application/x-www-form-urlencoded")
      .post("url="+url, function(error, data) {
        if (data.error) {
          console.log(data.error)
        }
        else{
          d3.select("#short").style("display", "block")
          d3.selectAll(".modal#share input.short_url").property("value", "http://"+location.host+"/"+data.slug)
        }
      })

    // set embed link
    d3.select(".modal-body input.embed_code").property("value", '<iframe width="560" height="315" src="http://atlas.media.mit.edu/'+lang+'/visualize/embed/'+build.url+'?controls=false" frameborder="0" ></iframe>')

    // set social media link URLs
    d3.selectAll(".modal-body a#Facebook").attr("href", build.social.facebook)
    d3.selectAll(".modal-body a#Twitter").attr("href", build.social.twitter)
    // d3.selectAll(".modal-body a#Google").attr("href", build.social.google)

    // open modal window
    d3.selectAll(".modal#share").classed("active", true);
    d3.selectAll("#mask").classed("visible", true);
    d3.selectAll("body").classed("frozen", true);
  }

}

function popup(href) {
  var width = 600,
      height = 400,
      left = window.screenLeft + window.innerWidth/2 - width/2,
      top = window.screenTop + window.innerHeight/2 - height/2;
  window.open(href, "", "menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=" + height + ",width=" + width + ",left=" + left + ",top=" + top);
  return false;
}
