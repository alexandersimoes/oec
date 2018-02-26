import React, {Component} from "react";
import {Canon} from "datawheel-canon";
import "./App.css";

export default class App extends Component {

  render() {
    return (
      <Canon>
        { this.props.children }
      </Canon>
    );
  }

}
