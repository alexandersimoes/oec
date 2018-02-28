import React, {Component} from "react";
import {Geomap} from "d3plus-react";
import worldtopo from "data/worldtopo.json";

export default class MapIcon extends Component {

  render() {
    return (
      <Geomap config={{
        constrole: false,
        data: [],
        height: 250,
        legend: false,
        ocean: "transparent",
        tiles: false,
        topojson: worldtopo,
        topojsonId: d => d.id,
        topojsonKey: "objects",
        fitObject: worldtopo,
        fitFilter: d => {
          // if (d.id === "231") {
          //   console.log(d);
          // }
          // https://api.datausa.io/attrs/birthplace/
          return `${d.id}` === "231";
        },
        shapeConfig: {
          Path: {
            fillOpacity: d => `${d.id}` === "231" ? 1 : "0.25",
            stroke: "#63737f"
          }
        },
        width: 250,
        zoom: false
      }} />
    );
  }

}
