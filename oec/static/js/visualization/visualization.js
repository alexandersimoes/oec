var configs = {};

var visualization = function(build, elem) {

  var app = build.app.type; // Alex, is this right?

  d3plus.viz()
    .container(elem)
    .type(app)
    .config(configs.default(build))
    .config(configs[app](build))
    .draw()

}
