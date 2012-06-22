///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
// STEP 1.
// Select the first round of options (countries, products, world)
///////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
// STEP 2.
// Assign events to click of selection (products or countries)
///////////////////////////////////////////////////////////////////////////////

$(".featured a").click(click_selection)
$("section[data-uri='products'] a.more").click(show_product_popover("products/view"))
$("section[data-uri='countries'] a.more").click(show_country_popover("countries/view"))

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
// STEP 3.
// Selecting a view - change data popups
///////////////////////////////////////////////////////////////////////////////
$(".accordion").collapse()

$("a.select_country_origin, a.select_country_dest").click(show_country_popover(false))
function show_country_popover(next_uri){
  return function(e){
    $("body").prepend("<div id='popover_bg'>")
    var this_id = $(this).hasClass("select_country_dest") ? "country_dest" : "country_origin";
    if($(".popover#"+this_id).length){
      $(".popover#"+this_id).show()
    }
    else {
      $("<div class='popover' id='"+this_id+"'>").appendTo($("body")).load("/exhibit/country_selection/", function(){
        $(this).find("a.country").parent().parent().data("type", this_id)
        $(this).find("a.country").click(click_selection).attr("class", this_id);
        if(next_uri){
          var next_section = $("section[data-uri='"+next_uri+"']")
          $(this).find("a."+this_id).click(function(){
            change_section(next_section);
          });
        }
      })
    }
    // console.log($(".popover#"+this_id).height())
    $(".popover#"+this_id).css({
      "left": (window.innerWidth / 2) - ($(".popover#"+this_id).width() / 2),
      "top": (window.innerHeight / 2) - 174,
    })
    return false;
  }
}
$("a.select_product").click(show_product_popover(false))
function show_product_popover(next_uri){
  return function(e){
    $("body").prepend("<div id='popover_bg'>")
    if($(".popover#product").length){
      $(".popover#product").show()
    }
    else {
      $("<div class='popover' id='product'>").appendTo($("body")).load("/exhibit/product_selection/", function(){
        $(this).find("a.product").click(click_selection);
        if(next_uri){
          var next_section = $("section[data-uri='"+next_uri+"']")
          $(this).find("a.product").click(function(){
            change_section(next_section);
          });
        }
      })
    }
    $(".popover#product").css({
      "left": (window.innerWidth / 2) - ($(".popover#product").width() / 2),
      "top": (window.innerHeight / 2) - 174,
    })
    return false;
  }
}
$("a.select_trade").click(function(e){
  $("body").prepend("<div id='popover_bg'>")
  if($(".popover#trade").length){
    $(".popover#trade").show()
  }
  else {
    var cont = $("<div class='popover single_col' id='trade'>").appendTo($("body"))
    var list = $("<ul data-type='trade'>").appendTo($("<div class='col_1'>").appendTo(cont))
    list.append("<li><a class='trade' data-abbrv='export' data-prep='to' href='#'>export</a></li>")
    list.append("<li><a class='trade' data-abbrv='import' data-prep='from' href='#'>import</a></li>")
    list.append("<li><a class='trade' data-abbrv='net_export' data-prep='to' href='#'>net export</a></li>")
    list.append("<li><a class='trade' data-abbrv='net_import' data-prep='from' href='#'>net import</a></li>")
    list.find("a").click(click_selection)
  }
  $(".popover#trade").css({
    "left": (window.innerWidth / 2) - ($(".popover#trade").width() / 2),
    "top": (window.innerHeight / 2) - 86,
  })
  return false;
})
$("a.select_year").click(function(e){
  if($(".popover#year").length){
    $(".popover#year").show()
  }
  else {
    var cont = $("<div class='popover single_col' id='year'>").appendTo($("body"))
    var list = $("<ul data-type='year'>").appendTo($("<div class='col_1'>").appendTo(cont))
    list.append("<li><a data-abbrv='1995' href='#'>1995</a></li>")
    list.append("<li><a data-abbrv='1996' href='#'>1996</a></li>")
    list.append("<li><a data-abbrv='1997' href='#'>1997</a></li>")
    list.append("<li><a data-abbrv='1998' href='#'>1998</a></li>")
    list.append("<li><a data-abbrv='1999' href='#'>1999</a></li>")
    list.append("<li><a data-abbrv='2000' href='#'>2000</a></li>")
    list.append("<li><a data-abbrv='2001' href='#'>2001</a></li>")
    list.append("<li><a data-abbrv='2002' href='#'>2002</a></li>")
    list.append("<li><a data-abbrv='2003' href='#'>2003</a></li>")
    list.append("<li><a data-abbrv='2004' href='#'>2004</a></li>")
    list.append("<li><a data-abbrv='2005' href='#'>2005</a></li>")
    list.append("<li><a data-abbrv='2006' href='#'>2006</a></li>")
    list.append("<li><a data-abbrv='2007' href='#'>2007</a></li>")
    list.append("<li><a data-abbrv='2008' href='#'>2008</a></li>")
    list.append("<li><a data-abbrv='2009' href='#'>2009</a></li>")
    list.append("<li><a data-abbrv='2010' href='#'>2010</a></li>")
    list.find("a").click(click_selection)
  }
  $(".popover#year").css({
    "left": e.pageX + 70,
    "top": e.pageY - 40,
  })
  return false;
})
$(document).click(function(){
  $(".popover").hide()
  $("#popover_bg").hide();
})

// When user makes their selection
$(".select .next").click(function(){
  var table_options = $(this).parent().prev().find("tr:nth-child(2) td")
  table_options.each(function(i, e){
    var abbrv = $(e).data().abbrv;
    var type = $(e).data().type;
    var name = $(e).text();
    App[type] = {
      "abbrv": abbrv,
      "name": name
    }
  })
  if(App.product.abbrv != "show" && App.product.abbrv != "all" && (App.product.abbrv+"").length < 4){
    App.product.abbrv = "0"+App.product.abbrv;
  }
  var url_request = [App.trade.abbrv, App.country_origin.abbrv, App.country_dest.abbrv, App.product.abbrv, App.year.abbrv]
  url_request = "/api/"+url_request.join("/")+"/";
  d3.json(url_request, function(json){
    // console.log(json)
    build_app(json, url_request)
  });
  return false;
})
// build the app given the data from the server
function build_app(json, request, app_type){
  // put data into common variables to they can be called from their respective
  // app functions
  json.attr_data.forEach(function(attr){
   var id_property = attr["community_id"] ? "community_id" : "region_id",
     name_property = attr["community__name"] ? "community__name" : "region__name",
     color_property = attr["community__color"] ? "community__color" : "region__color",
     text_color_property = attr["community__text_color"] ? "community__text_color" : "region__text_color";
   attr["category_id"] = attr[id_property]; delete attr[id_property];
   attr["category_name"] = attr[name_property]; delete attr[name_property];
   attr["category_color"] = attr[color_property]; delete attr[color_property];
   attr["category_text_color"] = attr[text_color_property]; delete attr[text_color_property];
   attr["heirarchical_id"] = attr["category_id"].toString().substr(0,1) + "." + attr["category_id"] + "." + attr["id"];
  })
  
  // turn flat attributes array into indexed object with ids
  // either country or products as the key
  json.attr_data = d3.nest()
    .key(function(d) { return d["id"]; })
    .rollup(function(d){ return d[0] })
    .map(json.attr_data);
  
  // the parameters that will be passed to the respective app
  var app_data = {
    "attr_data": json.attr_data,
    "raw_data": json.data,
    "selector": "#dataviz",
    "year": json.year,
    "other": json.other}
  
  if(app_type == "tree_map"){
    app_data.height = 600;
    app_data.width = 840;
    $("#dataviz").css("width",840);
    $("#dataviz").css("margin-left",0);
    var app = new TreeMap(app_data);
    app.build();
  }
  if(app_type == "product_space"){
    app_data.height = 600;
    app_data.width = 840;
    $("#dataviz").css("width",840);
    $("#dataviz").css("margin-left",0);
    var app = new ProductSpace(app_data);
  }
  if(app_type == "map"){
    app_data.height = 450;
    app_data.width = 640;
    $("#dataviz").css("width",740);
    $("#dataviz").css("margin-left",100);
    var app = new Map(app_data);
    app.build();
  }
}

//
// GENERAL STUFF
// Transition from one section to the next
function change_section(next_section, option){
  var selected_pos = next_section.data().pos
  var current_pos = $("section.current").data().pos
  
  var direction = selected_pos - current_pos;
  if(!direction){
    return;
  }
  else if(direction > 0){
    $(".back.btn").css("opacity", 1)
    $("section.current").removeClass().addClass("prev")
    next_section.removeClass().addClass("current")
  }
  else {
    $(".back.btn").css("opacity", 0)
    $("section.current").removeClass()
    next_section.removeClass().addClass("current")
  }
}
$("a.next").click(function(){
  $(this).parents("section").find("a.tag").remove()
  // var bcrumb = $('<a class="tag btn btn-large" href="#"><i class="icon-chevron-left" style="margin-top:3px;"></i> Back</a>').appendTo($(this).parents("section"));
  // bcrumb.click(prev_section)
  
  var next_section_uri = $(this).attr("href")
  var next_section = $("section[data-uri='"+next_section_uri+"']")
  change_section(next_section)
  
  return false;
})
$(".back.btn").click(function(){
  change_section($("section[data-pos='0']"));
  return false;
})
function prev_section(e){
  var next_section = $(this).parents("section");
  change_section(next_section);
  $(this).remove();
}

function click_selection(){
  var type = $(this).parent().parent().data().type;
  var abbrv = $(this).data().abbrv;
  var name = $(this).text();
  // console.log(type, abbrv, name)
  var element_to_change = $(".select_trade").parents(".accordion-body").prev().find("span.select_"+type);
  // console.log(element_to_change)
  if(type == "trade"){
    var prep = $(this).data().prep
    $(".select_trade").parents(".accordion-body").prev().find("span.select_prep").text(prep);
  }
  element_to_change.text(name)
  element_to_change.data("abbrv", abbrv)
  $(".popover").hide();
  $("#popover_bg").hide();
}

// Scroll events
function scroll(div_to_scroll, updown){
  return function(){
    div_to_scroll.scrollTop(div_to_scroll.scrollTop()+(15*updown))
  }
}
var interval_id = 0;
$("a.scroll").live("click", function(e){
  var div_to_scroll = $(this).siblings("ul");
  var updown = $(this).hasClass("down") ? 1 : -1;
  div_to_scroll.scrollTop(div_to_scroll.scrollTop()+(35*updown))
  e.stopPropagation();
})
$("a.scroll").live("mousedown", function(e){
  var div_to_scroll = $(this).siblings("ul");
  var updown = $(this).hasClass("down") ? 1 : -1;
  interval_id = setInterval(scroll(div_to_scroll, updown), 60);
  return false;
}).live("mouseup mouseleave", function(e) {
  clearInterval(interval_id);
  return false;
});

$(".col_1 li a").live("click", function(){
  // remove class selected of any that are
  $(".col_1 li a").removeClass("selected")
  $(this).addClass("selected")
  var class_list = $(this).attr("class").split(/\s+/);
  class_list.splice(class_list.indexOf('selected'), 1);
  var class_name = class_list[0]
  $(".col_2 li").hide();
  $(".col_2 li."+class_name).show();
  return false;
})






///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
// Build app !!!
///////////////////////////////////////////////////////////////////////////////
$(".next.btn").click(function(){
  var app = $(this).data().app;
  var type = $(this).parents(".accordion-group").data().type;
  var title = $(this).parents(".accordion-body").prev().find(".accordion-toggle").text();
  switch(type) {
    case "casy":
      var trade_flow = $(this).parents(".accordion-body").prev().find("span.select_trade").data().abbrv;
      var country_origin = $(this).parents(".accordion-body").prev().find("span.select_country_origin").data().abbrv;
      var country_dest = "all"
      var product = "show"
      var sub_heading = "Top Products"
      break;
    case "csay":
      var trade_flow = $(this).parents(".accordion-body").prev().find("span.select_trade").data().abbrv;
      var country_origin = $(this).parents(".accordion-body").prev().find("span.select_country_origin").data().abbrv;
      var country_dest = "show";
      var product = "all";
      var sub_heading = "Top Countries"
      break;
    case "ccsy":
      var trade_flow = $(this).parents(".accordion-body").prev().find("span.select_trade").data().abbrv;
      var country_origin = $(this).parents(".accordion-body").prev().find("span.select_country_origin").data().abbrv;
      var country_dest = $(this).parents(".accordion-body").prev().find("span.select_country_dest").data().abbrv;
      var product = "show";
      var sub_heading = "Top Products";
      break;
    case "cspy":
      var trade_flow = $(this).parents(".accordion-body").prev().find("span.select_trade").data().abbrv;
      var country_origin = $(this).parents(".accordion-body").prev().find("span.select_country_origin").data().abbrv;
      var country_dest = "show";
      var product = $(this).parents(".accordion-body").prev().find("span.select_product").data().abbrv;
      var sub_heading = "Top Countries"
      break;
    case "sapy":
      var trade_flow = $(this).parents(".accordion-body").prev().find("span.select_trade").data().abbrv;
      var country_origin = "show";
      var country_dest = "all";
      var product = $(this).parents(".accordion-body").prev().find("span.select_product").data().abbrv;
      var sub_heading = "Top Countries"
      break;
  }
  if(parseInt(product) == product && (product+"").length < 4){
    product = "0"+product;
  }
  var url_request = "/api/"+trade_flow+"/"+country_origin+"/"+country_dest+"/"+product+"/2009/";
  change_viz(title, sub_heading, app, url_request)
})

function change_viz(title, sub_heading, app, url_request){
  $("section[data-uri='app'] h1").text(title);
  // clear previous data
  $("#datainfo").html("");
  $("#dataviz").html("<div class='loading'>Loading...</div>")
  // now get the data
  d3.json(url_request, function(json){
    build_app(json, url_request, app)
    add_top_elements(json, app, sub_heading);
    // if product space get nearby products
    if(app == "product_space"){
      d3.json("/api/near/"+json.country1.name_3char+"/2009/5/", function(nearby_prods){
        add_nearby_prods(nearby_prods, json.attr_data)
      })
    }
  });
}

function add_top_elements(json, app, sub_heading){
  var current_data = json.data.filter(function(x){return x.year == json.year});
  current_data.sort(function(a, b){
    if (a.value < b.value) return 1;
    if (a.value > b.value) return -1;
    return 0;
  })
  // get sum for percentages
  var sum = 0;
  current_data.forEach(function(x){ sum += parseFloat(x["value"]); })
  // if(app == "tree_map"){
  //   $("#datainfo").append("<h2>"+sub_heading+"</h2>");
  // }
  // if(app == "product_space"){
  var list = $('<ul class="nav nav-tabs" id="myTab">').appendTo("#datainfo");
  var li = $("<li class='active'>").appendTo(list);
  var a = $('<a href="#top">'+sub_heading+'</a>').appendTo(li);
  a.click(function(){ return false; })
  var tabs = $('<div class="tab-content">').appendTo("#datainfo");
  var top_tab = $('<div class="tab-pane active" id="top">').appendTo(tabs);

  // }
  // Loop through top 5 elements
  for(var i = 0; i < 5; i++){
    var item = current_data[i];
    var item_attr = json.attr_data[item.item_id]
    // console.log(item_attr)
    if(item_attr.name_3char){
      var change_link = $("<a href='#'><img src='/media/img/icons/flag_"+item_attr.name_3char.toLowerCase()+".png' />"+item_attr.name+"</a>").appendTo(top_tab)
      var title = "What products does "+item_attr.name+" export?"
      var sub_heading = "Top Products"
      var url_request = "/api/export/"+item_attr.name_3char+"/all/show/2009/"
    }
    else {
      var change_link = $("<a href='#'><img src='/media/img/icons/community_"+item_attr.category_id+".png' />"+item_attr.name+"</a>").appendTo(top_tab)
      var title = "What countries export "+item_attr.name+"?"
      var sub_heading = "Top Countries"
      var url_request = "/api/export/show/all/"+item_attr.code+"/2009/"
    }
    // change_link.click(xx(title));
    (function(a, b, c, d) {
      change_link.click(function(){ 
        change_viz(a, b, c, d);
        return false;
      });
    })(title, sub_heading, "tree_map", url_request);
    // change_link.click(function(){
    //   console.log(title)
    //   change_viz(title, sub_heading, "tree_map", url_request);
    // })
    
    var t = $("<table>").appendTo(top_tab);
    t.append("<tr><td>Value</td><td>$"+format_big_num(item.value)[0]+format_big_num(item.value)[1]+"</td></tr>")
    t.append("<tr><td>Percent of total trade</td><td>"+d3.format(".2p")(item.value/sum)+"</td></tr>")
  }
  
}

function add_nearby_prods(nearby_prods, attr_data){
  // console.log("building newby prods")
  $("#myTab").append('<li><a href="#nearby">Nearby Products</a></li>')
  var nearby_tab = $('<div class="tab-pane" id="nearby">').appendTo(".tab-content")
  
  nearby_prods.forEach(function(np){
    var density = np[0]
    var p_id = np[1]
    var item_attr = attr_data[p_id]
    
    var change_link = $("<a href='#'><img src='/media/img/icons/community_"+item_attr.category_id+".png' />"+item_attr.name+"</a>").appendTo(nearby_tab);
    // var title = "What countries export "+item_attr.name+"?"
    // var sub_heading = "Top Countries"
    // var url_request = "/api/export/show/all/"+item_attr.code+"/2009/"
      
    // change_link.click(xx(title));
    (function(id) {
      change_link.click(function(){ 
        d3.select("circle#overlay_"+id).remove();
        var overlay = clone("circle#id_"+id)
        overlay.attr("id", "overlay_"+id)
          .style("fill", "none")
          .style("stroke", "red")
          .style("stroke-opacity", 1e-6)
          .style("stroke-width", 3)
        .transition()
          .duration(750)
          .attr("r", 12)
          .style("stroke-opacity", 1);
        return false;
      });
      
    })(p_id);
    
    var t = $("<table>").appendTo(nearby_tab);
    t.append("<tr><td>Density Value</td><td>"+d3.format(".4g")(density)+"</td></tr>")
    
  })
  
  $('#myTab a').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
  })
}

function clone(selector) {
  var node = d3.select(selector).node();
  return d3.select(node.parentNode.insertBefore(node.cloneNode(true), node.nextSibling));
}